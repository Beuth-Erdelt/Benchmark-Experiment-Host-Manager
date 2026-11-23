#Requires -Version 5.1
# Core set of reference experiments: the release gate of minor releases.
#
# Runs one experiment per benchmark on PostgreSQL, plus monitoring, application
# monitoring and persistent storage, BEXHOMA_PARALLEL of them at a time. The commands
# are copied unchanged from the test-docs-* scripts (tests/test_reference_experiments.py
# checks that they agree), so the logs are those of the documentation, in logs_tests.
# At the end it checks every log: at least one passed test, no failed test, no
# traceback, and the installed bexhoma version. A minor release needs all of them to pass.
#
# Runs:
#    1. TPC-H with monitoring                        docs_tpch_postgresql_monitoring (test-docs-tpch)
#    2. TPC-H with persistent storage                docs_tpch_postgresql_storage (test-docs-tpch)
#    3. TPC-H refresh stream                         docs_tpch_postgresql_refresh (test-docs-tpch)
#    4. TPC-DS                                       docs_tpcds_postgresql (test-docs-tpcds)
#    5. SSB                                          docs_ssb_postgresql (test-docs-ssb)
#    6. YCSB with monitoring                         docs_ycsb_postgresql_monitoring (test-docs-ycsb)
#    7. Benchbase TPC-C                              docs_benchbase_postgresql_run (test-docs-modes)
#    8. HammerDB TPC-C                               docs_hammerdb_postgresql_run (test-docs-modes)
#    9. application monitoring (Benchbase TPC-C)     docs_benchbase_postgresql_appmetrics (test-docs-appmetrics)
#   10. hardware (fio, WAL sync writes)              docs_hardware_fio_wal_sync_fdatasync (test-docs-hardware)
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# number of experiments that run at the same time
if ($env:BEXHOMA_PARALLEL) { $BEXHOMA_PARALLEL = [int]$env:BEXHOMA_PARALLEL } else { $BEXHOMA_PARALLEL = 4 }

. .\scripts\testfunctions.ps1

$BEXHOMA_VERSION = (pip show bexhoma | Select-String "^Version:" | ForEach-Object { ($_ -split '\s+')[1] })
# without the version, every log would pass the version check
if (-not $BEXHOMA_VERSION) { throw "bexhoma is not installed (pip show bexhoma)" }
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') bexhoma $BEXHOMA_VERSION, $BEXHOMA_PARALLEL experiments at a time"

# each run is a job of its own: it loads the test functions and runs one command
$RUNS = [ordered]@{}

#### 1. TPC-H with monitoring (test-docs-tpch.ps1)
$RUNS["docs_tpch_postgresql_monitoring"] = {
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_monitoring.log" -Encoding utf8
}

#### 2. TPC-H with persistent storage (test-docs-tpch.ps1)
$RUNS["docs_tpch_postgresql_storage"] = {
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_storage.log" -Encoding utf8
}

#### 3. TPC-H refresh stream (test-docs-tpch.ps1)
$RUNS["docs_tpch_postgresql_refresh"] = {
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ne 3                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -xrs 3                        <# parallel refresh stream applying 3 RF1+RF2 pairs per round #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
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
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_refresh.log" -Encoding utf8
}

#### 4. TPC-DS (test-docs-tpcds.ps1)
$RUNS["docs_tpcds_postgresql"] = {
bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
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
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_postgresql.log" -Encoding utf8
}

#### 5. SSB (test-docs-ssb.ps1)
$RUNS["docs_ssb_postgresql"] = {
bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -nlp 8                        <# number of loader pods (lineorder is generated in 8 chunks) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# add primary and foreign keys after data load #> `
  -xis                          <# run ANALYZE after data load #> `
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
}

#### 6. YCSB with monitoring (test-docs-ycsb.ps1)
$RUNS["docs_ycsb_postgresql_monitoring"] = {
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2,3                     <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_postgresql_monitoring.log" -Encoding utf8
}

#### 7. Benchbase TPC-C (test-docs-modes.ps1)
$RUNS["docs_benchbase_postgresql_run"] = {
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 8                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_run.log" -Encoding utf8
}

#### 8. HammerDB TPC-C (test-docs-modes.ps1)
$RUNS["docs_hammerdb_postgresql_run"] = {
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod (virtual users) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_postgresql_run.log" -Encoding utf8
}

#### 9. application monitoring (Benchbase TPC-C) (test-docs-appmetrics.ps1)
$RUNS["docs_benchbase_postgresql_appmetrics"] = {
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_appmetrics.log" -Encoding utf8
}

#### 10. hardware (fio, WAL sync writes) (test-docs-hardware.ps1)
$RUNS["docs_hardware_fio_wal_sync_fdatasync"] = {
bexhoma hardware `
  -dbms Hardware                <# hardware target(s) to test #> `
  -xht fio                      <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                       <# fio test file size #> `
  -xtd 60                       <# seconds per fio round #> `
  -xfrw write                   <# sequential write, simulating WAL append #> `
  -xfbs 8k                      <# fio block size, one WAL page per write #> `
  -xfid 1                       <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                   <# fio ioengine #> `
  -xffd 1                       <# fdatasync after every write (wal_sync_method=fdatasync) #> `
  -xfow 1                       <# prefilled test file: writes go into written blocks, like recycled WAL segments #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# benchmarking pod count #> `
  -nbt 1                        <# threads per benchmarking pod, fixed (single backend) #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rsr                          <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_wal_sync_fdatasync.log" -Encoding utf8
}


#### run them, BEXHOMA_PARALLEL at a time
$repo = (Get-Location).Path
$jobs = @()
foreach ($log in $RUNS.Keys) {
    while (@($jobs | Where-Object { $_.State -eq "Running" }).Count -ge $BEXHOMA_PARALLEL) {
        Start-Sleep -Seconds 30
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [START] $log"
    $jobs += Start-Job -Name $log -ArgumentList $repo, $RUNS[$log].ToString() -ScriptBlock {
        param($repo, $command)
        Set-Location $repo
        . .\scripts\testfunctions.ps1 | Out-Null
        Invoke-Expression $command
    }
    Start-Sleep -Seconds 30
}
$jobs | Wait-Job | Out-Null
$jobs | Receive-Job | Out-Null
$jobs | Remove-Job


#### check the logs
$failed = $false
foreach ($log in $RUNS.Keys) {
    $file = Join-Path $LOG_DIR "$log.log"
    $text = if (Test-Path $file) { Get-Content $file -Raw } else { "" }
    $problems = @()
    if ($text -notmatch "TEST passed") { $problems += "no passed test" }
    if ($text -match "TEST failed") { $problems += "failed test" }
    if ($text -match "(?m)^Traceback") { $problems += "traceback" }
    if ($text -notmatch "bexhoma version $([regex]::Escape($BEXHOMA_VERSION))") { $problems += "not bexhoma $BEXHOMA_VERSION" }
    if ($problems) {
        Write-Host "FAILED  ${log}: $($problems -join ', ')"
        $failed = $true
    } else {
        Write-Host "passed  $log"
    }
}


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs

if ($failed) {
    Write-Host "Reference experiments: FAILED"
    exit 1
}
Write-Host "Reference experiments: all passed with bexhoma $BEXHOMA_VERSION"
