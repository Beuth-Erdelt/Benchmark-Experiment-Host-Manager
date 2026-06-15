#Requires -Version 5.1
# Generates documentation summaries for CedarDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




#### TCP-H Monitoring (Example-TPC-H.md)
bexhoma tpch `
  -ms 5                         <# limit to 5 parallel DBMS configurations at a time #> `
  -xdt                           <# disable result type checking #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -dbms CedarDB                 <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -xii                           <# create indexes after data load #> `
  -xic                           <# enforce constraints after data load #> `
  -xis                           <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_tpch_testcase_cedardb_monitoring.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H CedarDB monitoring  sf=3"


#### YCSB Scale Loading (Example-YCSB.md)
bexhoma ycsb `
  -ms 5                         <# limit to 5 parallel DBMS configurations at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms CedarDB                 <# DBMS under test #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 1,8                      <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 1,4                      <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 2                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_cedardb_loading.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB CedarDB loading  sf=1  nlp=1,8"


#### Benchbase CH-benCHmark (Example-Benchbase-Others.md)
bexhoma benchbase `
  -ms 2                         <# limit to 2 parallel DBMS configurations at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (controls database size) #> `
  -xsd 5                         <# benchmark duration in minutes #> `
  -dbms CedarDB                 <# DBMS under test #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 100                      <# threads per benchmarking pod #> `
  -xnbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -xtb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -xbt chbenchmark                <# Benchbase benchmark type #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_testcase_chbenchmark_cedardb_simple.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase CedarDB chbenchmark simple  sf=10  nbp=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
