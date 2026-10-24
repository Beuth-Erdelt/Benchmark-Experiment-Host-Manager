#!/bin/bash
# Checks the load durability scripts (-xld durable|relaxed|unsafe) on the cluster
# (dev/plan-oltp-storage-dbms.md, WP10).
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
# Small runs (SF 1, one client round): the point is the loading phase.
#
# -xld sets the durability during the load only; afterwards the configured state (template, --set)
# is restored. The templates set no durability options (DBMS defaults, crash-safe).
# The placeholders durability.sql / restoredurability.sql of the cluster config's init script
# lists become (missing files are not run; .* = .sql, then .sh):
#   durable: durability-durable.*                             ... restoredurability-durable.*
#   relaxed: durability-relaxed.*                             ... restoredurability-relaxed.*
#   unsafe:  durability-relaxed.*, durability-unsafe.*        ... restoredurability-unsafe.*,
#                                                                restoredurability-relaxed.*
#
# What to check per log:
#   - "load durability <level>, scripts [...]" lists exactly the scripts of the level
#     the DBMS folder has (none for TiDB; Citus unsafe = relaxed scripts only)
#   - summary: "load_durability: <level>" per configuration
#   - result folder: bexhoma-loading-<config>-durability-*.stdout/.stderr logs
#     (pre-load) and -restoredurability-*.* logs (post-load), no errors in .stderr
#     except documented NOTICEs / the mysql password warning
#   - the durability-* stdout logs show the values during the load, the restore and checkschema
#     logs the configured values again:
#       PostgreSQL family: relaxed synchronous_commit off -> on; unsafe also fsync and
#                          full_page_writes off -> on, CHECKPOINT, "sync after fsync=off ... done"
#                          (PGBouncer included: its template no longer fixes synchronous_commit)
#       MySQL:             relaxed flush 2 (TPC-C/YCSB 0, log buffer 1G), key checks (TPC-H also
#                          autocommit) 0 -> 1/1/1; unsafe: Innodb_redo_log_enabled OFF -> ON,
#                          doublewrite DETECT_ONLY -> ON; bexhoma.saved_settings empty afterwards
#       MariaDB:           .sh as root: relaxed flush 2 -> 1; unsafe also doublewrite OFF -> ON
#       Citus:             synchronous_commit off on coordinator and every worker -> on again
#   - durable with --set (TPC-H MySQL): flush 1 during the load, back to the --set value 2
#     (initconstraints adds the FKs with foreign_key_checks=0; before, durable was OOM-killed there)
#   - -tr passes, no SUT restarts
#   - loading times: relaxed < durable expected; unsafe <= relaxed
#   - TPC-H PostgreSQL unsafe on -rst with -nc 2: repetition 2 finds the loaded volume
#     (no durability scripts, loading inherited) and the data is complete
#   - TPC-H PostgreSQL with schema tenancy: the scripts run once per tenant, restore after all
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




###########################################
################## TPC-H ##################
###########################################


#### TPC-H Durability PostgreSQL durable
# -dbms PostgreSQL              synchronous_commit, fsync, full_page_writes on (= template): baseline loading time
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld durable                  load durability: crash-safe load
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PostgreSQL durable"


#### TPC-H Durability PostgreSQL relaxed
# -dbms PostgreSQL              synchronous_commit off during the load
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PostgreSQL relaxed"


#### TPC-H Durability PostgreSQL unsafe
# -dbms PostgreSQL              also fsync and full_page_writes off; restore with CHECKPOINT and sync
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PostgreSQL unsafe"


#### TPC-H Durability PostgreSQL unsafe on persistent storage
# -dbms PostgreSQL              sync must reach the volume; repetition 2 reuses it
# -sf 1                         scaling factor
# -nc 2                         repetition 2 proves the data survives (no durability scripts there)
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          remove an existing volume first, so the load runs
# -rss 10Gi                     volume size
# -rst $BEXHOMA_STORAGE_CLASS   storage class
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PostgreSQL unsafe on storage"


#### TPC-H Durability PostgreSQL relaxed with schema tenancy
# -dbms PostgreSQL              durability scripts once per tenant, restore after all tenants
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -mtb schema                   one schema per tenant
# -mtn 2                        number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PostgreSQL schema tenancy"


#### TPC-H Durability PgDuckDB unsafe
# -dbms PgDuckDB                PostgreSQL scripts (path PostgreSQL)
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability PgDuckDB unsafe"


#### TPC-H Durability MySQL durable
# -dbms MySQL                   flush 1 during the load, back to the --set value 2 afterwards
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld durable                  load durability: crash-safe load
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_flush_log_at_trx_commit=2 relaxed benchmark, visible in the command
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G same pool as the -xld comparison 1792540834/1792542350 (template: 8G)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability MySQL durable"


