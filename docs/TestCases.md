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
* Duration: 1681s 
* Code: 1793871001
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 128Gi RAM. RAM limit is 128Gi.

### Connections
* mariadb-1-1-1-1-1 uses docker image mariadb:12.3.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:872811
  * datadisk:4478
  * volume_size:1.8T
  * volume_used:853G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871001
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:843416
  * datadisk:5472
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871001
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:927558
  * datadisk:37628
  * volume_size:1.8T
  * volume_used:906G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871001
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:843415
  * datadisk:5788
  * volume_size:1.8T
  * volume_used:824G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793871001

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1793871001-5cfd995f47-rjqh9: 0
* bexhoma-sut-monetdb-1-1793871001-56d8bf9c6d-g768j: 0
* bexhoma-sut-mysql-1-1793871001-679c8f5498-fnhh6: 0
* bexhoma-sut-postgresql-1-1793871001-68d5765d56-9fvs8: 0

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

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1    |                1 |    1 |      168.00 |           1.00 |            0.00 |         64.00 |           94.00 |              8 |           0 |             | None           |             0 | False         |               21.43 | False               |
| MonetDB-1-1    |                1 |    1 |      173.00 |           1.00 |            0.00 |        139.00 |           20.00 |              8 |           0 |             | None           |             0 | False         |               20.81 | False               |
| MySQL-1-1      |                1 |    1 |      216.00 |           1.00 |            1.00 |         67.00 |          139.00 |              8 |           0 |             | None           |             0 | False         |               16.67 | False               |
| PostgreSQL-1-1 |                1 |    1 |       91.00 |           2.00 |            1.00 |         42.00 |           36.00 |              8 |           0 |             | None           |             0 | False         |               39.56 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| mariadb-1-1-1-1-1    | MariaDB-1       | mariadb-1-1-1    | mariadb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        334 |            0.73 |             4988.14 |           1067.07 |          -1 | mariadb-1-1-1-1-1    |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         20 |            0.04 |           113348.44 |          17820.00 |          -1 | monetdb-1-1-1-1-1    |
| mysql-1-1-1-1-1      | MySQL-1         | mysql-1-1-1      | mysql-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        516 |            0.80 |             4551.58 |            690.70 |          -1 | mysql-1-1-1-1-1      |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        172 |            0.29 |            12573.61 |           2072.09 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1    | mariadb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        334 |            0.73 |             4988.14 |           1067.07 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         20 |            0.04 |           113348.44 |          17820.00 |          -1 |
| mysql-1-1-1      | mysql-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        516 |            0.80 |             4551.58 |            690.70 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        172 |            0.29 |            12573.61 |           2072.09 |          -1 |

#### Query Completion per Phase

