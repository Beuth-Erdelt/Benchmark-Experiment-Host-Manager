#Requires -Version 5.1
# Compares PostgreSQL 18 defaults against workload-tuned configurations,
# per benchmark, on a SUT sized to 16 cores / 128Gi RAM (the SUT container
# itself requests/limits 14 cores / 112Gi, leaving headroom for the OS,
# kubelet, and monitoring sidecars on the node).
#
# Five workloads, two variants each (Default = stock PostgreSQL 18 GUCs,
# Tuned = the --set overrides below): ycsb, benchbase tpcc, hammerdb tpcc,
# tpch, tpcds. Every other parameter (storage class, resources, scale
# factor, duration, node pinning) is held identical between Default and
# Tuned for the same workload, so the only variable under test is the
# PostgreSQL configuration itself.
#
# Storage class per workload group follows dev/test-storage-oltp-olap.ps1's
# round-3 (interleaved) findings, not round 1/2's:
#   - OLTP (ycsb, benchbase tpcc, hammerdb tpcc) -> shared. The only fio
#     finding that reproduced in all three storage rounds (4 confirmations)
#     is cephcsi collapsing under fsync'd random-write contention at every
#     queue depth - exactly the access pattern these three workloads
#     generate continuously.
#   - OLAP (tpch, tpcds) -> cephcsi. Round 2's "cephcsi is faster at
#     sequential reads" lean, which originally justified this, reversed in
#     round 3 and should NOT be relied on. What still holds after 3
#     confirmations is shared's write-size cliff above ~4-6M blocks; TPC-H/
#     TPC-DS loading issues large sequential COPY writes that land in
#     exactly that range, so cephcsi remains the safer pick for the load
#     phase even though query-time read throughput is now a toss-up.
#
# Each workload's Default and Tuned runs execute back to back (not grouped
# by variant across all five workloads) for the same reason interleaving
# mattered for the storage comparison: cluster-load drift over a multi-hour
# script should not be confounded with the setting being compared.
#
# Every round uses -rsr so Default and Tuned each start from a freshly
# loaded database - otherwise Tuned could inherit autovacuum/bloat/cache
# state left behind by Default's run and the comparison would be biased.
#
# This script does not sweep scale factors, client counts, or throughput
# targets - each workload runs at one fixed, "realistic for this box" size
# (see the comment above each function) so the two variants are cheap
# enough to compare directly. Expect several hours total; TPC-H/TPC-DS
# loading at these scale factors is the dominant cost.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

$BEXHOMA_STORAGE_CLASS_OLTP = "shared"
$BEXHOMA_STORAGE_CLASS_OLAP = "cephcsi"

# SUT sizing for the "16 cores / 128Gi" target node; request=limit avoids
# the cgroup-throttling jitter found during the hardware CPU-quota
# calibration work - leaves ~2 cores / ~16Gi of the node for the OS,
# kubelet, and monitoring sidecars.
$BEXHOMA_SUT_CPU = 14
$BEXHOMA_SUT_RAM = "112Gi"




###########################################
################## YCSB ###################
###########################################
# Workload B (read-mostly, 95/5): the representative default; workload A
# (50/50) is the write-stress alternative if you want to re-run with -xwl a.
# -sf 50 is a "meaningful mid-size" record count for this box, not a
# calibrated GB figure - YCSB's own -sf semantics (rows vs. GB) aren't
# precisely documented in the shared base parser, so treat this as a
# starting point to size against your actual per-record footprint rather
# than a target you can assume lands at a specific dataset size.
# -xmet 300 caps the benchmarking phase at 5 minutes so the two variants
# stay cheap to compare; raise it if you want steadier throughput numbers.

