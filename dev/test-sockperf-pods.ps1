#Requires -Version 5.1
# Fast smoke test for the sockperf Hardware benchmark type: compares 1 vs. 2
# benchmarking pods (-nbp 1,2) to confirm multi-pod sockperf runs actually
# work end to end - each pod picks its own dedicated sockperf server on the
# SUT via BEXHOMA_CHILD modulo SOCKPERF_NUM_SERVERS (see
# images/hardware/benchmarker/run_sockperf.sh) - and gives a first look at
# whether aggregate message rate scales from 1 to 2 pods or is already
# saturating the SUT's server pool/network path.
#
# Command #2 reruns the same 1-vs-2-pod comparison over TCP with a longer
# 60s window, to check whether the throughput drop / latency rise seen
# going from 1 to 2 benchmarking pods in docs_benchbase_postgresql_scale.log
# is explained by the shared network path between BEXHOMA_NODE_BENCHMARK and
# BEXHOMA_NODE_SUT, or points to SUT-side contention instead.
#
# This is a dev/ smoke test, not one of the documentation-generating sweeps
# in scripts/ - see scripts/test-docs-hardware.ps1 for the fio reference
# sweeps this one is modeled on. Kept deliberately short (-xtd 10, one
# mode/protocol/msgsize/mps combination, the argparse defaults) so it
# finishes in well under a minute per pod count.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null




###########################################
############### Sockperf ##################
###########################################


#### 1. Sockperf pod-count comparison (1 vs. 2 benchmarking pods)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht sockperf                    <# benchmark tool: sockperf (network latency/throughput) #> `
  -xtd 10                          <# seconds per sockperf round, short for a fast smoke test #> `
  -xspm ul                         <# sockperf mode: under-load (throughput/latency under sustained send rate) #> `
  -xspr max                        <# message rate: uncapped #> `
  -xsps 64                         <# message payload size in bytes #> `
  -xspp udp                        <# protocol: udp #> `
  -nbp 1,2                         <# benchmarking pod counts to compare (comma-separated) #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (unused by sockperf, one process per pod) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod(s) on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\sockperf_pods_1_vs_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 1. Sockperf pod-count comparison  mode=ul  protocol=udp  msgsize=64  mps=max  nbp=1,2"


#### 2. Sockperf pod-count comparison over TCP (1 vs. 2 benchmarking pods)
# Same 1-vs-2-pod comparison as #1, but over TCP to match Postgres/JDBC
# traffic (benchbase connects over TCP, not UDP) and with a longer 60s
# window per pod count for stable p50/p99 instead of the 10s smoke-test
# duration. Used to check whether docs_benchbase_postgresql_scale.log's
# throughput drop / latency rise from 1 to 2 benchmarking pods (same node
# pair: BEXHOMA_NODE_BENCHMARK -> BEXHOMA_NODE_SUT) is a raw network effect:
# if aggregate message rate also drops and latency also rises here, the
# shared network path is implicated; if it scales cleanly, the benchbase
# regression is more likely SUT-side (Postgres connection/lock contention).
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht sockperf                    <# benchmark tool: sockperf (network latency/throughput) #> `
  -xtd 60                          <# seconds per sockperf round, long enough for stable percentiles #> `
  -xspm ul                         <# sockperf mode: under-load (throughput/latency under sustained send rate) #> `
  -xspr max                        <# message rate: uncapped #> `
  -xsps 64                         <# message payload size in bytes #> `
  -xspp tcp                        <# protocol: tcp (matches Postgres/JDBC traffic) #> `
  -nbp 1,2                         <# benchmarking pod counts to compare (comma-separated) #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (unused by sockperf, one process per pod) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod(s) on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\sockperf_pods_1_vs_2_tcp.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 2. Sockperf pod-count comparison  mode=ul  protocol=tcp  msgsize=64  mps=max  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
