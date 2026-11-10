#Requires -Version 5.1
# Checks #848 on the cluster: no loader pod, loading script or load fails silently
# (dev/plan-848-no-silent-load-failures.md, section 4).
#
# Before: bexhoma must be installed from the branch no-silent-load-failures
# (pip install . in the repository), and the loader/generator images rebuilt.
#
# Part A - clean loads: the new checks must not raise false alarms.
#   Per log: "TEST passed: Loader pods without errors", "TEST passed: Loading completed
#   without failures", "TEST passed: Init scripts without errors"; summary section
#   "Ingestion" lists every configuration with all units ok. In the result folder, the
#   loader logs (bexhoma-loading-*.sensor.log / *.datagenerator.log) carry
#   BEXHOMA_INGEST:<file>:<expected>:<reported>:ok lines, expected == reported
#   (ClickHouse: reported empty; Benchbase: both empty; HammerDB: warehouses = SF).
#   A failed unit here is a false alarm or a real problem: look at the line in the
#   loader log (wc -l vs. the reply of the load statement).
# Part B - -xld with --set:
#   B1/B2 relaxed + --set synchronous_commit=on: durability-relaxed stdout log shows
#     {synchronous_commit=off} for the database, restoredurability-relaxed shows no database
#     setting left; no ERROR in the durability logs; Citus: the worker check passes.
#   B3 unsafe + --set fsync=on: refused before loading ("-xld unsafe cannot take effect:
#     fsync=on (--set), the load needs off"), experiment aborted, no loader job.
# Part C - a load that fails (TPC-H PostgreSQL SF 2 on its own volume, no other run uses it):
#   C1 the SUT container is killed during the ingest: loader pods fail and are not retried
#     (backoffLimit 0), the experiment aborts with diagnostics, TEST failed: Loader pods
#     without errors / Loading completed ...; the volume keeps loaded=False.
#   C2 the same command without -rsr: refused ("holds an unfinished load ... remove it (-rsr)").
#   C3 with -rsr: loads cleanly, volume loaded=True; -rsr removes the volume of C1/C2 first.
#
# Run from the repository root: .\dev\test-loading-failures.ps1
# Resume at a step (all steps before it are skipped):
#   .\dev\test-loading-failures.ps1 -StartAt A4-MariaDB
# Steps: A1 A2 A3 A4-PostgreSQL A4-MySQL A4-MariaDB A4-MonetDB A5 A6 A7 B1 B2 B3 C
# (C1-C3 depend on each other and run as one step). Stopped in the middle of a run:
# remove its leftovers first with  bexhoma stop -e <code>  (the code is in its log).
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

param([string]$StartAt = '')

$STEPS = @('A1', 'A2', 'A3', 'A4-PostgreSQL', 'A4-MySQL', 'A4-MariaDB', 'A4-MonetDB',
           'A5', 'A6', 'A7', 'B1', 'B2', 'B3', 'C')
if ($StartAt -and $STEPS -notcontains $StartAt) {
    Write-Host "unknown step $StartAt (steps: $($STEPS -join ', '))"
    exit 1
}
$script:started = -not $StartAt

function Test-Step([string]$Name) {
    # true from the step -StartAt names on (always without -StartAt)
    if ($Name -eq $StartAt) { $script:started = $true }
    if (-not $script:started) { Write-Host "skipping $Name" }
    return $script:started
}

. .\scripts\testfunctions.ps1

# the installed bexhoma must have the #848 code
python -c "import bexhoma.loading_checks" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "bexhoma without #848 (bexhoma.loading_checks missing): run 'pip install .' on branch no-silent-load-failures first"
    exit 1
}

function Write-Done([string]$Name) {
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $Name"
}


###########################################
######## A. Clean loads (false alarms) ####
###########################################

if (Test-Step 'A1') {
    #### A1 TPC-H, all loader images
    bexhoma tpch `
      -dbms PostgreSQL MySQL MariaDB MonetDB ClickHouse <# every TPC-H loader image #> `
      -sf 1                         <# scaling factor #> `
      -nlp 8                        <# number of data loader pods #> `
      -xii                          <# create indexes after loading #> `
      -xic                          <# create constraints after loading #> `
      -xis                          <# recompute statistics after loading #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_tpch_load.log" -Encoding utf8
    Write-Done "A1 TPC-H load"
}

if (Test-Step 'A2') {
    #### A2 TPC-DS, all loader images and the dsdgen check
    bexhoma tpcds `
      -dbms PostgreSQL MySQL MariaDB MonetDB ClickHouse <# every TPC-DS loader image #> `
      -sf 1                         <# scaling factor #> `
      -nlp 8                        <# number of data loader pods #> `
      -xii                          <# create indexes after loading #> `
      -xic                          <# create constraints after loading #> `
      -xis                          <# recompute statistics after loading #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_tpcds_load.log" -Encoding utf8
    Write-Done "A2 TPC-DS load"
}

