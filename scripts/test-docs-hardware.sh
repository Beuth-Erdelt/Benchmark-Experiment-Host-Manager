#!/bin/bash
# Generates documentation summaries for Hardware (fio and sysbench) experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




###########################################
################ Hardware #################
###########################################




#### 1. Hardware fio queue-depth sweep
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randread,randwrite      I/O patterns to sweep (comma-separated)
# -xfbs 4k                      fio block size
# -xfid 1,2,4,8,16,32,64,128    queue depths to sweep (comma-separated)
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 1,2,4,8,16,32,64,128 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 1. Hardware fio depth sweep  rw=randread,randwrite  iodepth=1..128"


#### 2. Hardware fio depth-sweep refinement around the elbow
# The coarse sweep above (1) only localizes the elbow to "somewhere between 64
# and 128" (each doubling step covers a wide range). This does a linear pass
# inside that bracket to pinpoint the actual knee instead of just the bracket
# containing it.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randread,randwrite      I/O patterns to sweep (comma-separated)
# -xfbs 4k                      fio block size, fixed
# -xfid 64,80,96,112,128        linear refinement around the elbow (comma-separated)
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 64,80,96,112,128 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_refine.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 2. Hardware fio depth sweep refine  rw=randread,randwrite  iodepth=64,80,96,112,128"


#### 3. Hardware fio numjobs sweep at fixed queue depth (elbow check)
# Fixes -xfid 64 (the elbow found above) and sweeps -nbt (numjobs per pod)
# instead of depth: if IOPS keep climbing with more threads at the same depth,
# 64 was a per-queue submission limit, not a real device ceiling; if IOPS stay
# flat, 64 is the actual hardware limit.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randread,randwrite      I/O patterns to sweep (comma-separated)
# -xfbs 4k                      fio block size, fixed
# -xfid 64                      queue depth, fixed at the elbow found earlier
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1,2,4,8,16               numjobs per pod to sweep (comma-separated)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 80Gi                     fio makes one -xts-sized file per numjobs thread; 16*4G=64G peak, so 50Gi is not enough
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1,2,4,8,16 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 80Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_numjobs_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 3. Hardware fio numjobs sweep  rw=randread,randwrite  iodepth=64  numjobs=1..16"


#### 4. Hardware fio block-size sweep at fixed queue depth (throughput curve)
# Also fixes -xfid 64, but sweeps -xfbs instead of numjobs: this finds the
# best block size at the queue depth already identified as the elbow, and
# shows where the workload shifts from IOPS-bound (small blocks) to
# bandwidth-bound (large blocks).
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randread,randwrite      I/O patterns to sweep (comma-separated)
# -xfbs 4k,8k,16k,64k,128k,256k,1M block sizes to sweep (comma-separated)
# -xfid 64                      queue depth, fixed at the elbow found earlier
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs), fixed
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k,8k,16k,64k,128k,256k,1M \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_blocksize_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 4. Hardware fio block-size sweep  rw=randread,randwrite  iodepth=64  bs=4k..1M"




###########################################
##### PostgreSQL config calibration ######
###########################################
# The sweeps above use bs=4k as a generic device-IOPS probe. PostgreSQL always
# issues 8kB pages (BLCKSZ), so the two commands below re-anchor the relevant
# numbers at the actual unit of I/O Postgres uses.


#### 5. Hardware fio depth sweep at PostgreSQL's page size (8k)
# Same shape as the original depth sweep, but bs=8k instead of 4k. This is the
# number that actually calibrates effective_io_concurrency /
# maintenance_io_concurrency, PostgreSQL's own prefetch-depth knobs.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randread,randwrite      I/O patterns to sweep (comma-separated)
# -xfbs 8k                      fio block size, fixed at PostgreSQL's page size (BLCKSZ)
# -xfid 1,2,4,8,16,32,64,128    queue depths to sweep (comma-separated)
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 8k \
  -xfid 1,2,4,8,16,32,64,128 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_8k.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 5. Hardware fio depth sweep 8k  rw=randread,randwrite  iodepth=1..128"