| phase            |   pods | TPC-DS Q1   | TPC-DS Q2   | TPC-DS Q3   | TPC-DS Q4   | TPC-DS Q5   | TPC-DS Q6   | TPC-DS Q7   | TPC-DS Q8   | TPC-DS Q9   | TPC-DS Q10   | TPC-DS Q11   | TPC-DS Q12   | TPC-DS Q13   | TPC-DS Q14a+b   | TPC-DS Q15   | TPC-DS Q16   | TPC-DS Q17   | TPC-DS Q18   | TPC-DS Q19   | TPC-DS Q20   | TPC-DS Q21   | TPC-DS Q22   | TPC-DS Q23a+b   | TPC-DS Q24a+b   | TPC-DS Q25   | TPC-DS Q26   | TPC-DS Q27   | TPC-DS Q28   | TPC-DS Q29   | TPC-DS Q30   | TPC-DS Q31   | TPC-DS Q32   | TPC-DS Q33   | TPC-DS Q34   | TPC-DS Q35   | TPC-DS Q36   | TPC-DS Q37   | TPC-DS Q38   | TPC-DS Q39a+b   | TPC-DS Q40   | TPC-DS Q41   | TPC-DS Q42   | TPC-DS Q43   | TPC-DS Q44   | TPC-DS Q45   | TPC-DS Q46   | TPC-DS Q47   | TPC-DS Q48   | TPC-DS Q49   | TPC-DS Q50   | TPC-DS Q51   | TPC-DS Q52   | TPC-DS Q53   | TPC-DS Q54   | TPC-DS Q55   | TPC-DS Q56   | TPC-DS Q57   | TPC-DS Q58   | TPC-DS Q59   | TPC-DS Q60   | TPC-DS Q61   | TPC-DS Q62   | TPC-DS Q63   | TPC-DS Q64   | TPC-DS Q65   | TPC-DS Q66   | TPC-DS Q67   | TPC-DS Q68   | TPC-DS Q69   | TPC-DS Q70   | TPC-DS Q71   | TPC-DS Q72   | TPC-DS Q73   | TPC-DS Q74   | TPC-DS Q75   | TPC-DS Q76   | TPC-DS Q77   | TPC-DS Q78   | TPC-DS Q79   | TPC-DS Q80   | TPC-DS Q81   | TPC-DS Q82   | TPC-DS Q83   | TPC-DS Q84   | TPC-DS Q85   | TPC-DS Q86   | TPC-DS Q87   | TPC-DS Q88   | TPC-DS Q89   | TPC-DS Q90   | TPC-DS Q91   | TPC-DS Q92   | TPC-DS Q93   | TPC-DS Q94   | TPC-DS Q95   | TPC-DS Q96   | TPC-DS Q97   | TPC-DS Q98   | TPC-DS Q99   | complete   |
|:-----------------|-------:|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:----------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-------------|:-----------|
| mariadb-1-1-1    |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| monetdb-1-1-1    |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| mysql-1-1-1      |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |
| postgresql-1-1-1 |      1 | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1         | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1             | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | 1/1          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries       |   mariadb-1-1-1-1-1 |   monetdb-1-1-1-1-1 |   mysql-1-1-1-1-1 |   postgresql-1-1-1-1-1 |
|:--------------|--------------------:|--------------------:|------------------:|-----------------------:|
| TPC-DS Q1     |               16.52 |               26.59 |            235.43 |                  86.36 |
| TPC-DS Q2     |             4017.16 |               55.40 |           3654.58 |                 205.67 |
| TPC-DS Q3     |                9.17 |               14.96 |             11.71 |                 130.38 |
| TPC-DS Q4     |            10591.35 |              358.45 |          44866.41 |                6290.86 |
| TPC-DS Q5     |             8779.10 |               48.60 |          15167.96 |                 395.40 |
| TPC-DS Q6     |              762.71 |               31.59 |          60238.18 |               53117.10 |
| TPC-DS Q7     |             3351.41 |               25.56 |           1595.43 |                 336.49 |
| TPC-DS Q8     |              411.85 |               16.89 |            352.31 |                 104.57 |
| TPC-DS Q9     |             4268.47 |               43.20 |           3768.47 |                1919.23 |
| TPC-DS Q10    |              177.53 |               16.01 |            638.34 |                 986.86 |
| TPC-DS Q11    |             6948.49 |              166.15 |          27477.07 |                3812.73 |
| TPC-DS Q12    |              254.63 |               10.22 |            242.36 |                  56.09 |
| TPC-DS Q13    |              925.37 |               21.84 |           1975.41 |                 562.06 |
| TPC-DS Q14a+b |            44045.19 |              795.43 |          42119.85 |                1681.50 |
| TPC-DS Q15    |              135.72 |                9.56 |            157.16 |                  96.23 |
| TPC-DS Q16    |             8831.45 |               15.80 |            420.90 |                 181.37 |
| TPC-DS Q17    |              738.91 |               50.95 |            930.17 |                 264.44 |
| TPC-DS Q18    |             1815.92 |               50.56 |           1214.80 |                 335.56 |
| TPC-DS Q19    |              233.59 |               18.08 |            250.64 |                 144.87 |
| TPC-DS Q20    |              448.84 |               12.82 |            434.28 |                  86.41 |
| TPC-DS Q21    |             4386.01 |               56.57 |           1760.19 |                 178.68 |
| TPC-DS Q22    |            10557.19 |              483.74 |           6627.71 |                2883.25 |
| TPC-DS Q23a+b |            58768.07 |              874.04 |          45484.54 |                4425.15 |
| TPC-DS Q24a+b |             1456.41 |               98.36 |           2756.28 |                 583.43 |
| TPC-DS Q25    |              120.79 |               61.72 |            183.21 |                 277.07 |
| TPC-DS Q26    |              608.94 |                9.06 |            422.16 |                 199.34 |
| TPC-DS Q27    |             2395.68 |               38.32 |            413.69 |                 316.60 |
| TPC-DS Q28    |             2534.88 |               30.99 |           3164.84 |                 612.95 |
| TPC-DS Q29    |               87.73 |               54.28 |            110.96 |                 292.06 |
| TPC-DS Q30    |              103.45 |               13.11 |            413.91 |                8458.63 |
| TPC-DS Q31    |             1022.75 |               54.50 |          10192.61 |                1424.49 |
| TPC-DS Q32    |                7.85 |               10.21 |            174.65 |                 103.10 |
| TPC-DS Q33    |              175.30 |               11.06 |            781.02 |                 335.08 |
| TPC-DS Q34    |             2439.51 |               14.08 |           1322.59 |                  23.15 |
| TPC-DS Q35    |              919.66 |               31.72 |          12719.52 |                1080.58 |
| TPC-DS Q36    |             2216.65 |               48.89 |           2796.39 |                 317.23 |
| TPC-DS Q37    |             2946.46 |               48.20 |              8.37 |                 256.76 |
| TPC-DS Q38    |             5382.31 |               80.12 |           6557.64 |                 844.33 |
| TPC-DS Q39a+b |              997.89 |              451.50 |           1360.36 |                2016.65 |
| TPC-DS Q40    |              210.27 |               28.22 |            127.66 |                  99.05 |
| TPC-DS Q41    |              381.86 |                3.92 |           1122.62 |                 850.65 |
| TPC-DS Q42    |              182.53 |                9.82 |             60.37 |                  74.10 |
| TPC-DS Q43    |              798.76 |               23.30 |              1.64 |                  23.75 |
| TPC-DS Q44    |                1.31 |               19.48 |              5.92 |                   1.71 |
| TPC-DS Q45    |              104.16 |                6.49 |            118.86 |                  67.30 |
| TPC-DS Q46    |             2797.37 |               20.37 |           1085.04 |                  25.44 |
| TPC-DS Q47    |            14229.80 |               96.45 |           9901.44 |                1813.12 |
| TPC-DS Q48    |              852.33 |               19.64 |           1358.07 |                 456.49 |
| TPC-DS Q49    |               97.29 |               44.79 |            124.74 |                 313.20 |
| TPC-DS Q50    |               21.52 |               47.69 |             26.59 |                 298.71 |
| TPC-DS Q51    |             6203.61 |              161.55 |           7349.67 |                 673.04 |
| TPC-DS Q52    |              166.26 |               11.12 |             23.02 |                  58.61 |
| TPC-DS Q53    |              112.83 |               15.99 |            197.81 |                  79.95 |
| TPC-DS Q54    |              899.61 |               10.96 |           2556.15 |                  64.58 |
| TPC-DS Q55    |              164.32 |                8.15 |             17.82 |                  60.47 |
| TPC-DS Q56    |              218.86 |               10.70 |            184.63 |                 294.82 |
| TPC-DS Q57    |             4958.00 |               41.83 |           3172.81 |                 669.19 |
| TPC-DS Q58    |             4323.69 |               15.62 |           5968.01 |                 284.89 |
| TPC-DS Q59    |             6779.91 |               48.56 |           5096.71 |                 283.26 |
| TPC-DS Q60    |              692.68 |               17.02 |            333.55 |                 324.58 |
| TPC-DS Q61    |              258.58 |               24.27 |              2.04 |                 104.26 |
| TPC-DS Q62    |             1284.92 |               14.87 |           3344.35 |                  73.25 |
| TPC-DS Q63    |              126.11 |               19.27 |            340.95 |                  92.03 |
| TPC-DS Q64    |              501.95 |              123.38 |            337.41 |                 493.08 |
| TPC-DS Q65    |             4451.62 |               35.36 |           5505.31 |                 438.00 |
| TPC-DS Q66    |              907.20 |               47.94 |           2453.06 |                 152.55 |
| TPC-DS Q67    |             5176.04 |              150.05 |           7333.75 |                3662.73 |
| TPC-DS Q68    |             2424.32 |               22.23 |            257.57 |                  29.80 |
| TPC-DS Q69    |                2.48 |                9.74 |              2.80 |                 101.53 |
| TPC-DS Q70    |             5976.82 |               31.18 |          11162.66 |                 342.68 |
| TPC-DS Q71    |              331.30 |               19.31 |            487.20 |                 241.51 |
| TPC-DS Q72    |              607.29 |              105.08 |           8629.42 |                 727.26 |
| TPC-DS Q73    |             2240.59 |               17.13 |           1354.15 |                  31.08 |
| TPC-DS Q74    |             4827.13 |               57.88 |          29383.23 |                 908.82 |
| TPC-DS Q75    |             4383.13 |              164.86 |           4652.49 |                 504.39 |
| TPC-DS Q76    |              620.55 |               17.67 |            883.26 |                 152.74 |
| TPC-DS Q77    |             4743.65 |               29.38 |           9949.78 |                 222.83 |
| TPC-DS Q78    |             4624.88 |              256.97 |          18486.98 |                1442.91 |
| TPC-DS Q79    |             2874.34 |               28.09 |           4766.10 |                 143.72 |
| TPC-DS Q80    |              438.84 |              207.52 |          10313.93 |                 339.60 |
| TPC-DS Q81    |              166.45 |               16.26 |           1941.34 |               35648.27 |
| TPC-DS Q82    |             3184.12 |               78.40 |              9.09 |                 216.72 |
| TPC-DS Q83    |              756.92 |                7.03 |            911.87 |                  60.25 |
| TPC-DS Q84    |               40.52 |               18.52 |             86.84 |                  63.46 |
| TPC-DS Q85    |              117.42 |               47.02 |             88.53 |                 250.31 |
| TPC-DS Q86    |              703.88 |               13.60 |            976.24 |                 178.74 |
| TPC-DS Q87    |             6190.74 |               74.47 |           7751.11 |                 800.69 |
| TPC-DS Q88    |             6987.67 |               27.89 |           2422.99 |                2188.38 |
| TPC-DS Q89    |             1208.16 |               18.92 |            117.88 |                  94.50 |
| TPC-DS Q90    |              289.36 |                5.33 |            374.48 |                 108.78 |
| TPC-DS Q91    |               18.32 |               12.58 |             23.02 |                 126.31 |
| TPC-DS Q92    |                4.08 |                7.22 |             16.88 |                  41.21 |
| TPC-DS Q93    |               36.14 |               42.36 |             50.02 |                 176.77 |
| TPC-DS Q94    |              396.64 |                8.74 |            429.33 |                 126.12 |
| TPC-DS Q95    |              689.83 |               90.09 |           4100.90 |                2835.30 |
| TPC-DS Q96    |              558.49 |                6.28 |            201.12 |                  70.25 |
| TPC-DS Q97    |             4841.63 |               75.17 |           7478.76 |                 314.89 |
| TPC-DS Q98    |              769.79 |               19.52 |            984.45 |                 149.54 |
| TPC-DS Q99    |             2810.27 |               21.07 |          11417.64 |                 120.48 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

