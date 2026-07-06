#Requires -Version 5.1
# Compares the "cephcsi" and "shared" storage classes for PostgreSQL-shaped
# OLTP and OLAP I/O patterns, using the Hardware (fio) benchmark.
#
# This is a dev/ exploration script, not one of the documentation-generating
# scripts in scripts/ - see docs/Example-Hardware.md and
# scripts/test-docs-hardware.ps1 for the reference sweeps this one is built
# on top of. Every fio profile below runs once per storage class in
# $BEXHOMA_STORAGE_CLASSES, so results are directly comparable pair-by-pair
# (same profile, same duration, only -rst differs).
#
# All fio rounds share the Hardware-1 SUT/PVC and must run strictly
# sequentially (see project notes on -rsr and PVC sharing in
# docs/Example-Hardware.md) - this script relies on the synchronous
# `... | Out-File` pipe to block until each round's bexhoma process exits
# before starting the next one, exactly like scripts/test-docs-hardware.ps1.
#
# Revision 2 adds an ANOMALY DIAGNOSTICS block per storage class, following
# up on two findings from the first run (see logs_tests/local/*_summary.md):
#   - cephcsi collapses under the OLTP contention proxy (randrw 70/30, 8k,
#     depth 64, fsync=1): ~66/29 iops at ~2.4-2.9s p95/p99 latency, versus
#     shared's 519/221 iops at sub-second latency - the inverse of every
#     other OLTP result on this cluster.
#   - shared collapses at 16M sequential writes: ~1.1-1.2 iops at 4-13s
#     p99 latency, versus cephcsi's 9-30 iops - while the two classes are
#     within a few percent of each other at 1M and 4M.
# The diagnostic profiles below decompose each anomaly along the axes most
# likely to explain it (fio ioengine, queue depth, read/write mix, fsync
# on/off) instead of accepting each as a single unexplained data point.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

$BEXHOMA_STORAGE_CLASSES = @("cephcsi", "shared")




###########################################
######## OLTP vs. OLAP storage compare ####
###########################################
# Each profile below is run once per entry of $BEXHOMA_STORAGE_CLASSES. The
# OLTP block uses PostgreSQL's 8k page size (BLCKSZ) with random access and
# latency-sensitive WAL/commit patterns; the OLAP block uses large sequential
# blocks approximating seq scans, bulk loads, and checkpoint writeback.

