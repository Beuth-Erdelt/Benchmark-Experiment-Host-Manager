#Requires -Version 5.1
# Generates documentation summaries for PGBouncer experiments.
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




####################################################
################## YCSB PGBouncer ##################
####################################################




bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of records x 1000) #> `
  -sfo 16                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -dbms PGBouncer               <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 16                       <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 11                       <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 16                       <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nbf 11                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -npp 4                        <# number of PGBouncer pool instances #> `
  -npi 128                      <# pool size (incoming connections) #> `
  -npo 64                       <# pool size (outgoing connections) #> `
  run 2>&1 | Out-File "$LOG_DIR\test_ycsb_testcase_pgbouncer_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PGBouncer  sf=16  nbp=16"


bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of records x 1000) #> `
  -sfo 16                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -dbms PGBouncer               <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 16                       <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 11                       <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 16                       <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nbf 11                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -npp 4                        <# number of PGBouncer pool instances #> `
  -npi 128                      <# pool size (incoming connections) #> `
  -npo 64                       <# pool size (outgoing connections) #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_ycsb_testcase_pgbouncer_2.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PGBouncer storage  sf=16  nbp=16  nc=2"


####################################################
############### Benchbase PGBouncer ################
####################################################


bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 10                        <# benchmark duration in minutes #> `
  -xconn                        <# collect new-connection latency #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_newconn.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase new-connection PostgreSQL  sf=16  nbp=1,2"


#### Benchbase PGBouncer (Example-PGBouncer.md)
bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 10                        <# benchmark duration in minutes #> `
  -xconn                        <# collect new-connection latency #> `
  -dbms PGBouncer               <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -npp 2                        <# number of PGBouncer pool instances #> `
  -npi 32                       <# pool size (incoming connections) #> `
  -npo 32                       <# pool size (outgoing connections) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_newconn_pool.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase new-connection PGBouncer  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