#### TPC-H Durability MySQL relaxed
# -dbms MySQL                   flush 2, key checks and autocommit off (TPC-H variant)
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability MySQL relaxed"


#### TPC-H Durability MySQL unsafe
# -dbms MySQL                   also InnoDB redo log off during the load
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability MySQL unsafe"


#### TPC-H Durability MariaDB relaxed
# -dbms MariaDB                 durability-relaxed.sh as root: flush 2 during the load
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability MariaDB relaxed"


#### TPC-H Durability Citus unsafe
# -dbms Citus                   only the relaxed scripts exist: coordinator and workers
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nw 3                         number of worker nodes
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H durability Citus unsafe"




###########################################
################# TPC-DS ##################
###########################################


#### TPC-DS Durability PostgreSQL relaxed
# -dbms PostgreSQL              synchronous_commit off during the load
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS durability PostgreSQL relaxed"


#### TPC-DS Durability MySQL relaxed
# -dbms MySQL                   flush 2, key checks off (reference MySQL variant)
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS durability MySQL relaxed"


#### TPC-DS Durability MySQL unsafe
# -dbms MySQL                   also InnoDB redo log off during the load
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS durability MySQL unsafe"




###########################################
################## YCSB ###################
###########################################


#### YCSB Durability PostgreSQL relaxed
# -dbms PostgreSQL              new: synchronous_commit off during the load
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability PostgreSQL relaxed"


#### YCSB Durability PGBouncer unsafe
# -dbms PGBouncer               PostgreSQL scripts in the dbms container behind the pooler
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability PGBouncer unsafe"


#### YCSB Durability MySQL relaxed
# -dbms MySQL                   flush 0 and 1G log buffer (YCSB variant)
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability MySQL relaxed"


#### YCSB Durability MySQL unsafe
# -dbms MySQL                   also InnoDB redo log off during the load
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability MySQL unsafe"


#### YCSB Durability Citus relaxed
# -dbms Citus                   new: synchronous_commit off on coordinator and workers
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 1                        replication factor
# -nws 48                       number of shards
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability Citus relaxed"


#### YCSB Durability TiDB relaxed
# -dbms TiDB                    no durability scripts: loads as configured, scripts []
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnsr 3                       number of TiDB SUT replicas
# -nw 3                         number of worker nodes
# -nwr 3                        replication factor
# -xop 1                        number of operations for the benchmark phase (in millions)
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -xnpd 3                       number of PD nodes
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB durability TiDB relaxed"




###########################################
################ HammerDB #################
###########################################


#### HammerDB Durability PostgreSQL relaxed
# -dbms PostgreSQL              new: synchronous_commit off during the build
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB durability PostgreSQL relaxed"


#### HammerDB Durability MySQL relaxed
# -dbms MySQL                   flush 0 and 1G log buffer (TPC-C variant)
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB durability MySQL relaxed"


#### HammerDB Durability MySQL unsafe
# -dbms MySQL                   also InnoDB redo log off during the build
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB durability MySQL unsafe"


#### HammerDB Durability Citus relaxed
# -dbms Citus                   new: synchronous_commit off on coordinator and workers
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -nw 3                         number of worker nodes
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB durability Citus relaxed"




###########################################
################ Benchbase ################
###########################################


#### Benchbase Durability TPC-C PostgreSQL relaxed
# -dbms PostgreSQL              new: synchronous_commit off during the load
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability TPC-C PostgreSQL relaxed"


#### Benchbase Durability TPC-C PGBouncer relaxed
# -dbms PGBouncer               PostgreSQL scripts in the dbms container behind the pooler
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xnpp 1                       number of PGBouncer proxy pods
# -xnpi 128                     maximum incoming connections per PGBouncer instance (default: loading threads = 1)
# -xnpo 64                      maximum outgoing connections per PGBouncer instance
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability TPC-C PGBouncer relaxed"


#### Benchbase Durability TPC-C MySQL relaxed
# -dbms MySQL                   new: flush 2, key checks off (reference MySQL variant)
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability TPC-C MySQL relaxed"


#### Benchbase Durability TPC-C MySQL unsafe
# -dbms MySQL                   also InnoDB redo log off during the load
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability TPC-C MySQL unsafe"


#### Benchbase Durability TPC-C Citus relaxed
# -dbms Citus                   new: synchronous_commit off on coordinator and workers
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 1                        replication factor
# -nws 48                       number of shards
# -xld relaxed                  load durability (default)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability TPC-C Citus relaxed"


#### Benchbase Durability Twitter PostgreSQL unsafe
# -dbms PostgreSQL              scripts of a Benchbase benchmark other than tpcc
# -sf 4                         scaling factor
# -xbt twitter                  Benchbase benchmark
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         one client round
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xld unsafe                   load durability
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase durability Twitter PostgreSQL unsafe"




###########################################
############## Clean Folder ###############
###########################################


clean_logs
