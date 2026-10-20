#!/bin/bash
# Checks the reset scripts (-ar) of every DBMS and benchmark on the cluster
# (dev/plan-reset-scripts.md, M11; contract in docs/DBMS.md "Reset scripts").
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
# Every run has two client rounds (-ne 1,2) with -ar, so every reset script
# runs twice, the first time right after loading.
#
# What to check per log (result folder: bexhoma-reset_<run>_<client>_<entry>-*):
#   - one reset log pair per round, no errors in the .stderr logs except
#     documented NOTICEs (psql VERBOSE, mariadb password warning)
#   - "reset (reset_x_y_z) completed in Ns" in the log, reset_seconds in the summary
#   - no WARNING about missing reset scripts at the start
#   - step 2 visible:
#       PostgreSQL family: CHECKPOINT with timing in the stdout log
#       Citus:             run_command_on_workers rows with success = t for every worker
#       MySQL/MariaDB:     reset-flush.sh ends with "dirty pages: 0", no "flush timeout";
#                          note the flush time (sets TIMEOUT, plan M0.3)
#       MonetDB:           CALL sys.flush_log() without error (M0.4)
#       Dragonfly/Redis:   SAVE returns OK on every data pod
#   - step 3 visible:
#       YugabyteDB:        "counters reset on 3 tservers"
#       TiDB:              FLUSH STATUS without error (M0.6)
#       Dragonfly:         CONFIG RESETSTAT returns OK (M0.7)
#   - TPC-H with -xrs: one reset per round (entry 1), none for the refresh stream (entry 2)
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh


# install_yugabytedb / remove_yugabytedb: as in test-docs-yugabytedb.sh (ephemeral, 3 tservers)
install_yugabytedb() {
  helm install bexhoma yugabytedb/yugabyte \
    --version 2025.2.7 \
    --set \
gflags.tserver.ysql_enable_packed_row=true,\
gflags.tserver.ysql_max_connections=1280,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=16Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=16Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=16Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=16Gi,\
storage.ephemeral=true,\
preflight.skipUlimit=true,\
enableLoadBalancer=true

  echo "Waiting 60s for pods to start..."
  sleep 60
}


remove_yugabytedb() {
  echo "Deleting Helm release bexhoma..."
  helm delete bexhoma
  echo "Waiting 60s for cleanup..."
  sleep 60
}



###########################################
################## YCSB ###################
###########################################


#### YCSB Reset PostgreSQL
# -dbms PostgreSQL              VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset PostgreSQL"


#### YCSB Reset PGBouncer
# -dbms PGBouncer               reset of PostgreSQL, through the pooler
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_ycsb_pgbouncer.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset PGBouncer"


#### YCSB Reset MySQL
# -dbms MySQL                   ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS)
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset MySQL"


#### YCSB Reset MariaDB
# -dbms MariaDB                 ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS)
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset MariaDB"


#### YCSB Reset Citus
# -dbms Citus                   CHECKPOINT and pg_stat_reset* on coordinator and every worker
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 1                        replication factor (Dragonfly: replica mode)
# -nws 48                       number of shards
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset Citus"


#### YCSB Reset CockroachDB
# -dbms CockroachDB             ANALYZE, crdb_internal.reset_sql_stats(), persist n/a
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 3                        replication factor (Dragonfly: replica mode)
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset CockroachDB"


#### YCSB Reset TiDB
# -dbms TiDB                    ANALYZE TABLE, FLUSH STATUS, persist n/a
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnsr 3                       number of TiDB SUT replicas
# -nw 3                         number of worker nodes
# -nwr 3                        replication factor (Dragonfly: replica mode)
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -xnpd 3                       number of PD nodes
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset TiDB"


#### YCSB Reset Dragonfly
# -dbms Dragonfly               SAVE and CONFIG RESETSTAT in the SUT pod
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset Dragonfly"


#### YCSB Reset Dragonfly Replica
# -dbms Dragonfly               SAVE and CONFIG RESETSTAT on every worker
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 1                        replication factor (Dragonfly: replica mode)
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset Dragonfly Replica"


#### YCSB Reset Redis
# -dbms Redis                   SAVE and CONFIG RESETSTAT in the SUT pod
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset Redis"


#### YCSB Reset Redis Cluster
# -dbms Redis                   SAVE and CONFIG RESETSTAT on every cluster node
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset Redis Cluster"


#### YCSB Reset YugabyteDB
install_yugabytedb

# -dbms YugabyteDB              ANALYZE, reset-counters.sh on every tserver, persist n/a
# -sf 1                         scaling factor
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB reset YugabyteDB"

remove_yugabytedb




###########################################
################ Benchbase ################
###########################################


#### Benchbase Reset TPC-C PostgreSQL
# -dbms PostgreSQL              VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C PostgreSQL"


#### Benchbase Reset TPC-C PGBouncer
# -dbms PGBouncer               reset of PostgreSQL, through the pooler
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xnpp 1                       number of PGBouncer proxy pods
# -xnpi 128                     maximum incoming connections per PGBouncer instance (default: loading threads = 1)
# -xnpo 64                      maximum outgoing connections per PGBouncer instance
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C PGBouncer"


