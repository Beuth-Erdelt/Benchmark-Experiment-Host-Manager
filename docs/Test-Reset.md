# Test: Reset Scripts

This page shows how to use `-ar` (reset scripts) and keeps the test script and the logs of its last run on the cluster.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These runs are solely to check that the feature works and to illustrate how to use bexhoma.**

References:
1. Steps and scripts per DBMS: [Reset scripts (`-ar`)](DBMS.md#reset-scripts--ar)
1. Test script: [test-docs-reset.sh](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-reset.sh), [test-docs-reset.ps1](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-reset.ps1)


## Reset Scripts

With `-ar`, a reset runs before each benchmarking round, also before the first round right after loading.
It is off by default and available for YCSB, Benchbase, HammerDB, TPC-H and TPC-DS.
Every reset does the same steps in the same order, so rounds and systems start from comparable states:

1. **Statistics**: `VACUUM` / `ANALYZE` or the equivalent
1. **Persist**: write dirty data to disk (`CHECKPOINT`, flush, `SAVE`), so that no checkpoint or flush left over from loading or the previous round falls into the measured round
1. **Counters**: zero the cumulative activity counters, so application metrics start at 0

The reset does not make caches cold.
A step without an equivalent in a DBMS is skipped; [DBMS](DBMS.md#reset-scripts--ar) lists what each DBMS does.

Example:
```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -ne 1,2 \
  -ar \
  run
```

This loads YCSB data into PostgreSQL and runs two benchmarking rounds (one and two benchmarker pods).
Before each round, `VACUUM ANALYZE`, `CHECKPOINT` and `pg_stat_reset()` run.

Each reset is logged per round in the result folder (`bexhoma-reset_<run>_<client>_<entry>-...log`).
The summary has a Reset table with the duration (`time_reset`) and the failed scripts (`reset_failed`) per round, and the test `Reset scripts ran without errors`.
With a TPC-H refresh stream (`-xrs`), the reset runs once per round, before both streams start.
With `-ar` on a configuration without reset scripts, the experiment prints a warning at the start.


## Test Script

The test script runs one experiment per DBMS and benchmark with two client rounds, so every reset script runs twice, the first time right after loading.
It covers PostgreSQL, PGBouncer, PgDuckDB, MySQL, MariaDB, Citus, MonetDB, CockroachDB, TiDB, YugabyteDB, Dragonfly (standalone, replica) and Redis (standalone, cluster) in the benchmarks that have reset scripts for them, Benchbase `twitter` in addition to `tpcc`, and TPC-H with a refresh stream.

You will have to change the node selectors (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1

mkdir -p $LOG_DIR
```

Run the script from the repository root:
```bash
bash scripts/test-docs-reset.sh
```
or in PowerShell
```powershell
.\scripts\test-docs-reset.ps1
```

What to check per log:
* one reset log pair per round, no errors in the `.stderr` logs except documented NOTICEs (psql VERBOSE, mariadb password warning)
* `reset (reset_x_y_z) completed in Ns` in the log, `time_reset` in the summary
* no warning about missing reset scripts at the start
* step 2 visible: `CHECKPOINT` (PostgreSQL family), `run_command_on_workers` with `success = t` for every worker (Citus), `dirty pages: 0` from `reset-flush.sh` (MySQL, MariaDB), `SAVE` returns `OK` on every data pod (Dragonfly, Redis)
* step 3 visible: `counters reset on 3 tservers` (YugabyteDB), `FLUSH STATUS` without error (TiDB), `CONFIG RESETSTAT` returns `OK` (Dragonfly, Redis)
* TPC-H with `-xrs`: one reset per round, none for the refresh stream

The last run used bexhoma 0.11.7 (2026-10-21 and 2026-10-22).
All runs passed their tests, except TPC-DS MariaDB, where Q94 and Q95 exceeded the query timeout (`-t 1200`); its resets ran without errors.


## YCSB


### PostgreSQL

VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*.

```bash
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_postgresql.log" target="_blank" rel="noopener">docs_reset_ycsb_postgresql.log</a>


### PGBouncer

Reset of PostgreSQL, through the pooler.

```bash
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnpp 1 \
  -xnpi 128 \
  -xnpo 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_pgbouncer.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_pgbouncer_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_pgbouncer.log" target="_blank" rel="noopener">docs_reset_ycsb_pgbouncer.log</a>


### MySQL

ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS).

```bash
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_mysql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mysql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mysql.log" target="_blank" rel="noopener">docs_reset_ycsb_mysql.log</a>


### MariaDB

ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS).

```bash
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_mariadb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mariadb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_mariadb.log" target="_blank" rel="noopener">docs_reset_ycsb_mariadb.log</a>


### Citus

CHECKPOINT and pg_stat_reset* on coordinator and every worker.

```bash
bexhoma ycsb \
  -dbms Citus \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_citus.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_citus_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_citus.log" target="_blank" rel="noopener">docs_reset_ycsb_citus.log</a>


### CockroachDB

ANALYZE, crdb_internal.reset_sql_stats(), persist n/a.

```bash
bexhoma ycsb \
  -dbms CockroachDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_cockroachdb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_cockroachdb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_cockroachdb.log" target="_blank" rel="noopener">docs_reset_ycsb_cockroachdb.log</a>


### TiDB

ANALYZE TABLE, FLUSH STATUS, persist n/a.

```bash
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -xnpd 3 \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_tidb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_tidb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_tidb.log" target="_blank" rel="noopener">docs_reset_ycsb_tidb.log</a>


### Dragonfly

SAVE and CONFIG RESETSTAT in the SUT pod.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_dragonfly.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly.log" target="_blank" rel="noopener">docs_reset_ycsb_dragonfly.log</a>


### Dragonfly Replica

SAVE and CONFIG RESETSTAT on every worker.

```bash
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_dragonfly_replica.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly_replica_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_dragonfly_replica.log" target="_blank" rel="noopener">docs_reset_ycsb_dragonfly_replica.log</a>


### Redis

SAVE and CONFIG RESETSTAT in the SUT pod.

```bash
bexhoma ycsb \
  -dbms Redis \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_redis.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis.log" target="_blank" rel="noopener">docs_reset_ycsb_redis.log</a>


### Redis Cluster

SAVE and CONFIG RESETSTAT on every cluster node.

```bash
bexhoma ycsb \
  -dbms Redis \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_redis_cluster.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis_cluster_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_redis_cluster.log" target="_blank" rel="noopener">docs_reset_ycsb_redis_cluster.log</a>


### YugabyteDB

ANALYZE, reset-counters.sh on every tserver, persist n/a.

YugabyteDB is installed with Helm before the run and removed afterwards, see [YugabyteDB](Example-YugaByteDB.md).

```bash
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 4 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_yugabytedb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_yugabytedb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_ycsb_yugabytedb.log" target="_blank" rel="noopener">docs_reset_ycsb_yugabytedb.log</a>


## Benchbase


### TPC-C PostgreSQL

VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_postgresql.log" target="_blank" rel="noopener">docs_reset_benchbase_postgresql.log</a>


### TPC-C PGBouncer

Reset of PostgreSQL, through the pooler.

```bash
bexhoma benchbase \
  -dbms PGBouncer \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -xnpp 1 \
  -xnpi 128 \
  -xnpo 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_pgbouncer.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_pgbouncer_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_pgbouncer.log" target="_blank" rel="noopener">docs_reset_benchbase_pgbouncer.log</a>


### TPC-C MySQL

ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS).

```bash
bexhoma benchbase \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_mysql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mysql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mysql.log" target="_blank" rel="noopener">docs_reset_benchbase_mysql.log</a>


### TPC-C MariaDB

ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS).

```bash
bexhoma benchbase \
  -dbms MariaDB \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_mariadb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mariadb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_mariadb.log" target="_blank" rel="noopener">docs_reset_benchbase_mariadb.log</a>


### Twitter PostgreSQL

Reset for a Benchbase benchmark other than tpcc.

```bash
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xbt twitter \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_twitter_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_twitter_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_twitter_postgresql.log" target="_blank" rel="noopener">docs_reset_benchbase_twitter_postgresql.log</a>


### TPC-C Citus

CHECKPOINT and pg_stat_reset* on coordinator and every worker.

```bash
bexhoma benchbase \
  -dbms Citus \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_citus.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_citus_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_citus.log" target="_blank" rel="noopener">docs_reset_benchbase_citus.log</a>


### TPC-C CockroachDB

ANALYZE, crdb_internal.reset_sql_stats(), persist n/a.

```bash
bexhoma benchbase \
  -dbms CockroachDB \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -nw 3 \
  -nwr 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_cockroachdb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_cockroachdb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_cockroachdb.log" target="_blank" rel="noopener">docs_reset_benchbase_cockroachdb.log</a>


### TPC-C TiDB

ANALYZE TABLE benchbase.*, FLUSH STATUS, persist n/a.

```bash
bexhoma benchbase \
  -dbms TiDB \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -xnpd 3 \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_tidb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_tidb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_tidb.log" target="_blank" rel="noopener">docs_reset_benchbase_tidb.log</a>


### TPC-C YugabyteDB

ANALYZE, reset-counters.sh on every tserver, persist n/a.

YugabyteDB is installed with Helm before the run and removed afterwards, see [YugabyteDB](Example-YugaByteDB.md).

```bash
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1,2 \
  -nbp 1 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_benchbase_yugabytedb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_yugabytedb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_benchbase_yugabytedb.log" target="_blank" rel="noopener">docs_reset_benchbase_yugabytedb.log</a>


## HammerDB


### PostgreSQL

VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* in database tpcc.

```bash
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1,2 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_hammerdb_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_postgresql.log" target="_blank" rel="noopener">docs_reset_hammerdb_postgresql.log</a>


### MySQL

ANALYZE TABLE in database tpcc, then reset-flush.sh.

```bash
bexhoma hammerdb \
  -dbms MySQL \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1,2 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_hammerdb_mysql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mysql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mysql.log" target="_blank" rel="noopener">docs_reset_hammerdb_mysql.log</a>


### MariaDB

ANALYZE TABLE in database tpcc, then reset-flush.sh.

```bash
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1,2 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_hammerdb_mariadb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mariadb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_mariadb.log" target="_blank" rel="noopener">docs_reset_hammerdb_mariadb.log</a>


### Citus

CHECKPOINT and pg_stat_reset* on coordinator and every worker.

```bash
bexhoma hammerdb \
  -dbms Citus \
  -sf 4 \
  -xsd 2 \
  -nc 1 \
  -ne 1,2 \
  -nlt 4 \
  -nbp 1 \
  -nbt 4 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_hammerdb_citus.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_citus_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_hammerdb_citus.log" target="_blank" rel="noopener">docs_reset_hammerdb_citus.log</a>


## TPC-H


### PostgreSQL

VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_postgresql.log" target="_blank" rel="noopener">docs_reset_tpch_postgresql.log</a>


### PgDuckDB

Reset of PostgreSQL.

```bash
bexhoma tpch \
  -dbms PgDuckDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_pgduckdb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_pgduckdb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_pgduckdb.log" target="_blank" rel="noopener">docs_reset_tpch_pgduckdb.log</a>


### MonetDB

ANALYZE, persist n/a, counters n/a.

```bash
bexhoma tpch \
  -dbms MonetDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_monetdb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_monetdb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_monetdb.log" target="_blank" rel="noopener">docs_reset_tpch_monetdb.log</a>


### MySQL

ANALYZE TABLE tpch.*, then reset-flush.sh.

```bash
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_mysql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mysql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mysql.log" target="_blank" rel="noopener">docs_reset_tpch_mysql.log</a>


### MariaDB

ANALYZE TABLE tpch.*, then reset-flush.sh.

```bash
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_mariadb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mariadb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_mariadb.log" target="_blank" rel="noopener">docs_reset_tpch_mariadb.log</a>


### Citus

CHECKPOINT and pg_stat_reset* on coordinator and every worker.

```bash
bexhoma tpch \
  -dbms Citus \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_citus.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_citus_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_citus.log" target="_blank" rel="noopener">docs_reset_tpch_citus.log</a>


### PostgreSQL with Refresh Stream

One reset per round, before both streams.

```bash
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xrs 1 \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_refresh_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_refresh_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpch_refresh_postgresql.log" target="_blank" rel="noopener">docs_reset_tpch_refresh_postgresql.log</a>


## TPC-DS


### PostgreSQL

VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*.

```bash
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpcds_postgresql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_postgresql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_postgresql.log" target="_blank" rel="noopener">docs_reset_tpcds_postgresql.log</a>


### MonetDB

ANALYZE, persist n/a, counters n/a.

```bash
bexhoma tpcds \
  -dbms MonetDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpcds_monetdb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_monetdb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_monetdb.log" target="_blank" rel="noopener">docs_reset_tpcds_monetdb.log</a>


### MySQL

ANALYZE TABLE tpcds.*, then reset-flush.sh.

```bash
bexhoma tpcds \
  -dbms MySQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpcds_mysql.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mysql_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mysql.log" target="_blank" rel="noopener">docs_reset_tpcds_mysql.log</a>


### MariaDB

ANALYZE TABLE tpcds.*, then reset-flush.sh.

```bash
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpcds_mariadb.log
```

Result: <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mariadb_summary.md" target="_blank" rel="noopener">summary</a>, <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_reset_tpcds_mariadb.log" target="_blank" rel="noopener">docs_reset_tpcds_mariadb.log</a>