|                   |   TPC-DS Q1 |   TPC-DS Q2 |   TPC-DS Q3 |   TPC-DS Q4 |   TPC-DS Q5 |   TPC-DS Q6 |   TPC-DS Q7 |   TPC-DS Q8 |   TPC-DS Q9 |   TPC-DS Q10 |   TPC-DS Q11 |   TPC-DS Q12 |   TPC-DS Q13 |   TPC-DS Q14a+b |   TPC-DS Q15 |   TPC-DS Q16 |   TPC-DS Q17 |   TPC-DS Q18 |   TPC-DS Q19 |   TPC-DS Q20 |   TPC-DS Q21 |   TPC-DS Q22 |   TPC-DS Q23a+b |   TPC-DS Q24a+b |   TPC-DS Q25 |   TPC-DS Q26 |   TPC-DS Q27 |   TPC-DS Q28 |   TPC-DS Q29 |   TPC-DS Q30 |   TPC-DS Q31 |   TPC-DS Q32 |   TPC-DS Q33 |   TPC-DS Q34 |   TPC-DS Q35 |   TPC-DS Q36 |   TPC-DS Q37 |   TPC-DS Q38 |   TPC-DS Q39a+b |   TPC-DS Q40 |   TPC-DS Q41 |   TPC-DS Q42 |   TPC-DS Q43 |   TPC-DS Q44 |   TPC-DS Q45 |   TPC-DS Q46 |   TPC-DS Q47 |   TPC-DS Q48 |   TPC-DS Q49 |   TPC-DS Q50 |   TPC-DS Q51 |   TPC-DS Q52 |   TPC-DS Q53 |   TPC-DS Q54 |   TPC-DS Q55 |   TPC-DS Q56 |   TPC-DS Q57 |   TPC-DS Q58 |   TPC-DS Q59 |   TPC-DS Q60 |   TPC-DS Q61 |   TPC-DS Q62 |   TPC-DS Q63 |   TPC-DS Q64 |   TPC-DS Q65 |   TPC-DS Q66 |   TPC-DS Q67 |   TPC-DS Q68 |   TPC-DS Q69 |   TPC-DS Q70 |   TPC-DS Q71 |   TPC-DS Q72 |   TPC-DS Q73 |   TPC-DS Q74 |   TPC-DS Q75 |   TPC-DS Q76 |   TPC-DS Q77 |   TPC-DS Q78 |   TPC-DS Q79 |   TPC-DS Q80 |   TPC-DS Q81 |   TPC-DS Q82 |   TPC-DS Q83 |   TPC-DS Q84 |   TPC-DS Q85 |   TPC-DS Q86 |   TPC-DS Q87 |   TPC-DS Q88 |   TPC-DS Q89 |   TPC-DS Q90 |   TPC-DS Q91 |   TPC-DS Q92 |   TPC-DS Q93 |   TPC-DS Q94 |   TPC-DS Q95 |   TPC-DS Q96 |   TPC-DS Q97 |   TPC-DS Q98 |   TPC-DS Q99 |
|:------------------|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|----------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|-------------:|
| monetdb-1-1-1-1-1 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |        0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |            0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         1.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |         0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST failed: SQL warnings (result mismatch)
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>
