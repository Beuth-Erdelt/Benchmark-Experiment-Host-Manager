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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
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
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_blocksize_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Hardware fio block-size sweep  rw=randread,randwrite  iodepth=64  bs=4k..1M"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