#### 6. Hardware fio random_page_cost calibration
# Sequential vs. random read at the same block size and depth. The
# latency/throughput ratio between the two rounds gives a device-specific
# number to replace random_page_cost's spinning-disk-era default of 4.0
# (relative to seq_page_cost=1.0) — often closer to 1.1-1.5 on NVMe.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw read,randread           sequential vs. random read (comma-separated)
# -xfbs 8k                      fio block size, fixed at PostgreSQL's page size (BLCKSZ)
# -xfid 64                      queue depth, fixed at the elbow found earlier
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw read,randread \
  -xfbs 8k \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_random_page_cost.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 6. Hardware fio random_page_cost calibration  rw=read,randread  iodepth=64"




###########################################
######### WAL / durability (fsync) #######
###########################################
# The four commands below share one shape: sequential 8k writes simulating
# WAL append, varying only the axis under test.


#### 7. Hardware fio WAL sync-write latency (fsync)
# Sequential 8k write + fsync after every write, depth 1, single thread. This
# is "how fast can one backend commit with synchronous_commit=on and no
# batching" - max TPS is approximately 1/latency. wal_sync_method=fsync.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating WAL append
# -xfbs 8k                      fio block size, one WAL page per write
# -xfid 1                       queue depth, fixed (single outstanding write)
# -xfe libaio                   fio ioengine
# -xfsy 1                       fsync after every write (wal_sync_method=fsync)
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod, fixed (single backend)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 8k \
  -xfid 1 \
  -xfe libaio \
  -xfsy 1 \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fsync.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 7. Hardware fio WAL sync-write fsync  bs=8k  iodepth=1"


#### 8. Hardware fio WAL sync-write latency (fdatasync)
# Same as above but fdatasync instead of fsync. fdatasync skips the
# inode-metadata sync fsync does, and is PostgreSQL's Linux default
# (wal_sync_method=fdatasync) - compare its latency against the fsync run
# above to confirm it is actually cheaper on this storage.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating WAL append
# -xfbs 8k                      fio block size, one WAL page per write
# -xfid 1                       queue depth, fixed (single outstanding write)
# -xfe libaio                   fio ioengine
# -xffd 1                       fdatasync after every write (wal_sync_method=fdatasync)
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod, fixed (single backend)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 8k \
  -xfid 1 \
  -xfe libaio \
  -xffd 1 \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fdatasync.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 8. Hardware fio WAL sync-write fdatasync  bs=8k  iodepth=1"


#### 9. Hardware fio WAL group-commit scaling
# Same sync-write profile as above, sweeping concurrent committing backends
# (-nbt) instead of a single one. If aggregate fsyncs/sec keeps climbing with
# more concurrent writers, the storage/controller coalesces concurrent
# commits well; if it flattens immediately, tune commit_delay/commit_siblings
# in Postgres to force batching in software instead.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating WAL append
# -xfbs 8k                      fio block size, one WAL page per write
# -xfid 1                       queue depth, fixed (single outstanding write per thread)
# -xfe libaio                   fio ioengine
# -xfsy 1                       fsync after every write (wal_sync_method=fsync)
# -nbp 1                        benchmarking pod count
# -nbt 1,2,4,8,16,32            concurrent committing backends to sweep (comma-separated)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 150Gi                    fio makes one -xts-sized file per backend; 32*4G=128G peak, so 50Gi is not enough
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 8k \
  -xfid 1 \
  -xfe libaio \
  -xfsy 1 \
  -nbp 1 \
  -nbt 1,2,4,8,16,32 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 150Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_group_commit.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 9. Hardware fio WAL group commit  bs=8k  iodepth=1  backends=1..32"


