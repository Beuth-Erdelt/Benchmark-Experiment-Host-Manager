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
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 1,2,4,8,16,32,64,128       <# queue depths to sweep (comma-separated) #> `
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP depth sweep  rw=randread,randwrite  bs=8k  iodepth=1..128"


#### OLTP 2. random_page_cost calibration (sequential vs. random read)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read,randread              <# sequential vs. random read (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found in the depth sweep #> `
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP random_page_cost calibration  rw=read,randread  iodepth=64"


#### OLTP 3. WAL sync-write commit latency (fsync)
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL sync-write fsync  bs=8k  iodepth=1"


#### OLTP 4. WAL sync-write commit latency (fdatasync)
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL sync-write fdatasync  bs=8k  iodepth=1"


#### OLTP 5. WAL group-commit scaling (concurrent committing backends)
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLTP WAL group commit  bs=8k  iodepth=1  backends=1..32"


#### OLTP 6. Mixed read/write contention proxy (foreground OLTP vs. WAL flush)
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
################## OLAP ###################
###########################################


#### OLAP 1. Sequential-read block-size sweep (seq-scan throughput curve)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read                       <# sequential read, simulating a large table/seq scan #> `
  -xfbs 64k,128k,256k,1M,4M,16M    <# block sizes to sweep (comma-separated) #> `
  -xfid 16                         <# queue depth, fixed (enough to keep a sequential reader saturated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs), fixed #> `
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP seq-read block-size sweep  bs=64k..16M  iodepth=16"


#### OLAP 2. Sequential-read queue-depth sweep (readahead effectiveness)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read                       <# sequential read, simulating a large table/seq scan #> `
  -xfbs 1M                         <# fio block size, fixed at a throughput-bound size found in the block-size sweep #> `
  -xfid 1,2,4,8,16,32              <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs), fixed #> `
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP seq-read depth sweep  bs=1M  iodepth=1..32"


#### OLAP 3. Parallel sequential-scan proxy (concurrent scan workers)
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

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $storageClass OLAP parallel scan proxy  bs=1M  iodepth=16  workers=1,2,4,8"


#### OLAP 4. Bulk sequential-write throughput (bulk load / checkpoint writeback)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating bulk load / checkpoint writeback #> `
  -xfbs 1M,4M,16M                  <# block sizes to sweep (comma-separated) #> `
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


Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Storage class: $storageClass"

}


###########################################
############## Clean Folder ###############
###########################################

Invoke-CleanLogs
