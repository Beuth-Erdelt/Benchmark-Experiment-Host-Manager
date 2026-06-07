#Requires -Version 5.1
# Generates documentation summaries for bexhoma start/load mode experiments.
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
#################### YCSB Modes ####################
####################################################


bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_ycsb_start_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_ycsb_load_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  --workload c                  <# YCSB workload template (c = 100% read) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 8                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_ycsb_run_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb




####################################################
################## Benchbase Modes #################
####################################################


bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_benchbase_start_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_benchbase_load_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 8                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc




####################################################
################### HammerDB Modes #################
####################################################


bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_hammerdb_start_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_hammerdb_load_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod (virtual users) #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_hammerdb_run_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc




####################################################
##################### TPC-H Modes ##################
####################################################


bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_tpch_start_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_tpch_load_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_run_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h




####################################################
#################### TPC-DS Modes ##################
####################################################


bexhoma tpcds `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_tpcds_start_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpcds"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_tpcds_load_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpcds"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --dbms PostgreSQL             <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpcds_run_postgresql.log" -Encoding utf8

Wait-BexhomaProcess "tpcds"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