#### 10. Hardware fio WAL record-size sweep
# Same sync-write profile, sweeping the WAL record size instead of backend
# count. Bigger transactions (or post-checkpoint full_page_writes bursts)
# write more before fsync - this shows how sync-write latency grows with
# record size.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating WAL append
# -xfbs 1k,8k,16k,32k,64k       WAL record sizes to sweep (comma-separated)
# -xfid 1                       queue depth, fixed (single outstanding write)
# -xfe libaio                   fio ioengine
# -xfsy 1                       fsync after every write (wal_sync_method=fsync)
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod, fixed (single backend)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 1k,8k,16k,32k,64k \
  -xfid 1 \
  -xfe libaio \
  -xfsy 1 \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_record_size.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 10. Hardware fio WAL record size  bs=1k..64k  iodepth=1"




###########################################
###### Checkpoint / background writer ####
###########################################


#### 11. Hardware fio checkpoint writeback bandwidth
# Large-block sequential writes without a per-write fsync, approximating how
# fast checkpointer/bgwriter can flush dirty pages during a checkpoint.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating checkpoint writeback
# -xfbs 1M,4M,16M               checkpoint writeback block sizes to sweep (comma-separated)
# -xfid 4,16                    queue depths to sweep (comma-separated)
# -xfe libaio                   fio ioengine
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 1M,4M,16M \
  -xfid 4,16 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_checkpoint_writeback.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 11. Hardware fio checkpoint writeback  bs=1M..16M  iodepth=4,16"


#### 12. Hardware fio OLTP/WAL contention proxy
# Single-profile approximation of foreground OLTP traffic contending with WAL
# flushes on one queue: mixed random read/write with fsync on the write side.
# This is NOT the same as true concurrent checkpoint+WAL+OLTP contention
# (that needs several parallel benchmarker jobs with different profiles in
# one round, deliberately out of scope here) but it is achievable with the
# single-profile-per-round model used throughout this script.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw randrw                  mixed random read/write, one queue, one profile
# -xfmx 70                      read percentage: 70% OLTP reads, 30% WAL-like writes
# -xfbs 8k                      fio block size, fixed at PostgreSQL's page size (BLCKSZ)
# -xfid 64                      queue depth, fixed at the elbow found earlier
# -xfe libaio                   fio ioengine
# -xfsy 1                       fsync after every write (approximates WAL flush contention)
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod (fio numjobs)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randrw \
  -xfmx 70 \
  -xfbs 8k \
  -xfid 64 \
  -xfe libaio \
  -xfsy 1 \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_oltp_wal_contention_proxy.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 12. Hardware fio OLTP/WAL contention proxy  randrw 70/30  bs=8k  iodepth=64"




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
# -dbms Hardware                hardware target(s) to test
# -xht sysbench                 benchmark tool: sysbench (CPU/memory)
# -xtd 60                       seconds per phase (CPU, then memory); long enough for -m/-mc to sample
# -nbp 1                        benchmarking pod count, fixed
# -nbt 1,2,4,8                  sysbench --threads to sweep (comma-separated)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect node-level cluster metrics (CPU throttling)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 2                         CPU limit for the SUT pod: calibration ceiling
# -rc 2                         CPU request for the SUT pod, matches -lc
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 1,2,4,8 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_cpu_quota_calibration.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 13. Hardware sysbench CPU quota calibration  lc=2  threads=1,2,4,8"


#### 14. Sysbench harness-overhead sweep (-nbp)
# Same fixed total of 4 sysbench threads against the same -lc 2 SUT, but
# re-partitioned across a growing number of separate benchmarker pods/SSH
# sessions (-nbp 1,2,4) instead of separate --threads inside one pod. Since
# the SUT's cgroup quota doesn't care about client-side process boundaries,
# aggregate events/sec should stay flat across all three rounds; a
# measurable drop as -nbp grows would point to benchmarker-side overhead
# (extra SSH sessions, extra pod-sync latency), not a hardware/cgroup finding.
# -dbms Hardware                hardware target(s) to test
# -xht sysbench                 benchmark tool: sysbench (CPU/memory)
# -xtd 60                       seconds per phase (CPU, then memory); long enough for -m/-mc to sample
# -nbp 1,2,4                    benchmarking pod counts to sweep (comma-separated)
# -nbt 4                        total sysbench threads, fixed, split across -nbp
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect node-level cluster metrics (CPU throttling)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 2                         CPU limit for the SUT pod, fixed
# -rc 2                         CPU request for the SUT pod, matches -lc
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1,2,4 \
  -nbt 4 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_nbp_overhead_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 14. Hardware sysbench nbp overhead sweep  lc=2  threads=4  pods=1,2,4"


