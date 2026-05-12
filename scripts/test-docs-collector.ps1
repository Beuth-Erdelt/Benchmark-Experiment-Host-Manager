#Requires -Version 5.1
# Generates documentation summaries for collector experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

$BEXHOMA_NODE_SUT       = "cl-worker38"
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
############# TPC-C Benchbase #############
###########################################




#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_1.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase collector 1/3  sf=16  nbp=1,2  nbf=16"

#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nbp 4,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -nbf 20                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_2.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase collector 2/3  sf=16  nbp=4,8  nbf=20"

#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nbp 4,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -nbf 20                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_3.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase collector 3/3  sf=16  nbp=4,8  nbf=20"




###########################################
########### TPC-C Benchbase MT ############
###########################################


$BEXHOMA_NUM_TENANTS = 2

# ---------------- SCHEMA ----------------
bexhoma benchbase `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
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
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_tenants_schema.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- DATABASE ----------------
bexhoma benchbase `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
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
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_tenants_database.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- CONTAINER ----------------
bexhoma benchbase `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
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
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_collector_tenants_container.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




###########################################
################## TPC-H ##################
###########################################


bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_1.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H collector 1/3  sf=3"

bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 6                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_2.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H collector 2/3  sf=6"

bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 6                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_3.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H collector 3/3  sf=6"




###########################################
################ TPC-H MT #################
###########################################

$BEXHOMA_NUM_TENANTS = 2

# ---------------- SCHEMA ----------------
bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
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
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_tenants_schema.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- DATABASE ----------------
bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
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
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_tenants_database.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- CONTAINER ----------------
bexhoma tpch `
  -tr                           <# verify result meets basic sanity requirements #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 15Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_collector_tenants_container.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=3"


###########################################
################## YCSB ###################
###########################################


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
  -nbf 2                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 15Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_collector_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB collector 1/3  nbp=1,8  nbf=2"

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
  -nbf 3                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 15Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_collector_2.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB collector 2/3  nbp=1,8  nbf=3"

#### YCSB Monitoring (Example-YCSB.md)
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
  -nbf 3                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_collector_3.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB collector 3/3  nbp=1,8  nbf=3"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 15Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_collector_1.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB collector 1/3  sf=16  nbp=1,2  nbt=16"

#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod (virtual users) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 15Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_collector_2.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB collector 2/3  sf=16  nbp=1,2  nbt=32"

#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod (virtual users) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_collector_3.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB collector 3/3  sf=16  nbp=1,2  nbt=32"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
