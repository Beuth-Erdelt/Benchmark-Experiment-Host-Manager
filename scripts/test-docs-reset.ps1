#Requires -Version 5.1
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
#       MonetDB:           none (persist n/a, Dec2025 has no sys.flush_log())
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

. .\scripts\testfunctions.ps1


# Install-YugabyteDB / Remove-YugabyteDB: as in test-docs-yugabytedb.ps1 (ephemeral, 3 tservers)
function Install-YugabyteDB {
    $settings = "gflags.tserver.ysql_enable_packed_row=true,gflags.tserver.ysql_max_connections=1280,resource.master.limits.cpu=2,resource.master.limits.memory=16Gi,resource.master.requests.cpu=2,resource.master.requests.memory=16Gi,resource.tserver.limits.cpu=8,resource.tserver.limits.memory=16Gi,resource.tserver.requests.cpu=8,resource.tserver.requests.memory=16Gi,storage.ephemeral=true,preflight.skipUlimit=true,enableLoadBalancer=true"
    helm install bexhoma yugabytedb/yugabyte --version 2025.2.7 --set $settings

    Write-Host "Waiting 60s for pods to start..."
    Start-Sleep -Seconds 60
}

function Remove-YugabyteDB {
    Write-Host "Deleting Helm release bexhoma..."
    helm delete bexhoma
    Write-Host "Waiting 60s for cleanup..."
    Start-Sleep -Seconds 60
}



###########################################
################## YCSB ###################
###########################################


#### YCSB Reset PostgreSQL
bexhoma ycsb `
  -dbms PostgreSQL              <# VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset PostgreSQL"


#### YCSB Reset PGBouncer
bexhoma ycsb `
  -dbms PGBouncer               <# reset of PostgreSQL, through the pooler #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnpp 1                       <# number of PGBouncer proxy pods #> `
  -xnpi 128                     <# maximum incoming connections per PGBouncer instance (default: loading threads) #> `
  -xnpo 64                      <# maximum outgoing connections per PGBouncer instance #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_pgbouncer.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset PGBouncer"


#### YCSB Reset MySQL
bexhoma ycsb `
  -dbms MySQL                   <# ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS) #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_mysql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset MySQL"


#### YCSB Reset MariaDB
bexhoma ycsb `
  -dbms MariaDB                 <# ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS) #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset MariaDB"


#### YCSB Reset Citus
bexhoma ycsb `
  -dbms Citus                   <# CHECKPOINT and pg_stat_reset* on coordinator and every worker #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor (Dragonfly: replica mode) #> `
  -nws 48                       <# number of shards #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_citus.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset Citus"


#### YCSB Reset CockroachDB
bexhoma ycsb `
  -dbms CockroachDB             <# ANALYZE, crdb_internal.reset_sql_stats(), persist n/a #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor (Dragonfly: replica mode) #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_cockroachdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset CockroachDB"


#### YCSB Reset TiDB
bexhoma ycsb `
  -dbms TiDB                    <# ANALYZE TABLE, FLUSH STATUS, persist n/a #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 1                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnsr 3                       <# number of TiDB SUT replicas #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor (Dragonfly: replica mode) #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -xnpd 3                       <# number of PD nodes #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_tidb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset TiDB"


#### YCSB Reset Dragonfly
bexhoma ycsb `
  -dbms Dragonfly               <# SAVE and CONFIG RESETSTAT in the SUT pod #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_dragonfly.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset Dragonfly"


#### YCSB Reset Dragonfly Replica
bexhoma ycsb `
  -dbms Dragonfly               <# SAVE and CONFIG RESETSTAT on every worker #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor (Dragonfly: replica mode) #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_dragonfly_replica.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset Dragonfly Replica"


#### YCSB Reset Redis
bexhoma ycsb `
  -dbms Redis                   <# SAVE and CONFIG RESETSTAT in the SUT pod #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_redis.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset Redis"


#### YCSB Reset Redis Cluster
bexhoma ycsb `
  -dbms Redis                   <# SAVE and CONFIG RESETSTAT on every cluster node #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_redis_cluster.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset Redis Cluster"


#### YCSB Reset YugabyteDB
Install-YugabyteDB

bexhoma ycsb `
  -dbms YugabyteDB              <# ANALYZE, reset-counters.sh on every tserver, persist n/a #> `
  -sf 1                         <# scaling factor #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_ycsb_yugabytedb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB reset YugabyteDB"

Remove-YugabyteDB




###########################################
################ Benchbase ################
###########################################


#### Benchbase Reset TPC-C PostgreSQL
bexhoma benchbase `
  -dbms PostgreSQL              <# VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C PostgreSQL"


#### Benchbase Reset TPC-C PGBouncer
bexhoma benchbase `
  -dbms PGBouncer               <# reset of PostgreSQL, through the pooler #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -xnpp 1                       <# number of PGBouncer proxy pods #> `
  -xnpi 128                     <# maximum incoming connections per PGBouncer instance (default: loading threads = 1) #> `
  -xnpo 64                      <# maximum outgoing connections per PGBouncer instance #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_pgbouncer.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C PGBouncer"


#### Benchbase Reset TPC-C MySQL
bexhoma benchbase `
  -dbms MySQL                   <# ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS) #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_mysql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C MySQL"


#### Benchbase Reset TPC-C MariaDB
bexhoma benchbase `
  -dbms MariaDB                 <# ANALYZE TABLE, then reset-flush.sh (dirty pages, FLUSH STATUS) #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C MariaDB"