#### 15. Sysbench shared-SUT saturation sweep (-ne)
# Same -lc 2 SUT, but this time -ne actually grows total demand: each
# additional parallel client submits another full -nbt-threads pod (see
# hardware.py, benchmarking_pods_scaled = num_executor * benchmarking_pods),
# so -ne 1,2,4,8 at -nbt 2 -nbp 1 pushes 2, 4, 8, then 16 total sysbench
# threads against the same fixed 2-core cgroup, all in one shared container -
# no second SUT pod involved. Aggregate events/sec should plateau once total
# demand exceeds ~2 cores' worth of throughput; this is the oversubscription
# curve for a single shared cgroup, the baseline command 16 compares against.
# -dbms Hardware                hardware target(s) to test
# -xht sysbench                 benchmark tool: sysbench (CPU/memory)
# -xtd 60                       seconds per phase (CPU, then memory); long enough for -m/-mc to sample
# -nbp 1                        benchmarking pod count, fixed
# -nbt 2                        threads per benchmarking pod, fixed at the saturation point
# -ne 1,2,4,8                   parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect node-level cluster metrics (CPU throttling)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 2                         CPU limit for the SUT pod, fixed
# -rc 2                         CPU request for the SUT pod, matches -lc
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 2 \
  -ne 1,2,4,8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_ne_saturation_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 15. Hardware sysbench ne saturation sweep  lc=2  threads=2  clients=1,2,4,8"


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
# -dbms Hardware                hardware target(s) to test
# -xht sysbench                 benchmark tool: sysbench (CPU/memory)
# -xtd 60                       seconds per phase (CPU, then memory); long enough for -m/-mc to sample
# -nbp 1                        benchmarking pod count per tenant, fixed
# -nbt 2                        threads per benchmarking pod, fixed at the saturation point
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect node-level cluster metrics (CPU throttling)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 2                         CPU limit per tenant SUT pod
# -rc 2                         CPU request per tenant SUT pod, matches -lc
# -mtb container                tenancy granularity: one SUT pod per tenant
# -mtn 4                        number of co-located tenants (SUT pods)
# -rnn $BEXHOMA_NODE_SUT        schedule every tenant's SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 2 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -mtb container \
  -mtn 4 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_noisy_neighbor.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 16. Hardware sysbench noisy-neighbor test  lc=2  threads=2  tenants=4"




###########################################
########## Netperf network latency ########
###########################################
# The three commands below all use -xht netperf (many-concurrent-connection
# TCP_RR/UDP_RR request/response, no disk I/O, so no -rst/-rss/-rsr needed)
# against a single netserver instance (images/hardware/sut/entrypoint.sh) -
# unlike sockperf below, netperf has no per-pod dedicated-server pool, because
# netserver forks a child per test session natively. This is also why netperf
# exists alongside sockperf at all: sockperf's client is limited to exactly
# one connection per process (confirmed against upstream:
# https://github.com/Mellanox/sockperf/issues/133), so "pod-count scaling"
# in sockperf's commands 20/23 below never exceeds -nbp connections. netperf's
# -nbt instead launches many *concurrent* TCP_RR connections from a single pod
# (images/hardware/benchmarker/run_netperf.sh), so commands 18/19 below can
# actually answer "does per-connection latency hold steady as concurrent
# connections grow" and "does splitting a fixed connection count across pods
# change anything" at realistic connection counts - the same questions
# sockperf's commands 20/23 ask, but at up to 64 real connections instead of
# at most 16.
#
# All three use -xnpp tcp (selects TCP_RR), matching PostgreSQL's wire
# protocol, same reasoning as sockperf's -xspp tcp below. -xtd 60 gives every
# round at least a minute, same reasoning as the sysbench/sockperf commands.


