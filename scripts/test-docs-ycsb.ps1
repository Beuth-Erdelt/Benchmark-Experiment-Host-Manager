#Requires -Version 5.1
# Generates documentation summaries for YCSB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

$BEXHOMA_NODE_SUT       = "cl-worker14"
$BEXHOMA_NODE_LOAD      = "cl-worker19"
$BEXHOMA_NODE_BENCHMARK = "cl-worker19"
$LOG_DIR                = ".\logs_tests"

# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------

if (-not (Test-Path "cluster.config")) {
    Write-Error "Error: cluster.config not found."
    exit 1
}
Write-Host "Passed: ./cluster.config found."

foreach ($dir in @("experiments", "k8s")) {
    if (-not (Test-Path $dir -PathType Container)) {
        Write-Error "Error: Directory '$dir' missing."
        exit 1
    }
}
Write-Host "Passed: ./experiments/ found."
Write-Host "Passed: ./k8s/ found."

New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null
Write-Host "Passed: $LOG_DIR/ found."

Write-Host "Checks passed. Proceeding..."

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Wait-BexhomaProcess {
    param([string]$ProcessName)
    while ($true) {
        $running = Get-CimInstance Win32_Process |
                   Where-Object { $_.CommandLine -like "*bexhoma*$ProcessName*" }
        if (-not $running) { break }
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Waiting for bexhoma $ProcessName to terminate..."
        Start-Sleep -Seconds 60
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): bexhoma $ProcessName has terminated."
}

function Invoke-CleanLogs {
    $warningText = "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens."

    Write-Host "Removing connection warning lines from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" -Recurse | ForEach-Object {
        $lines = Get-Content $_.FullName
        $filtered = $lines | Where-Object { $_ -ne $warningText }
        if ($filtered.Count -ne $lines.Count) {
            $filtered | Set-Content $_.FullName -Encoding utf8
        }
    }

    Write-Host "Extracting summaries from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" | ForEach-Object {
        $filename = $_.BaseName
        Write-Host "Cleaning $($_.FullName)"
        $show = $false
        $summary = @(foreach ($line in Get-Content $_.FullName) {
            if ($line -match '## Show Summary') { $show = $true }
            if ($show) { $line }
        })
        $summary | Out-File "$LOG_DIR\${filename}_summary.md" -Encoding utf8
    }

    Write-Host "Extraction complete! Files are saved in $LOG_DIR."
}

# ---------------------------------------------------------------------------
# Wait for any pre-existing jobs
# ---------------------------------------------------------------------------

Wait-BexhomaProcess "tpch"
Wait-BexhomaProcess "tpcds"
Wait-BexhomaProcess "hammerdb"
Wait-BexhomaProcess "benchbase"
Wait-BexhomaProcess "ycsb"




###########################################
################## YCSB ###################
###########################################




#### YCSB Scale Loading (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 1,8                      <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 1,4                      <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 2                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_loading.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB loading  sf=1  nlp=1,8"


#### YCSB Scale Benchmarking (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 2,3                      <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_benchmarking.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB benchmarking  sf=1  nbp=1,8"


#### YCSB Monitoring (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 3                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 2,3                      <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_monitoring.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB monitoring  sf=3  nbp=1,8"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
Start-Sleep -Seconds 30


#### YCSB Persistent Storage (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 2,3                      <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_storage.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB storage  sf=1  nbp=1,8  nc=2"


#### YCSB Custom Loading Parameters (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 1                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 2                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  '--set' 'deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64' `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_loading_patch.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB loading patch  sf=1  nlp=1"


###########################################
############## All Workloads ##############
###########################################


#### YCSB Workload A (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_a.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload a  sf=10  nbp=1,8"


#### YCSB Workload B (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload b                  <# YCSB workload template (b = 95% read / 5% update) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_b.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload b  sf=10  nbp=1,8"


#### YCSB Workload C (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_c.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload c  sf=10  nbp=1,8"


#### YCSB Workload D (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload d                  <# YCSB workload template (d = read latest) #> `
  -xio hashed                   <# index order strategy (hashed / ordered) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_d.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload d  sf=10  nbp=1"


#### YCSB Workload E (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload e                  <# YCSB workload template (e = scan) #> `
  -xio ordered                  <# index order strategy (hashed / ordered) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_e.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload e  sf=10  nbp=1"


#### YCSB Workload F (Example-YCSB.md)
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  --workload f                  <# YCSB workload template (f = read-modify-write) #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_f.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload f  sf=10  nbp=1,8"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
