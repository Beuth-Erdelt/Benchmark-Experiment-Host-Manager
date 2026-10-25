#Requires -Version 5.1
# Generates documentation summaries for SSB (Star Schema Benchmark) experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




###########################################
################### SSB ###################
###########################################




#### SSB PostgreSQL (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_postgresql.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB PostgreSQL  sf=1"


#### SSB MonetDB (Example-SSB.md)
bexhoma ssb `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_monetdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB MonetDB  sf=1"


#### SSB ClickHouse (Example-SSB.md)
bexhoma ssb `
  -dbms ClickHouse              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_clickhouse.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB ClickHouse  sf=1"


#### SSB Flat (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL MonetDB ClickHouse  <# DBMS under test (all three) #> `
  -sf 1                                <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xsv flat                            <# one denormalized table lineorder_flat, generated as flat files #> `
  -xii                                 <# create indexes after data load #> `
  -xis                                 <# run ANALYZE after data load #> `
  -nlp 8                               <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                                 <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS                      <# max simultaneous DBMS configurations #> `
  -t 1200                              <# query timeout in seconds #> `
  -tr                                  <# verify result meets basic sanity requirements #> `
  -lr 64Gi                             <# RAM limit for the SUT container #> `
  -rr 64Gi                             <# RAM requested for the SUT container #> `
  -rss 50Gi                            <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT               <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD              <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK         <# schedule benchmarker pods on this node #> `
  -ks no                               <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_flat.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB flat  sf=1"


#### SSB Random Parameters (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xqv random                   <# random query parameters that keep the filter factor of each query #> `
  -xrcp                         <# new random parameters for each stream #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_random.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB random  sf=1  ne=1,2"


#### SSB Persistent Storage (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -nc 2                         <# number of repeated runs per configuration (2nd run: data survives the SUT restart) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB storage  sf=1  nc=2"


#### SSB Load (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  load 2>&1 | Out-File "$LOG_DIR\docs_ssb_load.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB load  sf=1"


#### SSB Profiling (Example-SSB.md)
bexhoma ssb `
  -dbms PostgreSQL MonetDB ClickHouse  <# DBMS under test (all three) #> `
  -sf 1                                <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -nlp 8                               <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xdt                                 <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS                      <# max simultaneous DBMS configurations #> `
  -t 1200                              <# query timeout in seconds #> `
  -tr                                  <# verify result meets basic sanity requirements #> `
  -lr 64Gi                             <# RAM limit for the SUT container #> `
  -rr 64Gi                             <# RAM requested for the SUT container #> `
  -rss 50Gi                            <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT               <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD              <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK         <# schedule benchmarker pods on this node #> `
  -ks no                               <# remove the SUT at the end #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 <# lower planner cost for random reads (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 <# allow more concurrent prefetch I/O requests (SSD) #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring <# use io_uring for asynchronous I/O #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 <# parallel workers per query node #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 <# total parallel worker pool #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 <# total background worker processes #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB <# PostgreSQL buffer cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB <# planner estimate of OS-level cache size #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB <# per-operation sort/hash memory #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB <# memory for index/vacuum maintenance #> `
  profiling 2>&1 | Out-File "$LOG_DIR\docs_ssb_profiling.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB profiling  sf=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