#### 17. Netperf PostgreSQL single-connection round-trip latency baseline (TCP_RR)
# TCP_RR is netperf's own description of "a user-space to user-space ping with
# no think time" - synchronous, one transaction at a time - the same shape as
# PostgreSQL's synchronous simple-query protocol, and the same test sockperf's
# command 21 (ping-pong) targets with a different tool. This is the baseline
# command 18 scales up from.
# -dbms Hardware                hardware target(s) to test
# -xht netperf                  benchmark tool: netperf (many-concurrent-connection request/response)
# -xtd 60                       seconds per netperf round
# -xnpp tcp                     netperf protocol: tcp (selects TCP_RR, matches PostgreSQL's wire protocol)
# -nbp 1                        benchmarking pod count, fixed (single connection)
# -nbt 1                        concurrent TCP_RR connections, fixed (single-connection baseline)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_query_latency.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 17. Hardware netperf PostgreSQL query round-trip latency  protocol=tcp  nbt=1"


#### 18. Netperf PostgreSQL concurrent-connection scaling (TCP_RR, -nbt sweep)
# The test sockperf structurally cannot do: sweeps the number of *concurrent*
# TCP_RR connections (1 to 64) within a single pod, holding pod count fixed at
# 1. Compare each round's per-connection latency (avg/p50/p90/p99) against
# command 17's single-connection baseline, and aggregate transaction rate
# against 1x that baseline - directly the question PostgreSQL connection-pool
# sizing (max_connections, PgBouncer pool size) depends on: does the network
# path itself stay flat as concurrent connections grow, before any DBMS
# connection/lock handling enters the picture. Capped at 64
# (NETPERF_DATA_NUM_PORTS, see images/hardware/sut/Dockerfile): each
# concurrent connection needs its own fixed data port for the k8s Service to
# forward (netperf opens a fresh listening socket per test session, not one
# shared listener - see run_netperf.sh), so the pool size is the hard ceiling.
# -dbms Hardware                hardware target(s) to test
# -xht netperf                  benchmark tool: netperf (many-concurrent-connection request/response)
# -xtd 60                       seconds per netperf round
# -xnpp tcp                     netperf protocol: tcp (selects TCP_RR, matches PostgreSQL's wire protocol)
# -nbp 1                        benchmarking pod count, fixed - isolates connection-count from pod-count
# -nbt 1,8,16,32,64             concurrent TCP_RR connections to sweep, all within one pod
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1 \
  -nbt 1,8,16,32,64 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_connection_scaling_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 18. Hardware netperf PostgreSQL connection scaling  protocol=tcp  nbt=1,8,16,32,64"


#### 19. Netperf PostgreSQL pod-count scaling at fixed total concurrency (TCP_RR, -nbp sweep)
# Holds total concurrent connections fixed at 64 (NETPERF_DATA_NUM_PORTS'
# ceiling) and splits them across 1 vs 2 pods instead - the same "-nbp sweep at
# constant total threads" shape used to investigate benchbase's PostgreSQL
# pod-scaling result (docs_benchbase_postgresql_scale.log, Example-Benchbase.md):
# there, 1 pod x 160 threads outperformed 2 pods x 80 threads by ~21% despite
# identical total connection count. This command answers whether that came
# from the network/Kubernetes path itself: if throughput here also drops
# noticeably from 1x64 to 2x32, the network path is implicated; if it stays
# flat, the benchbase-side degradation is not a Kubernetes-networking effect.
# -dbms Hardware                hardware target(s) to test
# -xht netperf                  benchmark tool: netperf (many-concurrent-connection request/response)
# -xtd 60                       seconds per netperf round
# -xnpp tcp                     netperf protocol: tcp (selects TCP_RR, matches PostgreSQL's wire protocol)
# -nbp 1,2                      benchmarking pod counts to compare
# -nbt 64                       total concurrent TCP_RR connections, split evenly across pods
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod(s) on this node
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1,2 \
  -nbt 64 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_pod_scaling_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 19. Hardware netperf PostgreSQL pod scaling  protocol=tcp  nbp=1,2  nbt=64"


