#Requires -Version 5.1
# Phase B of the network-degeneration comparison - run
# dev/test-network-degeneration-postgresql-calibration.ps1 first and fill in
# $YCSB_TARGET / $BENCHBASE_TARGET below (roughly 60% of each tool's
# calibrated 1-pod/64-thread ceiling) before running this.
#
# Three-way comparison to isolate the network component of the
# throughput/latency degeneration seen when a fixed total connection count is
# split across more benchmarking pods against PostgreSQL:
#   - ycsb     : real YCSB workload a (50% read / 50% update) traffic
#   - benchbase: real TPC-C traffic
#   - netperf  : same connection count/pod split, zero DBMS logic, pure TCP_RR
#
# ycsb/benchbase run at a fixed, submaximal throughput target (from
# calibration) rather than uncapped - a DB engine gets noisy right at its
# ceiling (checkpoint stalls, lock contention, buffer pressure), and that
# noise would be indistinguishable from the pod-count effect this comparison
# is trying to isolate. netperf stays uncapped/closed-loop: TCP_RR is already
# self-paced per connection (at most one request in flight, bounded by real
# RTT), so it isn't exposed to that same near-saturation instability and
# doesn't need throttling for stable numbers.
#
# All three are otherwise matched as closely as bexhoma's shared -nbp/-nbt
# flags allow: same total connection count (64), same -nbp 1,2,4 sweep, same
# node pins, same ~5-minute measurement window.
#
# 64 total connections (not benchbase's original 160) is a deliberate choice:
# it is the largest count all three tools can use identically without further
# infrastructure changes - netperf's data-port pool (NETPERF_DATA_NUM_PORTS,
# see images/hardware/sut/Dockerfile) is currently sized at 64. Raising it
# would let this match the original 160-thread benchbase run exactly, at the
# cost of a much longer k8s Service port list; ask if that trade-off is wanted.
# -nbp 1,2,4 divides 64 evenly (64/32/16 threads per pod) with no rounding.
#
# Interpretation: compare each tool's own 1-pod vs 4-pod result. If netperf's
# aggregate throughput stays essentially flat (as it did at nbp=1,2 in
# docs_hardware_netperf_postgresql_pod_scaling_sweep.log) while ycsb and/or
# benchbase show rising latency at constant (throttled) throughput across the
# same nbp values, that reproduces the evidence against a Kubernetes-networking
# cause. If netperf's own latency also climbs at the same nbp values, that's
# evidence the network path itself contributes, even under stable submaximal
# load. nbp=4 is new ground - this session has only tested netperf up to nbp=2.
#
# This is a dev/ investigative script, not a docs/ generator - no result
# tables are pasted into documentation from this run.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

# Filled in from dev/test-network-degeneration-postgresql-calibration.ps1's real results
# (netdegen_ycsb_postgresql_calibration.log / netdegen_benchbase_postgresql_calibration.log,
# both at 1 pod / 64 threads, uncapped):
#   YCSB      achieved ~81,228 ops/sec  -> target 16384*3  = 49,152 (~60.5% of ceiling)
#   Benchbase achieved  ~9,246 req/sec  -> target 1024*5   =  5,120 (~55.4% of ceiling)
$YCSB_TARGET_BASE      = 16384
$YCSB_TARGET_FACTOR    = 3
$BENCHBASE_TARGET_BASE = 1024
$BENCHBASE_TARGET_FACTOR = 5




###########################################
############### YCSB #######################
###########################################

#### 1. YCSB PostgreSQL pod-count scaling at fixed total concurrency (workload a, throttled)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload: 50% read / 50% update #> `
  -xtb $YCSB_TARGET_BASE        <# base ops/s (from calibration) #> `
  -xnbf $YCSB_TARGET_FACTOR     <# target factor (from calibration) #> `
  -xnlf 1                       <# loading throughput target factor #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,2,4                    <# benchmarking pod counts to compare #> `
  -nbt 64                       <# total concurrent threads/connections, split evenly across pods #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pod(s) on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netdegen_ycsb_postgresql_pod_scaling.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 1. YCSB PostgreSQL pod scaling  wl=a  target=throttled  nbp=1,2,4  nbt=64"


###########################################
############### Benchbase ##################
###########################################

#### 2. Benchbase PostgreSQL pod-count scaling at fixed total concurrency (TPC-C, throttled)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb $BENCHBASE_TARGET_BASE   <# base ops/s (from calibration) #> `
  -xnbf $BENCHBASE_TARGET_FACTOR <# throughput target factor (from calibration) #> `
  -nbp 1,2,4                    <# benchmarking pod counts to compare #> `
  -nbt 64                       <# total concurrent threads/connections, split evenly across pods #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rsr                          <# delete any existing PVC, start from a clean volume #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netdegen_benchbase_postgresql_pod_scaling.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 2. Benchbase PostgreSQL pod scaling  sf=16  target=throttled  nbp=1,2,4  nbt=64"


###########################################
############### Netperf ####################
###########################################

#### 3. Netperf pod-count scaling at fixed total concurrency (TCP_RR, no DBMS, uncapped)
# Deliberately NOT throttled - see file header. Same nbp/nbt shape as commands
# 1 and 2, zero database engine in the loop - the network-only control.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht netperf                     <# benchmark tool: netperf (many-concurrent-connection request/response) #> `
  -xtd 300                         <# seconds per netperf round, matches benchbase's 5-minute window #> `
  -xnpp tcp                        <# netperf protocol: tcp (selects TCP_RR, matches PostgreSQL's wire protocol) #> `
  -nbp 1,2,4                       <# benchmarking pod counts to compare #> `
  -nbt 64                          <# total concurrent TCP_RR connections, split evenly across pods #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod(s) on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netdegen_netperf_postgresql_pod_scaling.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 3. Netperf pod scaling (control)  protocol=tcp  nbp=1,2,4  nbt=64  uncapped"


###########################################
############## Clean Folder ###############
###########################################

Invoke-CleanLogs