function Test-YcsbDefault {
    <#
    .SYNOPSIS
    YCSB with stock PostgreSQL 18 defaults (no --set overrides).
    #>
    bexhoma ycsb `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 50                           <# scale factor: record count, see note above #> `
      -xwl b                           <# YCSB workload B: read-mostly (95/5) #> `
      -xtb 16384                       <# base ops/sec target #> `
      -xnbf 1                          <# benchmarking target factor, fixed (no sweep) #> `
      -xnlf 1                          <# loading target factor, fixed (no sweep) #> `
      -xmet 300                        <# cap benchmarking phase at 5 minutes #> `
      -nlp 4                           <# loading pods #> `
      -nlt 16                          <# loading threads per pod #> `
      -nbp 2                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking threads per pod (64 total client threads) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -ne 1                            <# parallel client counts (no sweep) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 100Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      run 2>&1 | Out-File "$LOG_DIR\pg18_ycsb_default.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB default  sf=50  wl=b"
}

function Test-YcsbTuned {
    <#
    .SYNOPSIS
    YCSB with the OLTP-tuned PostgreSQL 18 settings.
    #>
    bexhoma ycsb `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 50                           <# scale factor: record count, matches default variant #> `
      -xwl b                           <# YCSB workload B: read-mostly (95/5) #> `
      -xtb 16384                       <# base ops/sec target #> `
      -xnbf 1                          <# benchmarking target factor, fixed (no sweep) #> `
      -xnlf 1                          <# loading target factor, fixed (no sweep) #> `
      -xmet 300                        <# cap benchmarking phase at 5 minutes #> `
      -nlp 4                           <# loading pods #> `
      -nlt 16                          <# loading threads per pod #> `
      -nbp 2                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking threads per pod (64 total client threads) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -ne 1                            <# parallel client counts (no sweep) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 100Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=4.0 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=1 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_sync_method=fdatasync `
      --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=28GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=84GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=32MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=200 `
      run 2>&1 | Out-File "$LOG_DIR\pg18_ycsb_tuned.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB tuned  sf=50  wl=b"
}


###########################################
############ Benchbase TPC-C ##############
###########################################
# -sf 160 warehouses matches dev/pg-storage.ps1's existing PG18 tuning
# precedent and the ~10 warehouses/core rule of thumb for a 16-core box.
# -nbt 32 (2x cores) instead of the docs example's 160 terminals, which
# targets a much larger cluster than this one.

function Test-BenchbaseTpccDefault {
    <#
    .SYNOPSIS
    Benchbase TPC-C with stock PostgreSQL 18 defaults (no --set overrides).
    #>
    bexhoma benchbase `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 160                          <# scale factor: TPC-C warehouses #> `
      -xbt tpcc                        <# Benchbase benchmark suite: TPC-C (also the default) #> `
      -xsd 10                          <# benchmark duration in minutes #> `
      -xtb 1024                        <# base ops/sec target #> `
      -xnbf 1                          <# benchmarking target factor, fixed (no sweep) #> `
      -nbp 1                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking terminals/threads #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 80Gi                        <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      run 2>&1 | Out-File "$LOG_DIR\pg18_benchbase_tpcc_default.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase TPC-C default  sf=160  terminals=32"
}