foreach ($storageClass in $BEXHOMA_STORAGE_CLASSES) {

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [START] Storage class: $storageClass"


###########################################
################## OLTP ###################
###########################################


#### OLTP 1. Queue-depth sweep at PostgreSQL's page size (8k)
# Extended to 256 (was 1..128): the first run showed IOPS still climbing at
# 128 for both classes with no elbow, so 128 wasn't the ceiling - one more
# doubling step checks whether 256 finds it.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 1,2,4,8,16,32,64,128,256   <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_depth_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP depth sweep  rw=randread,randwrite  bs=8k  iodepth=1..256"


#### OLTP 2. random_page_cost calibration (sequential vs. random read)
# Extended to 4 depths (was depth=64 only): the seq/random ratio is the
# basis for a random_page_cost recommendation, so it should hold across
# depths before being trusted, not rest on a single point.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read,randread              <# sequential vs. random read (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 1,16,64,128                <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_random_page_cost.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP random_page_cost calibration  rw=read,randread  iodepth=1,16,64,128"


#### OLTP 3. WAL sync-write commit latency (fsync)
# Added -nc 3: this single-round number anchors every later commit-latency
# comparison, and the first run measured it once.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (wal_sync_method=fsync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (single backend) #> `
  -nc 3                            <# repeat 3x: single-shot commit latency is noisy #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_wal_sync_fsync.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL sync-write fsync  bs=8k  iodepth=1  x3"


#### OLTP 4. WAL sync-write commit latency (fdatasync)
# Added -nc 3, same reasoning as test 3.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xffd 1                          <# fdatasync after every write (wal_sync_method=fdatasync, PostgreSQL's Linux default) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (single backend) #> `
  -nc 3                            <# repeat 3x: single-shot commit latency is noisy #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_wal_sync_fdatasync.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL sync-write fdatasync  bs=8k  iodepth=1  x3"


#### OLTP 5. WAL group-commit scaling (concurrent committing backends)
# Added -nc 3: the first run showed a noisy, non-monotonic cephcsi curve
# (51->16.6->93->82->137->391 iops across nbt=1..32) that looks like the same
# concurrent-fsync instability as the contention-proxy collapse (test 8),
# not just measurement noise - worth confirming with repetition before
# concluding shared scales better here.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write per thread) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (wal_sync_method=fsync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1,2,4,8,16,32               <# concurrent committing backends to sweep (comma-separated) #> `
  -nc 3                            <# repeat 3x: first run was noisy/non-monotonic for cephcsi #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 150Gi                       <# fio makes one -xts-sized file per backend; 32*4G=128G peak, so 50Gi is not enough #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_wal_group_commit.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL group commit  bs=8k  iodepth=1  backends=1..32  x3"


#### OLTP 6. Mixed read/write contention proxy (foreground OLTP vs. WAL flush)
# Unchanged from the first run - kept as the fixed reference point that the
# anomaly diagnostics below (tests 7-9) decompose.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 70                         <# read percentage: 70% OLTP reads, 30% WAL-like writes #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found in the depth sweep #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (approximates WAL flush contention) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_contention_proxy.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP contention proxy  randrw 70/30  bs=8k  iodepth=64"


###########################################
##### OLTP contention anomaly diagnostics #
###########################################
# cephcsi collapsed on test 6 (~66/29 iops, ~2.4-2.9s p95/p99) while shared
# stayed healthy (519/221 iops, sub-second latency) - the inverse of every
# other OLTP result. The three profiles below each vary one axis of test 6
# to find what specifically triggers it.


#### OLTP 7. Contention: fio ioengine sweep
# Rules out a fio/libaio artifact before blaming the storage backend: if
# io_uring doesn't collapse the same way at the same parameters, the finding
# is "libaio handles this contention pattern badly on cephcsi", not "cephcsi
# is bad under contention".
# sync is deliberately excluded: fio's sync ioengine has no queue, so
# combining it with -xfid 64 is an invalid pairing, not a real third
# comparison point - the first run of this test produced 0.00 for every
# metric on both storage classes and tripped -tr's zero-IOPS check (see
# images/hardware/benchmarker/run_fio.sh, which now logs fio's exit code and
# stderr and validates its JSON before parsing, so a repeat of this mistake
# fails loudly instead of silently). A synchronous single-outstanding-request
# baseline already exists at its own natural depth in tests 3/4 (WAL fsync/
# fdatasync, -xfid 1); it does not belong in a depth=64 comparison.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 70                         <# read percentage, matches test 6 #> `
  -xfbs 8k                         <# fio block size, matches test 6 #> `
  -xfid 64                         <# queue depth, matches test 6 #> `
  -xfe libaio,io_uring             <# ioengines to sweep (comma-separated); sync excluded, see comment above #> `
  -xfsy 1                          <# fsync after every write, matches test 6 #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -mc                              <# collect node-level cluster metrics: check for a CPU-side signal #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_contention_engine_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP contention engine sweep  engine=libaio,io_uring"


#### OLTP 8. Contention: queue-depth sweep
# Finds whether the collapse appears gradually or only past some depth -
# test 6 only sampled depth=64.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 70                         <# read percentage, matches test 6 #> `
  -xfbs 8k                         <# fio block size, matches test 6 #> `
  -xfid 1,4,16,32,64,128           <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 0,1                        <# with and without fsync: isolates whether fsync is required to trigger it #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -mc                              <# collect node-level cluster metrics: check for a CPU-side signal #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_contention_depth_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP contention depth sweep  iodepth=1..128  fsync=0,1"


#### OLTP 9. Contention: read/write mix sweep
# Finds how much write fraction is needed to trigger the collapse - sweeps
# from all-read (100, should match test 1's randread) to all-write (0,
# should match test 1's randwrite), crossed with fsync on/off.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 100,90,70,50,30,10,0       <# read percentages to sweep, all-read to all-write (comma-separated) #> `
  -xfbs 8k                         <# fio block size, matches test 6 #> `
  -xfid 64                         <# queue depth, matches test 6 #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 0,1                        <# with and without fsync (comma-separated) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -mc                              <# collect node-level cluster metrics: check for a CPU-side signal #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_oltp_contention_mix_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP contention mix sweep  rwmixread=0..100  fsync=0,1"


###########################################
################## OLAP ###################
###########################################


#### OLAP 1. Sequential-read block-size sweep (seq-scan throughput curve)
# Extended down to 16k (was 64k..16M): 16k-128k is PostgreSQL 17+'s real
# io_combine_limit range (default 128kB) for prefetched sequential-scan
# reads, so this now covers the sizes Postgres itself can actually request,
# not just an OS-readahead proxy. Also extended up to 64M to check whether
# shared's 16M write cliff (OLAP test 4) has a read-side counterpart at
# larger sizes still - the first run found no cliff on the read side up to
# 16M.
# Added -nc 3: this test ran once per storage class in round 2 and its
# cephcsi-vs-shared lean was cited in the PostgreSQL config recommendations -
# repeat it before trusting that lean, the same way group-commit's repeated
# numbers overturned round 1's single-shot conclusion there.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read                       <# sequential read, simulating a large table/seq scan #> `
  -xfbs 16k,32k,64k,128k,256k,1M,4M,16M,32M,64M <# block sizes to sweep (comma-separated) #> `
  -xfid 16                         <# queue depth, fixed (enough to keep a sequential reader saturated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs), fixed #> `
  -nc 3                            <# repeat 3x: this test's lean was cited in downstream recommendations #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_seqread_blocksize_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP seq-read block-size sweep  bs=16k..64M  iodepth=16  x3"


#### OLAP 2. Sequential-read queue-depth sweep (readahead effectiveness)
# Extended to 64,128 (was 1..32): neither class had plateaued by depth 32 in
# the first run.
# Added -nc 3, same reasoning as OLAP test 1.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read                       <# sequential read, simulating a large table/seq scan #> `
  -xfbs 1M                         <# fio block size, fixed at a throughput-bound size found in the block-size sweep #> `
  -xfid 1,2,4,8,16,32,64,128       <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs), fixed #> `
  -nc 3                            <# repeat 3x: this test's lean was cited in downstream recommendations #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_seqread_depth_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP seq-read depth sweep  bs=1M  iodepth=1..128  x3"


