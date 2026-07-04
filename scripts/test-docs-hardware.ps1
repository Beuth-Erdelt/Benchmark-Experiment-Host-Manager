#Requires -Version 5.1
# Generates documentation summaries for Hardware (fio) experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




###########################################
################ Hardware #################
###########################################




#### Hardware fio queue-depth sweep
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k                         <# fio block size #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_depth_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio depth sweep  rw=randread,randwrite  iodepth=1..128"


#### Hardware fio numjobs sweep at fixed queue depth (elbow check)
# The depth sweep above plateaus around iodepth=64. This fixes -xfid 64 and
# sweeps -nbt (numjobs per pod) instead: if IOPS keep climbing with more
# threads at the same depth, 64 was a per-queue submission limit, not a real
# device ceiling; if IOPS stay flat, 64 is the actual hardware limit.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k                         <# fio block size, fixed #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1,2,4,8,16                  <# numjobs per pod to sweep (comma-separated) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 80Gi                        <# fio makes one -xts-sized file per numjobs thread; 16*4G=64G peak, so 50Gi is not enough #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_numjobs_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio numjobs sweep  rw=randread,randwrite  iodepth=64  numjobs=1..16"


#### Hardware fio block-size sweep at fixed queue depth (throughput curve)
# Also fixes -xfid 64, but sweeps -xfbs instead of numjobs: this finds the
# best block size at the queue depth already identified as the elbow, and
# shows where the workload shifts from IOPS-bound (small blocks) to
# bandwidth-bound (large blocks).
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k,8k,16k,64k,128k,256k,1M <# block sizes to sweep (comma-separated) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs), fixed #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_blocksize_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio block-size sweep  rw=randread,randwrite  iodepth=64  bs=4k..1M"


#### Hardware fio depth-sweep refinement around the elbow
# The coarse depth sweep above only localizes the elbow to "somewhere between
# 64 and 128" (each doubling step covers a wide range). This does a linear
# pass inside that bracket to pinpoint the actual knee instead of just the
# bracket containing it.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k                         <# fio block size, fixed #> `
  -xfid 64,80,96,112,128           <# linear refinement around the elbow (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_depth_sweep_refine.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio depth sweep refine  rw=randread,randwrite  iodepth=64,80,96,112,128"


###########################################
##### PostgreSQL config calibration ######
###########################################
# The sweeps above use bs=4k as a generic device-IOPS probe. PostgreSQL always
# issues 8kB pages (BLCKSZ), so the two commands below re-anchor the relevant
# numbers at the actual unit of I/O Postgres uses.


#### Hardware fio depth sweep at PostgreSQL's page size (8k)
# Same shape as the original depth sweep, but bs=8k instead of 4k. This is the
# number that actually calibrates effective_io_concurrency /
# maintenance_io_concurrency, PostgreSQL's own prefetch-depth knobs.
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_depth_sweep_8k.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio depth sweep 8k  rw=randread,randwrite  iodepth=1..128"


#### Hardware fio random_page_cost calibration
# Sequential vs. random read at the same block size and depth. The
# latency/throughput ratio between the two rounds gives a device-specific
# number to replace random_page_cost's spinning-disk-era default of 4.0
# (relative to seq_page_cost=1.0) — often closer to 1.1-1.5 on NVMe.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw read,randread              <# sequential vs. random read (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_random_page_cost.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio random_page_cost calibration  rw=read,randread  iodepth=64"


###########################################
######### WAL / durability (fsync) #######
###########################################
# All four commands below share one shape: sequential 8k writes simulating
# WAL append, varying only the axis under test. -rsr is intentionally NOT set
# here (see project notes) - add it if you want every command to start from a
# freshly-provisioned volume instead of inheriting the previous command's
# write history, which matters more for these absolute-latency tests than for
# the relative-scaling sweeps above.


