#Requires -Version 5.1
# Generates documentation summaries for PgDuckDB experiments (Example-PgDuckDB.md).
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H power test on PgDuckDB in the DuckDB engine, quick, without monitoring
bexhoma tpch `
  -dbms PgDuckDB                <# DBMS under test #> `
  -xdfe                         <# run the queries in the DuckDB engine of pg_duckdb #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_pgduckdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PgDuckDB  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on PgDuckDB in the DuckDB engine
bexhoma tpch `
  -dbms PgDuckDB                <# DBMS under test #> `
  -xdfe                         <# run the queries in the DuckDB engine of pg_duckdb #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 150Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_pgduckdb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PgDuckDB monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H on PgDuckDB in the DuckDB engine, the second run uses the loaded volume
bexhoma tpch `
  -dbms PgDuckDB                <# DBMS under test #> `
  -xdfe                         <# run the queries in the DuckDB engine of pg_duckdb #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_pgduckdb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PgDuckDB storage  sf=1  nc=2"


####################################################
#### Variants ######################################
####################################################


# Variant: TPC-H power test on PgDuckDB in the executor of PostgreSQL (without -xdfe)
bexhoma tpch `
  -dbms PgDuckDB                <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_pgduckdb_postgresql_engine.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PgDuckDB PostgreSQL engine  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on PgDuckDB: 3 query streams and one RF1/RF2 stream in parallel
bexhoma tpch `
  -dbms PgDuckDB                <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -ne 3                         <# parallel query streams #> `
  -xrs 3                        <# refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_pgduckdb_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PgDuckDB refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
