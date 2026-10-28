# Test: Load Durability

This page shows how to use `-xld` (load durability) and keeps the test script and the logs of its last run on the cluster.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These runs are solely to check that the feature works and to illustrate how to use bexhoma.**

References:
1. Durability during the load: [Prepare Testbeds](Prepare-Testbeds.md#durability-during-the-load)
1. Settings per DBMS: [Load durability (`-xld`)](DBMS.md#load-durability--xld)
1. Test script: [test-docs-durability.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-durability.sh), [test-docs-durability.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-durability.ps1)


## Load Durability

`-xld durable|relaxed|unsafe` sets how much durability the DBMS gives up while data is loaded:

* `durable`: crash-safe, e.g. PostgreSQL `synchronous_commit`, `fsync` and `full_page_writes` on, MySQL `innodb_flush_log_at_trx_commit=1`
* `relaxed` (default): commits do not wait for the log flush, key checks are skipped, e.g. PostgreSQL `synchronous_commit=off`
* `unsafe`: the strongest lever of the DBMS, e.g. PostgreSQL `fsync=off`, MySQL redo log off; a crash during the load can corrupt the data

The level applies to the load only.
Before the check script, the server returns to its configured state (template and `--set`), so the benchmark always runs as configured.
The summary shows the level in the workload (`Load durability is relaxed (-xld; restored after the load).`) and per connection (`load_durability: relaxed`).

Durability scripts exist for PostgreSQL (also used by PgDuckDB and PGBouncer), MySQL, MariaDB and Citus.
Other DBMS load as configured.
See [Prepare Testbeds](Prepare-Testbeds.md#durability-during-the-load) for how the scripts are selected and [DBMS](DBMS.md#load-durability--xld) for what they set per DBMS.

Example:
```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -xii -xic -xis \
  -xld unsafe \
  run
```

This loads TPC-H SF 1 into PostgreSQL with `fsync` and `full_page_writes` off, then switches them on again, runs `CHECKPOINT` and a `sync` and creates indexes, constraints and statistics before the queries run.


## Test Script

The test script runs one small experiment (SF 1, one client round) per benchmark, DBMS and level.
The point is the loading phase.
It covers TPC-H, TPC-DS, YCSB, HammerDB and Benchbase on PostgreSQL, PgDuckDB, PGBouncer, MySQL, MariaDB, Citus and TiDB (no durability scripts), and in addition
* `durable` with `--set` (MySQL): durable during the load, back to the `--set` value afterwards
* `unsafe` on persistent storage (`-rst`, `-nc 2`): repetition 2 finds the loaded volume and the data is complete
* schema tenancy (`-mtb schema`): the scripts run once per tenant, the restore after all tenants

You will have to change the node selectors (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

Run the script from the repository root:
```bash
bash scripts/test-docs-durability.sh
```
or in PowerShell
```powershell
.\scripts\test-docs-durability.ps1
```

What to check per log:
* `load durability <level>, scripts [...]` lists exactly the scripts of the level that the DBMS folder has (none for TiDB; Citus `unsafe` = `relaxed` scripts only)
* the summary shows `load_durability: <level>` per configuration
* the result folder has `bexhoma-loading-<config>-durability-*` logs (before the load) and `-restoredurability-*` logs (after the load), with no errors in `.stderr` except documented NOTICEs and the mysql password warning
* the `durability-*` stdout logs show the values during the load, the restore and checkschema logs show the configured values again
* `-tr` passes, no SUT restarts

The last run used bexhoma 0.11.7 (2026-10-21 and 2026-10-22).
All runs passed their tests.


## TPC-H


### PostgreSQL durable

Synchronous_commit, fsync, full_page_writes on (= template): baseline loading time.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld durable \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_postgresql_durable.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_postgresql_durable_summary.md" target="_blank" rel="noopener">docs_durability_tpch_postgresql_durable.log</a>


### PostgreSQL relaxed

Synchronous_commit off during the load.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_postgresql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_postgresql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_tpch_postgresql_relaxed.log</a>


### PostgreSQL unsafe

Also fsync and full_page_writes off; restore with CHECKPOINT and sync.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_postgresql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_postgresql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_tpch_postgresql_unsafe.log</a>


### PostgreSQL unsafe on persistent storage

Sync must reach the volume; repetition 2 reuses it.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_postgresql_unsafe_storage.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_postgresql_unsafe_storage_summary.md" target="_blank" rel="noopener">docs_durability_tpch_postgresql_unsafe_storage.log</a>


### PostgreSQL relaxed with schema tenancy

Durability scripts once per tenant, restore after all tenants.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -mtb schema \
  -mtn 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_postgresql_tenants_schema.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_postgresql_tenants_schema_summary.md" target="_blank" rel="noopener">docs_durability_tpch_postgresql_tenants_schema.log</a>


### PgDuckDB unsafe

PostgreSQL scripts (path PostgreSQL).

```bash
bexhoma tpch \
  -dbms PgDuckDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_pgduckdb_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_pgduckdb_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_tpch_pgduckdb_unsafe.log</a>


### MySQL durable

Flush 1 during the load, back to the --set value 2 afterwards.

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld durable \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_flush_log_at_trx_commit=2 \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_mysql_durable.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_durable_summary.md" target="_blank" rel="noopener">docs_durability_tpch_mysql_durable.log</a>


### MySQL relaxed

Flush 2, key checks and autocommit off (TPC-H variant).

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_mysql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_tpch_mysql_relaxed.log</a>


### MySQL unsafe

Also InnoDB redo log off during the load.

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_mysql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mysql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_tpch_mysql_unsafe.log</a>


### MariaDB relaxed

Durability-relaxed.sh as root: flush 2 during the load.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_mariadb_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_mariadb_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_tpch_mariadb_relaxed.log</a>


### Citus unsafe

Only the relaxed scripts exist: coordinator and workers.

```bash
bexhoma tpch \
  -dbms Citus \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nw 3 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpch_citus_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpch_citus_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_tpch_citus_unsafe.log</a>


## TPC-DS


### PostgreSQL relaxed

Synchronous_commit off during the load.

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpcds_postgresql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpcds_postgresql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_tpcds_postgresql_relaxed.log</a>


### MySQL relaxed

Flush 2, key checks off (reference MySQL variant).

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpcds_mysql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpcds_mysql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_tpcds_mysql_relaxed.log</a>


### MySQL unsafe

Also InnoDB redo log off during the load.

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_tpcds_mysql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_tpcds_mysql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_tpcds_mysql_unsafe.log</a>


## YCSB


### PostgreSQL relaxed

New: synchronous_commit off during the load.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_ycsb_postgresql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_postgresql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_postgresql_relaxed.log</a>


### PGBouncer unsafe

PostgreSQL scripts in the dbms container behind the pooler.

```bash
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_ycsb_pgbouncer_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_pgbouncer_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_pgbouncer_unsafe.log</a>


### MySQL relaxed

Flush 0 and 1G log buffer (YCSB variant).

```bash
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_ycsb_mysql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_mysql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_mysql_relaxed.log</a>


### MySQL unsafe

Also InnoDB redo log off during the load.

```bash
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_ycsb_mysql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_mysql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_mysql_unsafe.log</a>


### Citus relaxed

New: synchronous_commit off on coordinator and workers.

```bash
bexhoma ycsb \
  -dbms Citus \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 1 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_ycsb_citus_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_citus_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_citus_relaxed.log</a>


### TiDB relaxed

No durability scripts: loads as configured, scripts [].

```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -xnpd 3 \
  run &>$LOG_DIR/docs_durability_ycsb_tidb_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_ycsb_tidb_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_ycsb_tidb_relaxed.log</a>


## HammerDB


### PostgreSQL relaxed

New: synchronous_commit off during the build.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_hammerdb_postgresql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_postgresql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_hammerdb_postgresql_relaxed.log</a>


### MySQL relaxed

Flush 0 and 1G log buffer (TPC-C variant).

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_hammerdb_mysql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_mysql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_hammerdb_mysql_relaxed.log</a>


### MySQL unsafe

Also InnoDB redo log off during the build.

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_hammerdb_mysql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_mysql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_hammerdb_mysql_unsafe.log</a>


### Citus relaxed

New: synchronous_commit off on coordinator and workers.

```bash
bexhoma hammerdb \
  -dbms Citus \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -nw 3 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_hammerdb_citus_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_hammerdb_citus_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_hammerdb_citus_relaxed.log</a>


## Benchbase


### TPC-C PostgreSQL relaxed

New: synchronous_commit off during the load.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_postgresql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_postgresql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_postgresql_relaxed.log</a>


### TPC-C PGBouncer relaxed

PostgreSQL scripts in the dbms container behind the pooler.

```bash
bexhoma benchbase \
  -dbms PGBouncer \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -xnpp 1 \
  -xnpi 128 \
  -xnpo 64 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_pgbouncer_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_pgbouncer_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_pgbouncer_relaxed.log</a>


### TPC-C MySQL relaxed

New: flush 2, key checks off (reference MySQL variant).

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_mysql_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_mysql_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_mysql_relaxed.log</a>


### TPC-C MySQL unsafe

Also InnoDB redo log off during the load.

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_mysql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_mysql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_mysql_unsafe.log</a>


### TPC-C Citus relaxed

New: synchronous_commit off on coordinator and workers.

```bash
bexhoma benchbase \
  -dbms Citus \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xld relaxed \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_citus_relaxed.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_citus_relaxed_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_citus_relaxed.log</a>


### Twitter PostgreSQL unsafe

Scripts of a Benchbase benchmark other than tpcc.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xbt twitter \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 40 \
  -xld unsafe \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_durability_benchbase_twitter_postgresql_unsafe.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_durability_benchbase_twitter_postgresql_unsafe_summary.md" target="_blank" rel="noopener">docs_durability_benchbase_twitter_postgresql_unsafe.log</a>
