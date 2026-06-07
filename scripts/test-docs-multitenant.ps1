#Requires -Version 5.1
# Generates documentation summaries for multi-tenancy experiments.
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
######### Benchbase TPC-H Multi-Tenant PVC #########
####################################################

$BEXHOMA_NUM_TENANTS = 2

bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp $BEXHOMA_NUM_TENANTS     <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_run_postgresql_tenants_schema.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp $BEXHOMA_NUM_TENANTS     <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_run_postgresql_tenants_database.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nlt 64                       <# threads per benchmarking pod #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_run_postgresql_tenants_container.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

$BEXHOMA_NUM_TENANTS = 2

bexhoma benchbase `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_postgresql_tenants_schema.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_postgresql_tenants_database.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_postgresql_tenants_container.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######## Benchbase TPC-C Multi-Tenant MySQL ########
####################################################

$BEXHOMA_NUM_TENANTS = 2

bexhoma benchbase `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  --dbms MySQL                  <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_mysql_tenants_database.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT MySQL database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -xkey                         <# simulate user think time and keying delays #> `
  --dbms MySQL                  <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_mysql_tenants_container.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT MySQL container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
