#Requires -Version 5.1
# Generates documentation summaries for TPC-H experiments.
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
################# TPC-H ###################
###########################################




#### TCP-H Compare (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_compare.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H compare  sf=1"


#### TCP-H Monitoring (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_monitoring.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H monitoring  sf=10"


#### TCP-H Throughput (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_throughput.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
Start-Sleep -Seconds 30


#### TCP-H Persistent Storage (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_storage.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H storage  sf=1  nc=2"


#### TCP-H Fractional Scaling Factor (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 0.1                       <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_fractional.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H fractional  sf=0.1  nc=2"


###########################################
############# TPC-H MonetDB ###############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpch-100
Start-Sleep -Seconds 30


#### TCP-H Power 100 (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -dbms MonetDB                 <# DBMS under test #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -t 3600                       <# query timeout in seconds #> `
  -dt                           <# disable result type checking #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_monetdb_1.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB power  sf=100  nc=1  ne=1"


#### TCP-H Power 100 repeated (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -dbms MonetDB                 <# DBMS under test #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -t 3600                       <# query timeout in seconds #> `
  -dt                           <# disable result type checking #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_monetdb_2.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB power  sf=100  nc=2  ne=1,1"


#### TCP-H Throughput 100 (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1,1,3                     <# parallel client counts to sweep (comma-separated) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -dbms MonetDB                 <# DBMS under test #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -t 3600                       <# query timeout in seconds #> `
  -dt                           <# disable result type checking #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_monetdb_3.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB throughput  sf=100  ne=1,1,3"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
