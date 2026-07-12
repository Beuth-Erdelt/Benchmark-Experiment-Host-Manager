#Requires -Version 5.1
# Sockperf's 1-vs-2-pod sockperf comparison (dev/test-sockperf-pods.ps1) only ever
# exercises 1 or 2 raw TCP/UDP streams total - sockperf has no way to run more than
# one connection per client process (confirmed against upstream:
# https://github.com/Mellanox/sockperf/issues/133). That is nowhere near
# docs_benchbase_postgresql_scale.log's 160 concurrent, blocking JDBC connections
# (160 in 1 pod vs 80+80 in 2 pods), so it cannot see connection-count-driven
# network-stack effects (conntrack pressure, NIC RSS/softirq queue distribution,
# ephemeral-port pressure) that only show up at that kind of concurrency.
#
# netperf's TCP_RR/UDP_RR closes that gap: it is the same blocking,
# one-transaction-at-a-time request/response pattern as a benchbase Worker (netperf's
# own manual: "a user-space to user-space ping with no think time"), with zero
# database semantics in the loop, and its manual explicitly documents running many
# concurrent instances as the supported way to get aggregate concurrency (section 7,
# "Running Concurrent Netperf Tests"). See images/hardware/benchmarker/run_netperf.sh
# for how -nbt (HARDWARE_THREADS) is wired into that many-instance concurrency and how
# each instance gets a fixed, k8s-Service-reachable data port.
#
# This compares 1 pod x 64 concurrent TCP_RR connections vs. 2 pods x 32 each -
# the largest concurrency the current NETPERF_DATA_NUM_PORTS=64 port pool supports
# (see images/hardware/sut/Dockerfile) - against docs_benchbase_postgresql_scale.log's
# aggregate throughput drop / latency rise going from 1 to 2 benchmarking pods, with no
# DB engine in the loop at all.
#
# This is a dev/ investigative run, not one of the documentation-generating sweeps in
# scripts/ - see scripts/test-docs-hardware.ps1 for the fio reference sweeps this one
# is modeled on, and dev/test-sockperf-pods.ps1 for the smaller sockperf smoke test
# this one is a concurrency-scaled successor to.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null




###########################################
################ Netperf ##################
###########################################


#### 1. Netperf pod-count comparison (1x64 vs. 2x32 concurrent TCP_RR connections)
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht netperf                     <# benchmark tool: netperf (many-concurrent-connection request/response) #> `
  -xtd 60                          <# seconds per netperf round, long enough for stable percentiles #> `
  -xnpp tcp                        <# netperf protocol: tcp (selects TCP_RR, matches Postgres/JDBC traffic) #> `
  -nbp 1,2                         <# benchmarking pod counts to compare (comma-separated) #> `
  -nbt 64                          <# total concurrent TCP_RR connections, split evenly across pods #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod(s) on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\netperf_pods_1x64_vs_2x32.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 1. Netperf pod-count comparison  protocol=tcp  nbp=1,2  nbt=64"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