#### Hardware fio WAL sync-write latency (fsync)
# Sequential 8k write + fsync after every write, depth 1, single thread. This
# is "how fast can one backend commit with synchronous_commit=on and no
# batching" - max TPS is approximately 1/latency. wal_sync_method=fsync.
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_wal_sync_fsync.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio WAL sync-write fsync  bs=8k  iodepth=1"


#### Hardware fio WAL sync-write latency (fdatasync)
# Same as above but fdatasync instead of fsync. fdatasync skips the
# inode-metadata sync fsync does, and is PostgreSQL's Linux default
# (wal_sync_method=fdatasync) - compare its latency against the fsync run
# above to confirm it is actually cheaper on this storage.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xffd 1                          <# fdatasync after every write (wal_sync_method=fdatasync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (single backend) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_wal_sync_fdatasync.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio WAL sync-write fdatasync  bs=8k  iodepth=1"


#### Hardware fio WAL group-commit scaling
# Same sync-write profile as above, sweeping concurrent committing backends
# (-nbt) instead of a single one. If aggregate fsyncs/sec keeps climbing with
# more concurrent writers, the storage/controller coalesces concurrent
# commits well; if it flattens immediately, tune commit_delay/commit_siblings
# in Postgres to force batching in software instead.
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_wal_group_commit.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio WAL group commit  bs=8k  iodepth=1  backends=1..32"


#### Hardware fio WAL record-size sweep
# Same sync-write profile, sweeping the WAL record size instead of backend
# count. Bigger transactions (or post-checkpoint full_page_writes bursts)
# write more before fsync - this shows how sync-write latency grows with
# record size.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 1k,8k,16k,32k,64k          <# WAL record sizes to sweep (comma-separated) #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_wal_record_size.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio WAL record size  bs=1k..64k  iodepth=1"


###########################################
###### Checkpoint / background writer ####
###########################################


#### Hardware fio checkpoint writeback bandwidth
# Large-block sequential writes without a per-write fsync, approximating how
# fast checkpointer/bgwriter can flush dirty pages during a checkpoint.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating checkpoint writeback #> `
  -xfbs 1M,4M,16M                  <# checkpoint writeback block sizes to sweep (comma-separated) #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_checkpoint_writeback.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio checkpoint writeback  bs=1M..16M  iodepth=4,16"


#### Hardware fio OLTP/WAL contention proxy
# Single-profile approximation of foreground OLTP traffic contending with WAL
# flushes on one queue: mixed random read/write with fsync on the write side.
# This is NOT the same as true concurrent checkpoint+WAL+OLTP contention
# (that needs several parallel benchmarker jobs with different profiles in
# one round, deliberately out of scope here - see project notes) but it is
# achievable with the single-profile-per-round model used throughout this
# script.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 70                         <# read percentage: 70% OLTP reads, 30% WAL-like writes #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_oltp_wal_contention_proxy.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio OLTP/WAL contention proxy  randrw 70/30  bs=8k  iodepth=64"


###########################################
##### Sysbench CPU noisy-neighbor #########
###########################################
# The four commands below all use -xht sysbench (CPU/memory, no disk I/O, so no
# -rst/-rss/-rsr needed) and share one investigation: does a Kubernetes CPU
# limit (-lc) on the SUT container actually isolate co-located workloads, and
# how much of that isolation survives once you look at the harness rather than
# the cgroup itself. Command 13 calibrates the per-pod saturation point;
# 14/15 are cheap single-SUT sanity checks that don't need a second SUT pod;
# 16 is the actual noisy-neighbor test, co-locating several independent SUT
# pods (via -mtn/-mtb container) on one node.
#
# -xtd 60 caps each of run_sysbench.sh's two phases (CPU, then memory) at 60s
# (see images/hardware/benchmarker/run_sysbench.sh); without it, sysbench
# falls back to its own short built-in default and a round can finish before
# -m/-mc's Prometheus scrape interval ever samples it, showing no monitoring
# data at all. Total round length is therefore roughly up to 2x60s (memory
# can finish earlier if its 10G transfers before the time limit) plus SSH/pod
# overhead - about 1-2 minutes per round, the "duration" column in the result
# DataFrame is the actual measured value (BEXHOMA_DURATION).