#### OLAP 3. Parallel sequential-scan proxy (concurrent scan workers)
# Added -nc 3: unchanged parameters from round 1, but its "cephcsi scales
# better past 2 workers" finding was cited in the PostgreSQL config
# recommendations (max_parallel_workers_per_gather) - same repeat-before-trust
# reasoning as OLAP tests 1-2.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read                       <# sequential read, simulating a large table/seq scan #> `
  -xfbs 1M                         <# fio block size, fixed at a throughput-bound size found in the block-size sweep #> `
  -xfid 16                         <# queue depth, fixed (enough to keep each reader saturated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1,2,4,8                     <# concurrent scan workers to sweep (comma-separated, fio numjobs) #> `
  -nc 3                            <# repeat 3x: this test's lean was cited in downstream recommendations #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# fio makes one -xts-sized file per worker; 8*4G=32G peak, so 50Gi is enough #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_parallel_scan.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP parallel scan proxy  bs=1M  iodepth=16  workers=1,2,4,8  x3"


#### OLAP 4. Bulk sequential-write throughput (bulk load / checkpoint writeback)
# Extended -xfbs to localize shared's 16M write cliff (first run only sampled
# 1M, 4M, and 16M - the cliff is somewhere in the 4M-16M gap).
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating bulk load / checkpoint writeback #> `
  -xfbs 1M,4M,6M,8M,10M,12M,14M,16M <# block sizes to sweep (comma-separated) #> `
  -xfid 4,16                       <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_bulk_write.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP bulk write  bs=1M..16M  iodepth=4,16"


#### OLAP 5. Mixed scan/ETL contention proxy (analytics reads vs. occasional writes)
# Unchanged from the first run.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 90                         <# read percentage: 90% analytical reads, 10% concurrent ETL writes #> `
  -xfbs 1M                         <# fio block size, fixed at a throughput-bound size found in the block-size sweep #> `
  -xfid 16                         <# queue depth, fixed (enough to keep the reader saturated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_contention_proxy.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP contention proxy  randrw 90/10  bs=1M  iodepth=16"


###########################################
##### OLAP write-cliff anomaly diagnostic #
###########################################
# shared collapsed at bs=16M in OLAP test 4 (~1.1-1.2 iops, 4-13s p99
# latency) while cephcsi kept working normally (9-30 iops). The profile
# below fixes bs=16M and sweeps queue depth (crossed with fsync on/off, to
# approximate archiving/copying a full 16MB WAL segment with an fsync at the
# end) to see whether the collapse needs concurrency or already happens at a
# single outstanding 16M write.


#### OLAP 6. Bulk-write cliff: depth sensitivity at the cliff block size
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating a WAL segment flush #> `
  -xfbs 16M                        <# fio block size, fixed at the cliff found in OLAP test 4 #> `
  -xfid 1,2,4,8,16                 <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 0,1                        <# with and without fsync: approximates archiving a WAL segment then fsync'ing it #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -mc                              <# collect node-level cluster metrics: check for a CPU-side signal #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $storageClass               <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\storage_${storageClass}_olap_bulk_write_cliff_depth.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP bulk-write cliff depth sensitivity  bs=16M  iodepth=1..16  fsync=0,1"


Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Storage class: $storageClass"

}


###########################################
############## Clean Folder ###############
###########################################

Invoke-CleanLogs