function Test-BenchbaseTpccTuned {
    <#
    .SYNOPSIS
    Benchbase TPC-C with the OLTP-tuned PostgreSQL 18 settings.
    #>
    bexhoma benchbase `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 160                          <# scale factor: TPC-C warehouses, matches default variant #> `
      -xbt tpcc                        <# Benchbase benchmark suite: TPC-C (also the default) #> `
      -xsd 10                          <# benchmark duration in minutes #> `
      -xtb 1024                        <# base ops/sec target #> `
      -xnbf 1                          <# benchmarking target factor, fixed (no sweep) #> `
      -nbp 1                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking terminals/threads #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 80Gi                        <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=4.0 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=16 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_sync_method=fdatasync `
      --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=28GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=84GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=100 `
      run 2>&1 | Out-File "$LOG_DIR\pg18_benchbase_tpcc_tuned.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase TPC-C tuned  sf=160  terminals=32"
}


###########################################
############# HammerDB TPC-C ##############
###########################################
# Same warehouses/terminal counts as the Benchbase TPC-C variant above so
# the two TPC-C tools are as close to apples-to-apples as their different
# CLIs allow. HammerDB has no benchmark-type flag - it only ever runs
# TPC-C, unlike Benchbase's -xbt.

function Test-HammerdbTpccDefault {
    <#
    .SYNOPSIS
    HammerDB TPC-C with stock PostgreSQL 18 defaults (no --set overrides).
    #>
    bexhoma hammerdb `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 160                          <# scale factor: TPC-C warehouses #> `
      -xsd 10                          <# benchmark duration in minutes #> `
      -xrt 2                           <# ramp-up period in minutes #> `
      -nlt 16                          <# loading virtual users #> `
      -nbp 1                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking virtual users/terminals #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -ne 1                            <# parallel client counts (no sweep) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 80Gi                        <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      run 2>&1 | Out-File "$LOG_DIR\pg18_hammerdb_tpcc_default.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB TPC-C default  sf=160  vusers=32"
}

function Test-HammerdbTpccTuned {
    <#
    .SYNOPSIS
    HammerDB TPC-C with the OLTP-tuned PostgreSQL 18 settings.
    #>
    bexhoma hammerdb `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 160                          <# scale factor: TPC-C warehouses, matches default variant #> `
      -xsd 10                          <# benchmark duration in minutes #> `
      -xrt 2                           <# ramp-up period in minutes #> `
      -nlt 16                          <# loading virtual users #> `
      -nbp 1                           <# benchmarking pods #> `
      -nbt 32                          <# benchmarking virtual users/terminals #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -ne 1                            <# parallel client counts (no sweep) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 80Gi                        <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLTP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=4.0 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=16 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_sync_method=fdatasync `
      --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=28GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=84GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=100 `
      run 2>&1 | Out-File "$LOG_DIR\pg18_hammerdb_tpcc_tuned.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB TPC-C tuned  sf=160  vusers=32"
}


###########################################
################# TPC-H ####################
###########################################
# -sf 100 (~100GB raw) exceeds shared_buffers but not effective_cache_size
# on this box, matching the experiment_dict precedent already used in this
# repo. -ne 1,4 covers both a power test (single stream, one query gets the
# whole box) and a throughput test (4 concurrent streams).

function Test-TpchDefault {
    <#
    .SYNOPSIS
    TPC-H with stock PostgreSQL 18 defaults (no --set overrides).
    #>
    bexhoma tpch `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 100                          <# scale factor #> `
      -nlp 8                           <# loading pods #> `
      -nlt 8                           <# loading threads per pod #> `
      -xii                             <# create indexes after loading #> `
      -xic                             <# add primary/foreign-key constraints after loading #> `
      -xis                             <# run ANALYZE after loading #> `
      -xqr 1                           <# query repeats #> `
      -ne 1,4                          <# parallel query streams: power test (1) and throughput test (4) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 200Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLAP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      run 2>&1 | Out-File "$LOG_DIR\pg18_tpch_default.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H default  sf=100  streams=1,4"
}

function Test-TpchTuned {
    <#
    .SYNOPSIS
    TPC-H with the OLAP-tuned PostgreSQL 18 settings.
    #>
    bexhoma tpch `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 100                          <# scale factor, matches default variant #> `
      -nlp 8                           <# loading pods #> `
      -nlt 8                           <# loading threads per pod #> `
      -xii                             <# create indexes after loading #> `
      -xic                             <# add primary/foreign-key constraints after loading #> `
      -xis                             <# run ANALYZE after loading #> `
      -xqr 1                           <# query repeats #> `
      -ne 1,4                          <# parallel query streams: power test (1) and throughput test (4) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 200Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLAP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=4 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=14 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=16 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=36GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=96GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=4GB `
      run 2>&1 | Out-File "$LOG_DIR\pg18_tpch_tuned.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H tuned  sf=100  streams=1,4"
}