if (Test-Step 'A3') {
    #### A3 SSB, all loader images (markers only, they failed loudly already)
    bexhoma ssb `
      -dbms PostgreSQL MySQL MariaDB MonetDB ClickHouse <# every SSB loader image #> `
      -sf 1                         <# scaling factor #> `
      -nlp 8                        <# number of data loader pods #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_ssb_load.log" -Encoding utf8
    Write-Done "A3 SSB load"
}

#### A4 TPC-H refresh stream, one run per refresh loader image (all DBMS of a run share one job)
foreach ($dbms in @('PostgreSQL', 'MySQL', 'MariaDB', 'MonetDB')) {
    if (Test-Step "A4-$dbms") {
        bexhoma tpch `
          -dbms $dbms                   <# refresh loader image of this DBMS #> `
          -sf 1                         <# scaling factor #> `
          -ne 1                         <# one client round #> `
          -nlp 8                        <# number of data loader pods #> `
          -xii                          <# create indexes after loading (without them Q17/Q20 run into the query timeout) #> `
          -xrs 1                        <# one RF1/RF2 pair: BEXHOMA_INGEST rf1-orders-1, rf1-lineitem-1, rf2-1 ok #> `
          -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
          -tr                           <# verify result meets basic sanity requirements #> `
          -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
          -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
          -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
          run 2>&1 | Out-File "$LOG_DIR\test_848_tpch_refresh_$($dbms.ToLower()).log" -Encoding utf8
        Write-Done "A4 TPC-H refresh $dbms"
    }
}

if (Test-Step 'A5') {
    #### A5 YCSB generator: [INSERT] OK count = insertcount of the pod
    bexhoma ycsb `
      -dbms PostgreSQL              <# DBMS under test #> `
      -sf 1                         <# one million records #> `
      -xwl a                        <# workload #> `
      -nlp 4                        <# number of data loader pods: BEXHOMA_INGEST usertable-1..4 #> `
      -nlt 64                       <# threads per loader pod #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_ycsb_load.log" -Encoding utf8
    Write-Done "A5 YCSB load"
}

if (Test-Step 'A6') {
    #### A6 Benchbase generator: exit code, "Finished loading data into", no [ERROR line
    bexhoma benchbase `
      -dbms PostgreSQL              <# DBMS under test #> `
      -sf 16                        <# warehouses #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_benchbase_load.log" -Encoding utf8
    Write-Done "A6 Benchbase load"
}

if (Test-Step 'A7') {
    #### A7 HammerDB generator: SCHEMA COMPLETE, warehouses = SF
    bexhoma hammerdb `
      -dbms PostgreSQL              <# DBMS under test #> `
      -sf 16                        <# warehouses: BEXHOMA_INGEST:warehouses:16:16:ok #> `
      -nlt 16                       <# virtual users of the schema build #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -ks no                        <# remove the SUT at the end #> `
      load 2>&1 | Out-File "$LOG_DIR\test_848_hammerdb_load.log" -Encoding utf8
    Write-Done "A7 HammerDB load"
}


###########################################
######## B. -xld with --set ###############
###########################################

if (Test-Step 'B1') {
    #### B1 relaxed load, synchronous benchmark (PostgreSQL)
    bexhoma tpch `
      -dbms PostgreSQL              <# DBMS under test #> `
      -sf 1                         <# scaling factor #> `
      -ne 1                         <# one client round #> `
      -nlp 8                        <# number of data loader pods #> `
      -xii                          <# create indexes after loading #> `
      -xic                          <# create constraints after loading #> `
      -xis                          <# recompute statistics after loading #> `
      -xld relaxed                  <# load with synchronous_commit=off (per database) #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -tr                           <# verify result meets basic sanity requirements #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on <# benchmark with synchronous commits #> `
      run 2>&1 | Out-File "$LOG_DIR\test_848_xld_relaxed_set_sync_postgresql.log" -Encoding utf8
    Write-Done "B1 -xld relaxed --set synchronous_commit=on PostgreSQL"
}

if (Test-Step 'B2') {
    #### B2 the same on Citus (coordinator and workers)
    bexhoma tpch `
      -dbms Citus                   <# DBMS under test #> `
      -sf 1                         <# scaling factor #> `
      -ne 1                         <# one client round #> `
      -nlp 8                        <# number of data loader pods #> `
      -nw 2                         <# number of worker nodes #> `
      -nwr 1                        <# replication factor #> `
      -nws 48                       <# number of shards #> `
      -xii                          <# create indexes after loading #> `
      -xic                          <# create constraints after loading #> `
      -xis                          <# recompute statistics after loading #> `
      -xld relaxed                  <# load with synchronous_commit=off (per database, also on the workers) #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -tr                           <# verify result meets basic sanity requirements #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      -rnw $BEXHOMA_NODES_WORKER    <# schedule worker pods on these nodes #> `
      --set deployment[bexhoma-deployment-citus].container[dbms].synchronous_commit=on <# coordinator: benchmark with synchronous commits #> `
      run 2>&1 | Out-File "$LOG_DIR\test_848_xld_relaxed_set_sync_citus.log" -Encoding utf8
    Write-Done "B2 -xld relaxed --set synchronous_commit=on Citus"
}

