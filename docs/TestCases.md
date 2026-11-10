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
* Duration: 1308s 
* Code: 1794055305
* This includes the reading queries of TPC-DS.
* This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
  * TPC-DS (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q99.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.13.
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
  * disk:896286
  * datadisk:4474
  * volume_size:1.8T
  * volume_used:876G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--innodb-read-io-threads=64', '--innodb-write-io-threads=64', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-io-capacity=200', '--innodb-io-capacity-max=1000', '--innodb-log-buffer-size=1G', '--tmp-table-size=1G', '--max-heap-table-size=1G']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* monetdb-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:890647
  * datadisk:5472
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* mysql-1-1-1-1-1 uses docker image mysql:9.7.2
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:896286
  * datadisk:37644
  * volume_size:1.8T
  * volume_used:876G
  * cpu_list:0-223
  * args:['--max_connections=1500', '--character-set-server=utf8mb4', '--collation-server=utf8mb4_bin', '--local-infile=1', '--innodb-redo-log-capacity=32GB', '--innodb-io-capacity=400', '--innodb-io-capacity_max=2000', '--innodb-read-io-threads=8', '--innodb-write-io-threads=8', '--innodb-use-native-aio=0', '--innodb-buffer-pool-size=8G', '--innodb-buffer-pool-instances=8', '--innodb-flush-method=O_DIRECT', '--innodb-flush-neighbors=0', '--skip-log-bin', '--innodb-change-buffer-max-size=50', '--tmpdir=/mysqltmp', '--ssl-ca=/etc/mysql/certs/ca.pem', '--ssl-cert=/etc/mysql/certs/server-cert.pem', '--ssl-key=/etc/mysql/certs/server-key.pem']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305
* postgresql-1-1-1-1-1 uses docker image postgres:18.6
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:890647
  * datadisk:5794
  * volume_size:1.8T
  * volume_used:870G
  * cpu_list:0-223
  * args:['-c', 'max_connections=640', '-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'shared_buffers=16GB', '-c', 'effective_cache_size=40GB', '-c', 'work_mem=512MB', '-c', 'maintenance_work_mem=2GB', '-c', 'autovacuum=off', '-c', 'wal_level=minimal', '-c', 'max_wal_senders=0', '-c', 'max_wal_size=32GB', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_completion_target=1.0', '-c', 'lock_timeout=30s', '-c', 'idle_in_transaction_session_timeout=30000']
  * requests_cpu:4
  * requests_memory:128Gi
  * limits_memory:128Gi
  * resources_total: 4.0 CPU, 128.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 128.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794055305

### SUT Container Restarts
* bexhoma-sut-mariadb-1-1794055305-7c59c75f95-gt4ld: 0
* bexhoma-sut-monetdb-1-1794055305-655cf6db5b-z77sf: 0
* bexhoma-sut-mysql-1-1794055305-7f775d78b-sbhhg: 0
* bexhoma-sut-postgresql-1-1794055305-68cbc8c9f8-ncr44: 0

### Workflow

#### Actual

* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)

#### Planned

* DBMS PostgreSQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MySQL-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MariaDB-1 - Experiment 1 Client 1: tpcds (1 pods)
* DBMS MonetDB-1 - Experiment 1 Client 1: tpcds (1 pods)

### Loading

#### Per Run

|                |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:---------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| MariaDB-1-1    |                1 |    1 |      180.00 |           4.00 |            1.00 |         66.00 |           99.00 |              8 |           0 |             | None           |             0 | False         |               20.00 | False               |
| MonetDB-1-1    |                1 |    1 |      161.00 |           3.00 |            1.00 |        118.00 |           27.00 |              8 |           0 |             | None           |             0 | False         |               22.36 | False               |
| MySQL-1-1      |                1 |    1 |      212.00 |           4.00 |            1.00 |         60.00 |          137.00 |              8 |           0 |             | None           |             0 | False         |               16.98 | False               |
| PostgreSQL-1-1 |                1 |    1 |      100.00 |           5.00 |            1.00 |         40.00 |           43.00 |              8 |           0 |             | None           |             0 | False         |               36.00 | False               |

