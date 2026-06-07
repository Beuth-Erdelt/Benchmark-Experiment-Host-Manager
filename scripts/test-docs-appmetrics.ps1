#Requires -Version 5.1
# Generates documentation summaries for application metrics experiments.
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
########## PostgreSQL Application Metrics ##########
####################################################




#### Benchbase Application Metrics (Example-Benchbase.md)
bexhoma benchbase `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_postgresql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PostgreSQL appmetrics  sf=16  nbp=1,2"


#### YCSB Application Metrics (Example-YCSB.md)
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
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL appmetrics  sf=3  nbp=1,8"


#### TPC-H Application Metrics (Example-TPC-H.md)
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -t 1200                       <# query timeout in seconds #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PostgreSQL appmetrics  sf=3"


#### TPC-DS Application Metrics (Example-TPC-DS.md)
bexhoma tpcds `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -t 1200                       <# query timeout in seconds #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpcds_testcase_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "tpcds"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS PostgreSQL appmetrics  sf=3"


#### HammerDB Application Metrics (Example-HammerDB.md)
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
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB PostgreSQL appmetrics  sf=16  nbp=1,2"


####################################################
############ MySQL Application Metrics #############
####################################################


#### Benchbase MySQL Application Metrics
bexhoma benchbase `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms MySQL                   <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_mysql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MySQL appmetrics  sf=16  nbp=1,2"


#### YCSB MySQL Application Metrics
bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 3                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms MySQL                   <# DBMS under test #> `
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
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_mysql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL appmetrics  sf=3  nbp=1,8"


#### TPC-H MySQL Application Metrics
bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -dbms MySQL                   <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -t 1200                       <# query timeout in seconds #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_run_mysql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MySQL appmetrics  sf=3"


#### TPC-DS MySQL Application Metrics
bexhoma tpcds `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -dt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -dbms MySQL                   <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -t 1200                       <# query timeout in seconds #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpcds_run_mysql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "tpcds"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MySQL appmetrics  sf=3"


#### HammerDB MySQL Application Metrics
bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms MySQL                   <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_run_mysql_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MySQL appmetrics  sf=16  nbp=1,2"


####################################################
######### CockroachDB Application Metrics ##########
####################################################


bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -sfo 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms CockroachDB             <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
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
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_cockroachdb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB CockroachDB appmetrics  sf=10  nbp=1"


#### Benchbase CockroachDB Application Metrics
bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  -dbms CockroachDB             <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_cockroachdb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase CockroachDB appmetrics  sf=16  nbp=1,2"


####################################################
############ Redis Application Metrics #############
####################################################


bexhoma ycsb `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -sfo 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms Redis                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 12                       <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_redis_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Redis appmetrics  sf=1  nbp=1"


####################################################
############# TiDB Application Metrics #############
####################################################


bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -sfo 1                        <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  -nsr 3                        <# number of storage replicas #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms TiDB                    <# DBMS under test #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 1                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 1                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_tidb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB TiDB appmetrics  sf=1  nbp=1"


bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  -nsr 3                        <# number of storage replicas #> `
  -dbms TiDB                    <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_tidb_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase TiDB appmetrics  sf=16  nbp=1,2"


####################################################
########### PGBouncer Application Metrics ##########
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
  -ma                           <# collect application-level metrics #> `
  -npp 4                        <# number of PGBouncer pool instances #> `
  -npi 128                      <# pool size (incoming connections) #> `
  -npo 64                       <# pool size (outgoing connections) #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_run_pgbouncer_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PGBouncer appmetrics  sf=16  nbp=16"


#### Benchbase PGBouncer Application Metrics
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
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect application-level metrics #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_run_pgbouncer_appmetrics.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PGBouncer appmetrics  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