if (Test-Step 'B3') {
    #### B3 unsafe load with fsync fixed on the command line: refused before loading
    bexhoma tpch `
      -dbms PostgreSQL              <# DBMS under test #> `
      -sf 1                         <# scaling factor #> `
      -ne 1                         <# one client round #> `
      -xld unsafe                   <# needs fsync=off, which --set fixes to on #> `
      -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
      -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
      -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
      -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
      --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on <# server-wide: conflicts with -xld unsafe #> `
      run 2>&1 | Out-File "$LOG_DIR\test_848_xld_unsafe_set_fsync_refused.log" -Encoding utf8
    Write-Done "B3 -xld unsafe --set fsync=on (refused)"
}


###########################################
######## C. A load that fails #############
###########################################

if (Test-Step 'C') {
    # TPC-H PostgreSQL SF 2 on nvme: volume bexhoma-storage-postgresql-nvme-tpch-2, used by no other run
    $C_ARGS = @(
      'tpch',
      '-dbms', 'PostgreSQL',
      '-sf', '2',
      '-nlp', '8',
      '-xii', '-xic', '-xis',
      '-rst', $BEXHOMA_STORAGE_CLASS, '-rss', '20Gi',
      '-ms', "$BEXHOMA_MS",
      '-rnn', $BEXHOMA_NODE_SUT, '-rnl', $BEXHOMA_NODE_LOAD, '-rnb', $BEXHOMA_NODE_BENCHMARK,
      '-ks', 'no'
    )

    #### C1 kill the SUT container during the ingest
    $log = "$LOG_DIR\test_848_tpch_sut_killed_during_ingest.log"
    $logAbsolute = Join-Path (Resolve-Path $LOG_DIR).Path 'test_848_tpch_sut_killed_during_ingest.log'
    $job = Start-Job -ScriptBlock {
        param($dir, $arguments, $logfile)
        Set-Location $dir
        & bexhoma @arguments -rsr load 2>&1 | Out-File $logfile -Encoding utf8
    } -ArgumentList (Get-Location).Path, $C_ARGS, $logAbsolute
    # the experiment code from the log, so that only this run's SUT is killed
    $code = $null
    while (-not $code -and $job.State -eq 'Running') {
        Start-Sleep -Seconds 10
        if (Test-Path $log) {
            $m = Select-String -Path $log -Pattern 'has code (\d+)' | Select-Object -First 1
            if ($m) { $code = $m.Matches[0].Groups[1].Value }
        }
    }
    # wait until its loader pods are ingesting, then kill the DBMS process of its SUT
    $killed = $false
    while (-not $killed -and $job.State -eq 'Running') {
        Start-Sleep -Seconds 10
        $loaders = kubectl get pods -l "app=bexhoma,component=loading,experiment=$code" --field-selector=status.phase=Running -o name
        if ($loaders) {
            Start-Sleep -Seconds 20
            $sut = kubectl get pods -l "app=bexhoma,component=sut,experiment=$code" -o name | Select-Object -First 1
            Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') killing the DBMS in $sut (experiment $code) during the ingest"
            kubectl exec $sut -c dbms -- bash -c "kill 1"
            $killed = $true
        }
    }
    Wait-Job $job | Out-Null
    Remove-Job $job
    kubectl get pvc bexhoma-storage-postgresql-nvme-tpch-2 -L loaded,loading_failed
    Write-Done "C1 SUT killed during the ingest (experiment $code; expected: aborted, tests failed, volume loaded=False)"

    #### C2 the same without -rsr: the unfinished volume is refused
    & bexhoma @C_ARGS load 2>&1 | Out-File "$LOG_DIR\test_848_tpch_unfinished_volume_refused.log" -Encoding utf8
    Write-Done "C2 unfinished volume (expected: refused, remove it (-rsr))"

    #### C3 with -rsr: a clean load on a new volume
    & bexhoma @C_ARGS -rsr load 2>&1 | Out-File "$LOG_DIR\test_848_tpch_reload_after_failure.log" -Encoding utf8
    kubectl get pvc bexhoma-storage-postgresql-nvme-tpch-2 -L loaded,loading_failed
    Write-Done "C3 reload with -rsr (expected: tests passed, volume loaded=True)"
}