#### 13. Sysbench CPU-quota calibration (thread sweep)
# Single SUT pod, -lc/-rc 2 (hard 2-core ceiling, request==limit so no
# bursting). Sweeps sysbench's own thread count (-nbt) at fixed -nbp 1: events
# per second should roughly double from 1->2 threads, then flatten for 4 and 8
# (a 2-core cgroup can't run more concurrent CPU-bound threads than it has
# cores), and -mc's CPU utilization for this SUT container should plateau at
# ~2 cores from -nbt=2 onward. The threads-per-pod value found here where
# events/sec first plateaus is the "saturation point" used as a fixed
# parameter in commands 14-16.
bexhoma hardware `
  -dbms Hardware                    <# hardware target(s) to test #> `
  -xht sysbench                     <# benchmark tool: sysbench (CPU/memory) #> `
  -xtd 60                           <# seconds per phase (CPU, then memory); long enough for -m/-mc to sample #> `
  -nbp 1                             <# benchmarking pod count, fixed #> `
  -nbt 1,2,4,8                       <# sysbench --threads to sweep (comma-separated) #> `
  -ne 1                              <# parallel client counts to sweep (comma-separated) #> `
  -m                                 <# collect SUT resource metrics #> `
  -mc                                <# collect node-level cluster metrics (CPU throttling) #> `
  -ms $BEXHOMA_MS                    <# max simultaneous DBMS configurations #> `
  -tr                                <# verify result meets basic sanity requirements #> `
  -lc 2                              <# CPU limit for the SUT pod: calibration ceiling #> `
  -rc 2                              <# CPU request for the SUT pod, matches -lc #> `
  -rnn $BEXHOMA_NODE_SUT             <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK       <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sysbench_cpu_quota_calibration.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware sysbench CPU quota calibration  lc=2  threads=1,2,4,8"


#### 14. Sysbench harness-overhead sweep (-nbp)
# Same fixed total of 4 sysbench threads against the same -lc 2 SUT, but
# re-partitioned across a growing number of separate benchmarker pods/SSH
# sessions (-nbp 1,2,4) instead of separate --threads inside one pod. Since
# the SUT's cgroup quota doesn't care about client-side process boundaries,
# aggregate events/sec should stay flat across all three rounds; a
# measurable drop as -nbp grows would point to benchmarker-side overhead
# (extra SSH sessions, extra pod-sync latency), not a hardware/cgroup finding.
bexhoma hardware `
  -dbms Hardware                    <# hardware target(s) to test #> `
  -xht sysbench                     <# benchmark tool: sysbench (CPU/memory) #> `
  -xtd 60                           <# seconds per phase (CPU, then memory); long enough for -m/-mc to sample #> `
  -nbp 1,2,4                         <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                             <# total sysbench threads, fixed, split across -nbp #> `
  -ne 1                              <# parallel client counts to sweep (comma-separated) #> `
  -m                                 <# collect SUT resource metrics #> `
  -mc                                <# collect node-level cluster metrics (CPU throttling) #> `
  -ms $BEXHOMA_MS                    <# max simultaneous DBMS configurations #> `
  -tr                                <# verify result meets basic sanity requirements #> `
  -lc 2                              <# CPU limit for the SUT pod, fixed #> `
  -rc 2                              <# CPU request for the SUT pod, matches -lc #> `
  -rnn $BEXHOMA_NODE_SUT             <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK       <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sysbench_nbp_overhead_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware sysbench nbp overhead sweep  lc=2  threads=4  pods=1,2,4"