###########################################
######### Sockperf network latency ########
###########################################
# The four commands below all use -xht sockperf (network latency/throughput,
# no disk I/O, so no -rst/-rss/-rsr needed) and share one SUT: a static pool of
# 16 UDP+TCP server pairs (SOCKPERF_NUM_SERVERS, see
# images/hardware/sut/entrypoint.sh); each benchmarker pod picks its own
# dedicated server via BEXHOMA_CHILD modulo (see run_sockperf.sh), so several
# pods never contend on one socket. All four use -xspp tcp, matching
# PostgreSQL's actual wire protocol (never UDP) - so pod-count scaling in
# commands 20/23 is measured over the same connection-oriented path (TCP
# handshake, per-flow conntrack state through the Service, kernel socket
# buffers) that real DBMS traffic uses, not UDP's connectionless one. 20 and
# 23 both sweep -nbp, but measure different things: 20 (mode=ul) is aggregate
# throughput under load, while 23 (mode=pp) is command 21's single-connection
# latency floor repeated at growing concurrency - the two together separate
# "does aggregate throughput hold up" from "does each individual connection's
# latency stay flat" as concurrent connections grow, which is exactly the
# question PostgreSQL connection-pool sizing (max_connections, PgBouncer pool
# size) depends on. 21/22 fix -nbp 1 to model one connection's shape (a single
# synchronous query loop, a single WAL-sender/COPY stream) in isolation. See
# the netperf section above for the same questions asked at real (not just
# per-pod) connection concurrency.
#
# -xtd 60 gives every round at least a minute, long enough for -m's Prometheus
# scrape interval to sample it at least once, the same reasoning already used
# for -xtd on the sysbench commands above.


#### 20. Sockperf pod/client scaling sweep
# -xspp tcp (not udp): pod-count scaling is meant to characterize the same
# connection-oriented network path PostgreSQL actually uses, so it should not
# skip TCP's handshake/conntrack/socket-buffer overhead by testing over UDP
# instead. Capped at -nbp 16 (SOCKPERF_NUM_SERVERS): beyond that, pods start
# sharing a server via the BEXHOMA_CHILD modulo, which would confound scaling
# with server-side contention instead of measuring pure client/network
# scaling.
# -dbms Hardware                hardware target(s) to test
# -xht sockperf                 benchmark tool: sockperf (network latency/throughput)
# -xtd 60                       seconds per sockperf round
# -xspm ul                      sockperf mode: under-load (continuous send at target rate)
# -xspr max                     message rate: uncapped
# -xsps 64                      message payload size in bytes
# -xspp tcp                     protocol: tcp, matches PostgreSQL's wire protocol
# -nbp 1,2,4,8,16                benchmarking pod counts to sweep, capped at the server pool size
# -nbt 1                        threads per benchmarking pod, fixed (unused by sockperf, one process per pod)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod(s) on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm ul \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1,2,4,8,16 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_pod_scaling_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 20. Hardware sockperf pod scaling sweep  mode=ul  protocol=tcp  msgsize=64  mps=max  nbp=1,2,4,8,16"