###########################################
################# TPC-DS ###################
###########################################
# -sf 50, smaller than TPC-H's 100: TPC-DS carries more tables and a
# heavier per-row footprint at the same nominal scale factor, so this stays
# conservative for a first comparison run. -t 1800 caps overall experiment
# time since TPC-DS's query mix runs noticeably longer than TPC-H's under
# stock (untuned) settings.

function Test-TpcdsDefault {
    <#
    .SYNOPSIS
    TPC-DS with stock PostgreSQL 18 defaults (no --set overrides).
    #>
    bexhoma tpcds `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 50                           <# scale factor #> `
      -nlp 8                           <# loading pods #> `
      -nlt 8                           <# loading threads per pod #> `
      -xii                             <# create indexes after loading #> `
      -xic                             <# add primary/foreign-key constraints after loading #> `
      -xis                             <# run ANALYZE after loading #> `
      -xqr 1                           <# query repeats #> `
      -ne 1,4                          <# parallel query streams: power test (1) and throughput test (4) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -t 1800                          <# overall experiment timeout in seconds #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 150Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLAP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      run 2>&1 | Out-File "$LOG_DIR\pg18_tpcds_default.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS default  sf=50  streams=1,4"
}

function Test-TpcdsTuned {
    <#
    .SYNOPSIS
    TPC-DS with the OLAP-tuned PostgreSQL 18 settings.
    #>
    bexhoma tpcds `
      -dbms PostgreSQL                 <# hardware target(s) to test #> `
      -sf 50                           <# scale factor, matches default variant #> `
      -nlp 8                           <# loading pods #> `
      -nlt 8                           <# loading threads per pod #> `
      -xii                             <# create indexes after loading #> `
      -xic                             <# add primary/foreign-key constraints after loading #> `
      -xis                             <# run ANALYZE after loading #> `
      -xqr 1                           <# query repeats #> `
      -ne 1,4                          <# parallel query streams: power test (1) and throughput test (4) #> `
      -nc 1                            <# repetitions (single measurement) #> `
      -m                               <# collect SUT resource metrics #> `
      -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
      -t 1800                          <# overall experiment timeout in seconds #> `
      -tr                              <# verify result meets basic sanity requirements #> `
      -rsr                             <# delete any existing PVC, so each variant starts from a clean, freshly loaded DB #> `
      -rss 150Gi                       <# size of the persistent volume claim #> `
      -rst $BEXHOMA_STORAGE_CLASS_OLAP <# storage class for persistent volumes #> `
      -rc $BEXHOMA_SUT_CPU -lc $BEXHOMA_SUT_CPU   <# SUT CPU request/limit #> `
      -rr $BEXHOMA_SUT_RAM -lr $BEXHOMA_SUT_RAM   <# SUT RAM request/limit #> `
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
      --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=4 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=14 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=16 `
      --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=36GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=96GB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=768MB `
      --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=4GB `
      run 2>&1 | Out-File "$LOG_DIR\pg18_tpcds_tuned.log" -Encoding utf8

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS tuned  sf=50  streams=1,4"
}


###########################################
############### Driver loop ###############
###########################################
# Default -> Tuned per workload, not grouped by variant across all five
# workloads - keeps cluster-load drift from being confounded with the
# setting being compared, same reasoning as
# dev/test-storage-oltp-olap.ps1's interleaved driver loop.

$tests = @(
    @('Test-YcsbDefault',          'Test-YcsbTuned'),
    @('Test-BenchbaseTpccDefault', 'Test-BenchbaseTpccTuned'),
    @('Test-HammerdbTpccDefault',  'Test-HammerdbTpccTuned'),
    @('Test-TpchDefault',          'Test-TpchTuned'),
    @('Test-TpcdsDefault',         'Test-TpcdsTuned')
)

foreach ($pair in $tests) {
    foreach ($testName in $pair) {
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [START] $testName"
        & $testName
    }
}


###########################################
############## Clean Folder ###############
###########################################

Invoke-CleanLogs