### Benchmarking

#### Per Connection

| DBMS                 | configuration   | phase            | job                |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod                  |
|:---------------------|:----------------|:-----------------|:-------------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:---------------------|
| mariadb-1-1-1-1-1    | MariaDB-1       | mariadb-1-1-1    | mariadb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        339 |            0.74 |             4923.82 |           1051.33 |          -1 | mariadb-1-1-1-1-1    |
| monetdb-1-1-1-1-1    | MonetDB-1       | monetdb-1-1-1    | monetdb-1-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         17 |            0.04 |           100748.75 |          20964.71 |          -1 | monetdb-1-1-1-1-1    |
| mysql-1-1-1-1-1      | MySQL-1         | mysql-1-1-1      | mysql-1-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        489 |            0.70 |             5215.27 |            728.83 |          -1 | mysql-1-1-1-1-1      |
| postgresql-1-1-1-1-1 | PostgreSQL-1    | postgresql-1-1-1 | postgresql-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        180 |            0.31 |            11901.53 |           1980.00 |          -1 | postgresql-1-1-1-1-1 |

#### Per Phase

|                  | phase            |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:-----------------|:-----------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| mariadb-1-1-1    | mariadb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        339 |            0.74 |             4923.82 |           1051.33 |          -1 |
| monetdb-1-1-1    | monetdb-1-1-1    |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |         17 |            0.04 |           100748.75 |          20964.71 |          -1 |
| mysql-1-1-1      | mysql-1-1-1      |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        489 |            0.70 |             5215.27 |            728.83 |          -1 |
| postgresql-1-1-1 | postgresql-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               99 |                  99 |        180 |            0.31 |            11901.53 |           1980.00 |          -1 |

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
| TPC-DS Q1     |               15.71 |              158.86 |            197.62 |                 170.50 |
| TPC-DS Q2     |             3981.12 |               53.29 |           3539.43 |                 322.88 |
| TPC-DS Q3     |               12.46 |               12.05 |             35.78 |                 246.75 |
| TPC-DS Q4     |            10104.53 |              342.64 |          51482.47 |                6639.13 |
| TPC-DS Q5     |             9273.21 |               49.33 |          16253.15 |                 370.50 |
| TPC-DS Q6     |              584.51 |               26.59 |          62857.27 |               65443.20 |
| TPC-DS Q7     |             3452.69 |               32.92 |           1754.30 |                 329.58 |
| TPC-DS Q8     |              308.75 |               40.89 |            316.85 |                  61.19 |
| TPC-DS Q9     |             3578.81 |               40.28 |           4214.68 |                2773.55 |
| TPC-DS Q10    |               58.46 |               23.29 |            295.42 |                1086.88 |
| TPC-DS Q11    |             6693.94 |              398.59 |          26564.06 |                3952.04 |
| TPC-DS Q12    |              206.54 |               16.58 |            240.49 |                  55.98 |
| TPC-DS Q13    |              774.18 |               36.26 |           1938.93 |                 517.99 |
| TPC-DS Q14a+b |            50670.07 |              898.35 |          36160.62 |                1563.59 |
| TPC-DS Q15    |              138.20 |                9.94 |            162.44 |                  88.81 |
| TPC-DS Q16    |             9950.05 |               20.60 |            379.68 |                 155.92 |
| TPC-DS Q17    |              596.00 |               56.97 |           1025.14 |                 235.32 |
| TPC-DS Q18    |             2438.47 |               47.83 |           1196.80 |                 397.15 |
| TPC-DS Q19    |              177.37 |               19.06 |            307.91 |                 123.65 |
| TPC-DS Q20    |              329.93 |               12.19 |            408.64 |                 197.94 |
| TPC-DS Q21    |             3529.87 |               62.48 |           1826.96 |                 286.47 |
| TPC-DS Q22    |             9180.91 |              355.14 |           6272.58 |                2644.35 |
| TPC-DS Q23a+b |            51118.25 |              819.56 |          52292.89 |                4927.96 |
| TPC-DS Q24a+b |               23.67 |               84.68 |              6.73 |                  43.17 |
| TPC-DS Q25    |              100.60 |               57.40 |            181.08 |                 251.74 |
| TPC-DS Q26    |              605.34 |                9.30 |            516.58 |                 211.27 |
| TPC-DS Q27    |             2448.00 |               48.39 |            593.49 |                 314.46 |
| TPC-DS Q28    |             2529.64 |               30.19 |           4180.76 |                 595.62 |
| TPC-DS Q29    |               44.70 |               53.52 |             74.58 |                 249.06 |
| TPC-DS Q30    |               31.19 |               13.07 |             81.36 |                 817.05 |
| TPC-DS Q31    |              995.59 |               49.67 |          14233.84 |                1837.44 |
| TPC-DS Q32    |                6.14 |               14.02 |            143.50 |                  95.21 |
| TPC-DS Q33    |              135.06 |               14.52 |            576.21 |                 299.70 |
| TPC-DS Q34    |             2721.48 |               16.81 |            971.67 |                  22.60 |
| TPC-DS Q35    |              877.48 |               41.36 |          12358.20 |                 992.68 |
| TPC-DS Q36    |             2216.57 |               57.72 |           2591.92 |                 320.88 |
| TPC-DS Q37    |             2936.60 |               40.34 |             16.02 |                 192.13 |
| TPC-DS Q38    |             6287.24 |               65.40 |           6885.72 |                 854.68 |
| TPC-DS Q39a+b |              988.16 |             1026.28 |           1104.01 |                2525.55 |
| TPC-DS Q40    |              141.11 |               28.19 |            129.41 |                 106.32 |
| TPC-DS Q41    |              950.14 |                4.78 |           1084.03 |                 845.84 |
| TPC-DS Q42    |              245.28 |               13.10 |             71.17 |                  66.73 |
| TPC-DS Q43    |              810.00 |               22.15 |              9.74 |                  22.88 |
| TPC-DS Q44    |             1102.44 |               34.04 |           1862.12 |                 332.01 |
| TPC-DS Q45    |              120.28 |                8.19 |             97.17 |                  74.82 |
| TPC-DS Q46    |             2709.90 |               19.68 |            946.04 |                  30.89 |
| TPC-DS Q47    |            13063.19 |               87.73 |           7805.31 |                2056.39 |
| TPC-DS Q48    |              853.24 |               24.30 |            927.52 |                 534.33 |
| TPC-DS Q49    |              105.20 |               42.45 |            112.66 |                 348.20 |
| TPC-DS Q50    |               21.63 |               45.50 |             24.77 |                 433.06 |
| TPC-DS Q51    |             6885.97 |              153.42 |           7593.59 |                 810.09 |
| TPC-DS Q52    |              262.60 |               11.25 |             20.53 |                  64.96 |
| TPC-DS Q53    |              151.70 |               14.58 |            169.54 |                  81.17 |
| TPC-DS Q54    |              988.62 |              188.67 |           2437.91 |                  67.66 |
| TPC-DS Q55    |              164.78 |                9.15 |             12.94 |                  66.98 |
| TPC-DS Q56    |              127.78 |               10.78 |            182.24 |                 307.47 |
| TPC-DS Q57    |             4791.77 |               32.94 |           2548.57 |                1093.60 |
| TPC-DS Q58    |             5565.69 |               15.18 |           5577.65 |                 282.55 |
| TPC-DS Q59    |             8687.18 |               50.23 |           4421.85 |                 369.97 |
| TPC-DS Q60    |              277.12 |               12.37 |            306.65 |                 334.95 |
| TPC-DS Q61    |              276.08 |               16.10 |              2.37 |                 111.76 |
| TPC-DS Q62    |             1495.41 |               12.71 |           3471.02 |                  79.17 |
| TPC-DS Q63    |              270.24 |               14.94 |            180.44 |                  82.03 |
| TPC-DS Q64    |             1086.93 |              120.21 |            314.10 |                 545.65 |
| TPC-DS Q65    |             5338.74 |               29.53 |           5414.62 |                 453.77 |
| TPC-DS Q66    |             1099.02 |               21.39 |           1844.25 |                 313.98 |
| TPC-DS Q67    |             6096.94 |              125.87 |           7043.32 |                2872.70 |
| TPC-DS Q68    |             2700.47 |               34.52 |            248.21 |                  29.98 |
| TPC-DS Q69    |                2.04 |                8.18 |              3.19 |                  95.17 |
| TPC-DS Q70    |             6113.41 |               30.52 |           9901.53 |                 304.16 |
| TPC-DS Q71    |              410.63 |               14.81 |            412.00 |                 393.55 |
| TPC-DS Q72    |              641.45 |               98.57 |           8967.76 |                 969.91 |
| TPC-DS Q73    |             2167.50 |               17.00 |            213.69 |                  22.59 |
| TPC-DS Q74    |             5365.64 |               57.43 |           7650.60 |                 878.91 |
| TPC-DS Q75    |             5438.40 |              177.31 |           1860.57 |                 728.57 |
| TPC-DS Q76    |              852.82 |               21.24 |            409.59 |                 120.18 |
| TPC-DS Q77    |             5914.83 |               20.34 |           8635.90 |                 261.08 |
| TPC-DS Q78    |             4215.16 |              259.95 |          16112.44 |                2219.18 |
| TPC-DS Q79    |             2600.76 |               25.54 |           3766.14 |                 142.86 |
| TPC-DS Q80    |              416.15 |              172.87 |           8662.73 |                 328.97 |
| TPC-DS Q81    |              156.90 |               16.36 |           1780.81 |               37426.92 |
| TPC-DS Q82    |             3274.36 |               53.64 |              7.94 |                 235.66 |
| TPC-DS Q83    |             1032.02 |               10.84 |            619.03 |                  67.78 |
| TPC-DS Q84    |               46.16 |               23.34 |             59.73 |                  21.36 |
| TPC-DS Q85    |              193.79 |               78.99 |             83.87 |                 252.97 |
| TPC-DS Q86    |              657.58 |               24.53 |            909.55 |                 149.32 |
| TPC-DS Q87    |             6343.37 |              161.35 |           5865.20 |                 840.50 |
| TPC-DS Q88    |             8105.92 |               55.01 |           1867.24 |                2829.95 |
| TPC-DS Q89    |             1020.03 |               21.80 |              7.54 |                  23.16 |
| TPC-DS Q90    |              121.67 |               10.12 |            308.43 |                  93.83 |
| TPC-DS Q91    |               18.73 |               13.30 |             12.61 |                 151.08 |
| TPC-DS Q92    |                5.09 |                8.82 |             52.39 |                  71.12 |
| TPC-DS Q93    |               35.61 |               42.37 |             36.29 |                 199.70 |
| TPC-DS Q94    |              379.84 |               10.12 |            383.66 |                 139.11 |
| TPC-DS Q95    |              578.72 |               97.49 |           3188.02 |                3043.83 |
| TPC-DS Q96    |              559.07 |                6.46 |            139.04 |                  71.90 |
| TPC-DS Q97    |             4216.73 |               75.21 |           6422.60 |                 426.99 |
| TPC-DS Q98    |              723.45 |               19.96 |            810.87 |                 131.00 |
| TPC-DS Q99    |             2738.94 |               23.33 |          10328.17 |                 109.35 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

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
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>