#### 15. Sysbench shared-SUT saturation sweep (-ne)
# Same -lc 2 SUT, but this time -ne actually grows total demand: each
# additional parallel client submits another full -nbt-threads pod (see
# hardware.py, benchmarking_pods_scaled = num_executor * benchmarking_pods),
# so -ne 1,2,4,8 at -nbt 2 -nbp 1 pushes 2, 4, 8, then 16 total sysbench
# threads against the same fixed 2-core cgroup, all in one shared container -
# no second SUT pod involved. Aggregate events/sec should plateau once total
# demand exceeds ~2 cores' worth of throughput; this is the oversubscription
# curve for a single shared cgroup, the baseline command 16 compares against.
bexhoma hardware `
  -dbms Hardware                    <# hardware target(s) to test #> `
  -xht sysbench                     <# benchmark tool: sysbench (CPU/memory) #> `
  -xtd 60                           <# seconds per phase (CPU, then memory); long enough for -m/-mc to sample #> `
  -nbp 1                             <# benchmarking pod count, fixed #> `
  -nbt 2                             <# threads per benchmarking pod, fixed at the saturation point #> `
  -ne 1,2,4,8                        <# parallel client counts to sweep (comma-separated) #> `
  -m                                 <# collect SUT resource metrics #> `
  -mc                                <# collect node-level cluster metrics (CPU throttling) #> `
  -ms $BEXHOMA_MS                    <# max simultaneous DBMS configurations #> `
  -tr                                <# verify result meets basic sanity requirements #> `
  -lc 2                              <# CPU limit for the SUT pod, fixed #> `
  -rc 2                              <# CPU request for the SUT pod, matches -lc #> `
  -rnn $BEXHOMA_NODE_SUT             <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK       <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sysbench_ne_saturation_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware sysbench ne saturation sweep  lc=2  threads=2  clients=1,2,4,8"


#### 16. Sysbench co-located noisy-neighbor test (-mtn/-mtb container)
# The actual cross-tenant test: -mtn 4 -mtb container creates 4 independent
# SutConfiguration objects (4 separate SUT pods, 4 separate cgroups, see
# hardware.py), each -lc/-rc 2 like command 13, all pinned to the same node
# via -rnn. BEXHOMA_TENANT_BY=container makes every tenant's benchmarker pod
# wait on one shared experiment-level Redis counter before starting sysbench
# (see images/hardware/benchmarker/benchmarker.sh), so all four 2-thread
# sysbench runs begin at the same synchronized instant instead of drifting
# apart with each pod's own scheduling jitter. Compare each tenant's
# events/sec (get_summary_benchmark_per_phase_multitenant groups one row per
# tenant) against the single-pod baseline from command 13 at threads=2: flat
# per-tenant throughput means Kubernetes' CPU quotas actually isolate
# co-located pods on this node; a per-tenant dip points to contention the
# quotas don't cover (shared LLC, memory bandwidth).
bexhoma hardware `
  -dbms Hardware                    <# hardware target(s) to test #> `
  -xht sysbench                     <# benchmark tool: sysbench (CPU/memory) #> `
  -xtd 60                           <# seconds per phase (CPU, then memory); long enough for -m/-mc to sample #> `
  -nbp 1                             <# benchmarking pod count per tenant, fixed #> `
  -nbt 2                             <# threads per benchmarking pod, fixed at the saturation point #> `
  -ne 1                              <# parallel client counts to sweep (comma-separated) #> `
  -m                                 <# collect SUT resource metrics #> `
  -mc                                <# collect node-level cluster metrics (CPU throttling) #> `
  -ms $BEXHOMA_MS                    <# max simultaneous DBMS configurations #> `
  -tr                                <# verify result meets basic sanity requirements #> `
  -lc 2                              <# CPU limit per tenant SUT pod #> `
  -rc 2                              <# CPU request per tenant SUT pod, matches -lc #> `
  -mtb container                     <# tenancy granularity: one SUT pod per tenant #> `
  -mtn 4                             <# number of co-located tenants (SUT pods) #> `
  -rnn $BEXHOMA_NODE_SUT             <# schedule every tenant's SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK       <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sysbench_noisy_neighbor.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware sysbench noisy-neighbor test  lc=2  threads=2  tenants=4"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
