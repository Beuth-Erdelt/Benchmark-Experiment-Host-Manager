#Requires -Version 5.1
# Phase A of the network-degeneration comparison (see
# dev/test-network-degeneration-postgresql-comparison.ps1 for phase B).
#
# DB engines get noisy right at their throughput ceiling - checkpoint stalls,
# lock contention, and buffer pressure all become bursty near saturation - so
# an uncapped/max-rate comparison sweep risks measuring that noise instead of
# the pod-count effect we actually want to isolate. This calibrates each
# tool's achievable ceiling at 64 threads/1 pod first (same pattern as
# hardware.py's sysbench section: command 13 calibrates a saturation point,
# 14-16 then use a fixed value derived from it), so phase B can run the actual
# 1,2,4-pod comparison sweep at a stable, submaximal, controlled target
# instead of flat out.
#
# netperf is deliberately NOT calibrated/throttled here: TCP_RR is already
# self-paced per connection (at most one request in flight, bounded by real
# RTT, not an aggressive flood), so it isn't exposed to the same
# near-saturation instability a DB engine gets from internal state (WAL,
# checkpoints, locks) - see dev/test-network-degeneration-postgresql-comparison.ps1's
# netperf command, which stays uncapped.
#
# After this runs, read the achieved throughput from each summary
# (docs_hardware equivalent: `hardware_ycsb_...`/benchbase's own throughput
# column) and fill in the -xtb/-xnbf target in
# dev/test-network-degeneration-postgresql-comparison.ps1 at roughly 60% of
# the calibrated ceiling - conservatively below the noisy knee, still a real
# load, not a trivial one.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null




#### A1. YCSB PostgreSQL ceiling calibration (1 pod, 64 threads, uncapped)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload: 50% read / 50% update #> `
  -xtb 0                        <# base ops/s = 0 #> `
  -xnbf 1                       <# target factor; 0 base * any factor = YCSB_TARGET 0 (unlimited) #> `
  -xnlf 1                       <# loading throughput target factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod count, fixed (calibration only needs 1) #> `
  -nbt 64                       <# total concurrent threads/connections #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netdegen_ycsb_postgresql_calibration.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] A1. YCSB PostgreSQL ceiling calibration  wl=a  target=unlimited  nbp=1  nbt=64"


#### A2. Benchbase PostgreSQL ceiling calibration (1 pod, 64 threads, uncapped)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s (unreachable at this scale) #> `
  -nbp 1                        <# benchmarking pod count, fixed (calibration only needs 1) #> `
  -nbt 64                       <# total concurrent threads/connections #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rsr                          <# delete any existing PVC, start from a clean volume #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netdegen_benchbase_postgresql_calibration.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] A2. Benchbase PostgreSQL ceiling calibration  sf=16  target=16384 (unreachable)  nbp=1  nbt=64"

Invoke-CleanLogs