#### Benchbase Reset TPC-C MySQL
# -dbms MySQL                   ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS)
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C MySQL"


#### Benchbase Reset TPC-C MariaDB
# -dbms MariaDB                 ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS)
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C MariaDB"


#### Benchbase Reset Twitter PostgreSQL
# -dbms PostgreSQL              reset for a Benchbase benchmark other than tpcc
# -sf 4                         scaling factor
# -xbt twitter                  Benchbase benchmark
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset Twitter PostgreSQL"


#### Benchbase Reset TPC-C Citus
# -dbms Citus                   CHECKPOINT and pg_stat_reset* on coordinator and every worker
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 1                        replication factor (Dragonfly: replica mode)
# -nws 48                       number of shards
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C Citus"


#### Benchbase Reset TPC-C CockroachDB
# -dbms CockroachDB             ANALYZE, crdb_internal.reset_sql_stats(), persist n/a
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -nw 3                         number of worker nodes
# -nwr 3                        replication factor (Dragonfly: replica mode)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C CockroachDB"


#### Benchbase Reset TPC-C TiDB
# -dbms TiDB                    ANALYZE TABLE benchbase.*, FLUSH STATUS, persist n/a
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -xnsr 3                       number of TiDB SUT replicas
# -nw 3                         number of worker nodes
# -nwr 3                        replication factor (Dragonfly: replica mode)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -xnpd 3                       number of PD nodes
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C TiDB"


#### Benchbase Reset TPC-C YugabyteDB
install_yugabytedb

# -dbms YugabyteDB              ANALYZE, reset-counters.sh on every tserver, persist n/a
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 1                       benchmarking throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase reset TPC-C YugabyteDB"

remove_yugabytedb




###########################################
################ HammerDB #################
###########################################


#### HammerDB Reset PostgreSQL
# -dbms PostgreSQL              VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* in database tpcc
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB reset PostgreSQL"


#### HammerDB Reset MySQL
# -dbms MySQL                   ANALYZE TABLE in database tpcc, then reset-flush.sh
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB reset MySQL"


#### HammerDB Reset MariaDB
# -dbms MariaDB                 ANALYZE TABLE in database tpcc, then reset-flush.sh
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB reset MariaDB"


#### HammerDB Reset Citus
# -dbms Citus                   CHECKPOINT and pg_stat_reset* on coordinator and every worker
# -sf 4                         scaling factor
# -xsd 2                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlt 4                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        threads per benchmarking pod
# -nw 3                         number of worker nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_hammerdb_citus.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB reset Citus"




###########################################
################## TPC-H ##################
###########################################


#### TPC-H Reset PostgreSQL
# -dbms PostgreSQL              VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset PostgreSQL"


#### TPC-H Reset PgDuckDB
# -dbms PgDuckDB                reset of PostgreSQL
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset PgDuckDB"


#### TPC-H Reset MonetDB
# -dbms MonetDB                 ANALYZE, CALL sys.flush_log(), counters n/a
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset MonetDB"


#### TPC-H Reset MySQL
# -dbms MySQL                   ANALYZE TABLE tpch.*, then reset-flush.sh
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset MySQL"


#### TPC-H Reset MariaDB
# -dbms MariaDB                 ANALYZE TABLE tpch.*, then reset-flush.sh
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset MariaDB"


#### TPC-H Reset Citus
# -dbms Citus                   CHECKPOINT and pg_stat_reset* on coordinator and every worker
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nw 3                         number of worker nodes
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
bexhoma tpch \
  -dbms Citus \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nw 3 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  run &>$LOG_DIR/docs_reset_tpch_citus.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset Citus"


#### TPC-H Reset PostgreSQL with Refresh Stream
# -dbms PostgreSQL              one reset per round, before both streams
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,1                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -xrs 1                        refresh stream in parallel -- one reset per round, none for the refresh stream
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H reset PostgreSQL with Refresh Stream"




###########################################
################# TPC-DS ##################
###########################################


#### TPC-DS Reset PostgreSQL
# -dbms PostgreSQL              VACUUM ANALYZE, CHECKPOINT, pg_stat_reset*
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS reset PostgreSQL"


#### TPC-DS Reset MonetDB
# -dbms MonetDB                 ANALYZE, CALL sys.flush_log(), counters n/a
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS reset MonetDB"


#### TPC-DS Reset MySQL
# -dbms MySQL                   ANALYZE TABLE tpcds.*, then reset-flush.sh
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS reset MySQL"


#### TPC-DS Reset MariaDB
# -dbms MariaDB                 ANALYZE TABLE tpcds.*, then reset-flush.sh
# -sf 1                         scaling factor
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       two client rounds -- the reset runs before each
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after loading
# -xic                          create constraints after loading
# -xis                          recompute statistics after loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       timeout per query in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           activate configured reset scripts before each round
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

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS reset MariaDB"




###########################################
############## Clean Folder ###############
###########################################


clean_logs
