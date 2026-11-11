#Requires -Version 5.1
# Generates test logs for SQL Server 2022 Developer edition (#834), one run per workload.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs to logs_tests/local (not in the repository), and
# extracts summaries into separate files.
#
# The license forbids publishing benchmark results without Microsoft's prior
# written approval: the logs stay in logs_tests/local (git-ignored, check with
# git check-ignore logs_tests/local/x.log), no docs page shows or links them,
# and nothing of them is committed, quoted in issues or PRs, or shown elsewhere.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

# after dot-sourcing: testfunctions.ps1 sets .\logs_tests
$LOG_DIR = ".\logs_tests\local"
New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null


#### TPC-H with all post-load steps, persistent storage, reset
bexhoma tpch `
  -dbms SQLServer               <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -nlp 8                        <# number of data loader pods #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run UPDATE STATISTICS after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_sqlserver_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H SQLServer storage  sf=1"


#### TPC-H refresh stream
bexhoma tpch `
  -dbms SQLServer               <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ne 3                         <# parallel query streams #> `
  -nlp 8                        <# number of data loader pods #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run UPDATE STATISTICS after data load #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xrs 3                        <# refresh stream: 3 RF1+RF2 pairs per round, parallel to the query streams #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_sqlserver_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H SQLServer refresh  sf=1  ne=3"


#### YCSB workload a, persistent storage, reset
bexhoma ycsb `
  -dbms SQLServer               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2                       <# throughput target as a multiple of the base ops/s #> `
  -xnlf 1                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_sqlserver_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB SQLServer workload a  sf=1"


#### Benchbase tpcc (the only Benchbase benchmark with a SQL Server config)
bexhoma benchbase `
  -dbms SQLServer               <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xbt tpcc                     <# Benchbase benchmark type #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 16384                    <# base ops/s used to compute the throughput target #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_tpcc_sqlserver_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase SQLServer tpcc  sf=16"


#### HammerDB TPC-C
bexhoma hammerdb `
  -dbms SQLServer               <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_sqlserver.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB SQLServer  sf=16"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