#### Benchbase Reset Twitter PostgreSQL
bexhoma benchbase `
  -dbms PostgreSQL              <# reset for a Benchbase benchmark other than tpcc #> `
  -sf 4                         <# scaling factor #> `
  -xbt twitter                  <# Benchbase benchmark #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_twitter_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset Twitter PostgreSQL"


#### Benchbase Reset TPC-C Citus
bexhoma benchbase `
  -dbms Citus                   <# CHECKPOINT and pg_stat_reset* on coordinator and every worker #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor (Dragonfly: replica mode) #> `
  -nws 48                       <# number of shards #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_citus.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C Citus"


#### Benchbase Reset TPC-C CockroachDB
bexhoma benchbase `
  -dbms CockroachDB             <# ANALYZE, crdb_internal.reset_sql_stats(), persist n/a #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor (Dragonfly: replica mode) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_cockroachdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C CockroachDB"


#### Benchbase Reset TPC-C TiDB
bexhoma benchbase `
  -dbms TiDB                    <# ANALYZE TABLE benchbase.*, FLUSH STATUS, persist n/a #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -xnsr 3                       <# number of TiDB SUT replicas #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor (Dragonfly: replica mode) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -xnpd 3                       <# number of PD nodes #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_tidb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C TiDB"


#### Benchbase Reset TPC-C YugabyteDB
Install-YugabyteDB

bexhoma benchbase `
  -dbms YugabyteDB              <# ANALYZE, reset-counters.sh on every tserver, persist n/a #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 40                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_benchbase_yugabytedb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase reset TPC-C YugabyteDB"

Remove-YugabyteDB




###########################################
################ HammerDB #################
###########################################


#### HammerDB Reset PostgreSQL
bexhoma hammerdb `
  -dbms PostgreSQL              <# VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* in database tpcc #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlt 4                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_hammerdb_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB reset PostgreSQL"


#### HammerDB Reset MySQL
bexhoma hammerdb `
  -dbms MySQL                   <# ANALYZE TABLE in database tpcc, then reset-flush.sh #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlt 4                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_hammerdb_mysql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB reset MySQL"


#### HammerDB Reset MariaDB
bexhoma hammerdb `
  -dbms MariaDB                 <# ANALYZE TABLE in database tpcc, then reset-flush.sh #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlt 4                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_hammerdb_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB reset MariaDB"


#### HammerDB Reset Citus
bexhoma hammerdb `
  -dbms Citus                   <# CHECKPOINT and pg_stat_reset* on coordinator and every worker #> `
  -sf 4                         <# scaling factor #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlt 4                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor (Dragonfly: replica mode) #> `
  -nws 48                       <# number of shards #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_hammerdb_citus.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB reset Citus"




###########################################
################## TPC-H ##################
###########################################


#### TPC-H Reset PostgreSQL
bexhoma tpch `
  -dbms PostgreSQL              <# VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset PostgreSQL"


#### TPC-H Reset PgDuckDB
bexhoma tpch `
  -dbms PgDuckDB                <# reset of PostgreSQL #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_pgduckdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset PgDuckDB"


#### TPC-H Reset MonetDB
bexhoma tpch `
  -dbms MonetDB                 <# ANALYZE, persist n/a, counters n/a #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_monetdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset MonetDB"


#### TPC-H Reset MySQL
bexhoma tpch `
  -dbms MySQL                   <# ANALYZE TABLE tpch.*, then reset-flush.sh #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_mysql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset MySQL"


#### TPC-H Reset MariaDB
bexhoma tpch `
  -dbms MariaDB                 <# ANALYZE TABLE tpch.*, then reset-flush.sh #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset MariaDB"


#### TPC-H Reset Citus
bexhoma tpch `
  -dbms Citus                   <# CHECKPOINT and pg_stat_reset* on coordinator and every worker #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor (Dragonfly: replica mode) #> `
  -nws 48                       <# number of shards #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_citus.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset Citus"


#### TPC-H Reset PostgreSQL with Refresh Stream
bexhoma tpch `
  -dbms PostgreSQL              <# one reset per round, before both streams #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,1"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xrs 1                        <# refresh stream in parallel -- one reset per round, none for the refresh stream #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpch_refresh_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H reset PostgreSQL with Refresh Stream"




###########################################
################# TPC-DS ##################
###########################################


#### TPC-DS Reset PostgreSQL
bexhoma tpcds `
  -dbms PostgreSQL              <# VACUUM ANALYZE, CHECKPOINT, pg_stat_reset* #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# timeout per query in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpcds_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS reset PostgreSQL"


#### TPC-DS Reset MonetDB
bexhoma tpcds `
  -dbms MonetDB                 <# ANALYZE, persist n/a, counters n/a #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# timeout per query in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpcds_monetdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS reset MonetDB"


#### TPC-DS Reset MySQL
bexhoma tpcds `
  -dbms MySQL                   <# ANALYZE TABLE tpcds.*, then reset-flush.sh #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# timeout per query in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpcds_mysql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS reset MySQL"


#### TPC-DS Reset MariaDB
bexhoma tpcds `
  -dbms MariaDB                 <# ANALYZE TABLE tpcds.*, then reset-flush.sh #> `
  -sf 1                         <# scaling factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,2"                     <# two client rounds -- the reset runs before each #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after loading #> `
  -xic                          <# create constraints after loading #> `
  -xis                          <# recompute statistics after loading #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# timeout per query in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# activate configured reset scripts before each round #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_reset_tpcds_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS reset MariaDB"




###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
