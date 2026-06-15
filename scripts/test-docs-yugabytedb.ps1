#Requires -Version 5.1
# Generates documentation summaries for YugabyteDB experiments.
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

function Install-YugabyteDB {
    param([string]$Persistent = "yes")

    if ($Persistent -eq "yes") { $Ephemeral = "false" } else { $Ephemeral = "true" }

    helm install bexhoma yugabytedb/yugabyte `
        --version 2025.2.1 `
        --set "gflags.tserver.ysql_enable_packed_row=true,gflags.tserver.ysql_max_connections=1280,resource.master.limits.cpu=2,resource.master.limits.memory=16Gi,resource.master.requests.cpu=2,resource.master.requests.memory=16Gi,resource.tserver.limits.cpu=8,resource.tserver.limits.memory=16Gi,resource.tserver.requests.cpu=8,resource.tserver.requests.memory=16Gi,storage.master.size=100Gi,storage.master.storageClass=shared,storage.tserver.size=100Gi,storage.tserver.storageClass=shared,storage.ephemeral=$Ephemeral,tserver.livenessProbe.timeoutSeconds=10,master.livenessProbe.timeoutSeconds=10,enableLoadBalancer=true"

    Write-Host "Waiting 60s for pods to start..."
    Start-Sleep -Seconds 60
}

function Remove-YugabyteDB {
    param([string]$RemovePVC = "no")

    Write-Host "Deleting Helm release bexhoma..."
    helm delete bexhoma

    if ($RemovePVC -eq "yes") {
        Write-Host "Removing PVCs for yb-tserver and yb-master..."
        kubectl delete pvc -l app=yb-tserver
        kubectl delete pvc -l app=yb-master
    } else {
        Write-Host "Keeping PVCs (persistent storage not deleted)"
    }

    Write-Host "Waiting 60s for cleanup..."
    Start-Sleep -Seconds 60
}

# ---------------------------------------------------------------------------
# Wait for any pre-existing jobs
# ---------------------------------------------------------------------------

Wait-BexhomaProcess "tpch"
Wait-BexhomaProcess "tpcds"
Wait-BexhomaProcess "hammerdb"
Wait-BexhomaProcess "benchbase"
Wait-BexhomaProcess "ycsb"




################################################
################## YugaByteDB ##################
################################################


# install YugabyteDB
Install-YugabyteDB -Persistent "no"

#### YCSB Ingestion (Example-YugaByteDB.md)
bexhoma ycsb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_yugabytedb_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB YugabyteDB ingestion  sf=1  nbp=1"

#### YCSB Execution (Example-YugaByteDB.md)
bexhoma ycsb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -sl                           <# skip loading phase (reuse existing data) #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_yugabytedb_2.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB YugabyteDB execution skip-load  sf=1  nbp=1"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"
Start-Sleep -Seconds 30

# install YugabyteDB
Install-YugabyteDB -Persistent "no"
Start-Sleep -Seconds 30

kubectl delete pvc bexhoma-storage-yugabytedb-ycsb-1
Start-Sleep -Seconds 30

#### YCSB Dummy Persistent Storage (Example-YugaByteDB.md)
bexhoma ycsb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 1Gi                      <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_yugabytedb_3.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB YugabyteDB dummy PVC  sf=1  nbp=1"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"
Start-Sleep -Seconds 30

# install YugabyteDB
Install-YugabyteDB -Persistent "no"
Start-Sleep -Seconds 30


#### Benchbase Simple (Example-YugaByteDB.md)
bexhoma benchbase `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                         <# benchmark duration in minutes #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -xnbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -xtb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_yugabytedb_1.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YugabyteDB simple  sf=16  nbp=1,2"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"
Start-Sleep -Seconds 30

# install YugabyteDB
Install-YugabyteDB -Persistent "no"
Start-Sleep -Seconds 30


#### Benchbase More Complex (Example-YugaByteDB.md)
bexhoma benchbase `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 128                       <# scaling factor (controls database size) #> `
  -xli 30                       <# log status to stdout every x seconds #> `
  -xsd 20                        <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 1280                     <# threads per benchmarking pod #> `
  -xnbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -xtb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_yugabytedb_2.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YugabyteDB complex  sf=128  nbp=1,2,5,10"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"


################################################
######## YugaByteDB Application Metrics ########
################################################


# install YugabyteDB
Install-YugabyteDB -Persistent "no"
Start-Sleep -Seconds 30

bexhoma ycsb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_yugabytedb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB YugabyteDB appmetrics  sf=1  nbp=1"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"


# install YugabyteDB
Install-YugabyteDB -Persistent "no"
Start-Sleep -Seconds 30


#### Benchbase Application Metrics (Example-YugaByteDB.md)
bexhoma benchbase `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                         <# benchmark duration in minutes #> `
  -dbms YugabyteDB              <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -xnbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -xtb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_yugabytedb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YugabyteDB appmetrics  sf=16  nbp=1,2"


# remove YugabyteDB installation
Remove-YugabyteDB -RemovePVC "no"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