#### 21. Sockperf PostgreSQL simple-query round-trip latency (ping-pong, TCP)
# -xspm pp mirrors PostgreSQL's synchronous simple-query protocol: one
# connection sends, blocks for the reply, sends the next - -xspr max fires the
# next request the instant the previous reply lands, giving the single-
# connection round-trip latency ceiling. This is the network-latency analogue
# of the WAL fsync "single outstanding write" tests in the fio section above.
# -dbms Hardware                hardware target(s) to test
# -xht sockperf                 benchmark tool: sockperf (network latency/throughput)
# -xtd 60                       seconds per sockperf round
# -xspm pp                      sockperf mode: ping-pong (synchronous request/reply)
# -xspr max                     message rate: uncapped (next request right after each reply)
# -xsps 64                      message payload size in bytes
# -xspp tcp                     protocol: tcp, matches PostgreSQL's wire protocol
# -nbp 1                        benchmarking pod count, fixed (single connection)
# -nbt 1                        threads per benchmarking pod, fixed (unused by sockperf)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm pp \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_query_latency.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 21. Hardware sockperf PostgreSQL query round-trip latency  mode=pp  protocol=tcp  msgsize=64"


#### 22. Sockperf PostgreSQL streaming/bulk throughput (WAL sender/COPY, TCP, 8k)
# -xspm ul (continuous one-way stream) models WAL streaming replication or a
# COPY/bulk result transfer rather than a request/reply cycle. -xsps 8192 is
# PostgreSQL's page size (BLCKSZ) in bytes - same 8k anchor already used
# throughout the fio section - so this becomes the network-throughput
# counterpart to those page-sized fio numbers. Unlike fio's -xfbs, -xsps casts
# to a plain int, so it must be written as 8192, not "8k".
# -dbms Hardware                hardware target(s) to test
# -xht sockperf                 benchmark tool: sockperf (network latency/throughput)
# -xtd 60                       seconds per sockperf round
# -xspm ul                      sockperf mode: under-load (continuous one-way stream)
# -xspr max                     message rate: uncapped, find the throughput ceiling
# -xsps 8192                    message payload size in bytes, PostgreSQL's page size (BLCKSZ)
# -xspp tcp                     protocol: tcp, matches PostgreSQL's wire protocol
# -nbp 1                        benchmarking pod count, fixed (single stream)
# -nbt 1                        threads per benchmarking pod, fixed (unused by sockperf)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm ul \
  -xspr max \
  -xsps 8192 \
  -xspp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_streaming_throughput.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 22. Hardware sockperf PostgreSQL streaming throughput  mode=ul  protocol=tcp  msgsize=8192"


#### 23. Sockperf PostgreSQL query latency under concurrent connections (ping-pong, TCP, -nbp sweep)
# Same shape as command 21 (ping-pong, tcp, msgsize=64 - one synchronous
# request/reply loop per pod), but sweeping -nbp 1,2,4,8,16 like command 20
# instead of fixing it at 1. Command 20 already shows whether aggregate
# throughput holds up as pod count grows; this shows whether each individual
# connection's round-trip latency (avg/p50/p99/p999) stays flat as more
# concurrent connections share the same SUT and network path, or degrades -
# the more operationally relevant question for sizing max_connections/PgBouncer
# pools, since a connection pool can be "aggregate throughput is fine" and
# still be a bad experience per-query if per-connection latency creeps up.
# Capped at -nbp 16 for the same server-pool reason as command 20.
# -dbms Hardware                hardware target(s) to test
# -xht sockperf                 benchmark tool: sockperf (network latency/throughput)
# -xtd 60                       seconds per sockperf round
# -xspm pp                      sockperf mode: ping-pong (synchronous request/reply)
# -xspr max                     message rate: uncapped (next request right after each reply)
# -xsps 64                      message payload size in bytes
# -xspp tcp                     protocol: tcp, matches PostgreSQL's wire protocol
# -nbp 1,2,4,8,16                benchmarking pod counts to sweep, capped at the server pool size
# -nbt 1                        threads per benchmarking pod, fixed (unused by sockperf, one process per pod)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod(s) on this node
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm pp \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1,2,4,8,16 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_latency_scaling_sweep.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] 23. Hardware sockperf PostgreSQL query latency under concurrency  mode=pp  protocol=tcp  msgsize=64  nbp=1,2,4,8,16"




###########################################
############## Clean Folder ###############
###########################################


clean_logs
