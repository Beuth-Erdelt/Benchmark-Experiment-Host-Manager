#Requires -Version 5.1
# Generates test logs for IBM Db2 Community Edition 12.1.5 (#829), one run per workload.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs to logs_tests/local (not in the repository), and
# extracts summaries into separate files.
#
# The results of Db2 are kept internal: the logs stay in logs_tests/local
# (git-ignored, check with git check-ignore logs_tests/local/x.log), no docs page
# shows or links them, and nothing of them is committed, quoted in issues or PRs,
# or shown elsewhere.
#
# Db2 Community Edition uses at most 4 cores and 8 GB of instance memory
# (license, db2licm -l); the template requests 4 cores and 12Gi. The SUT container
# needs the capability IPC_OWNER (no privileged mode). Check in the logs that the
# AI optimizer is off (checkschema: ai_optimizer, auto_ai_optimizer OFF).
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
  -dbms DB2                     <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -nlp 4                        <# number of data loader pods #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# gather optimizer statistics (RUNSTATS) after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_db2_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DB2 storage  sf=1"


#### TPC-H refresh stream
bexhoma tpch `
  -dbms DB2                     <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ne 3                         <# parallel query streams #> `
  -nlp 4                        <# number of data loader pods #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# gather optimizer statistics (RUNSTATS) after data load #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -xrs 3                        <# refresh stream: 3 RF1+RF2 pairs per round, parallel to the query streams #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_db2_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DB2 refresh  sf=1  ne=3"


#### TPC-DS with all post-load steps, persistent storage, reset
bexhoma tpcds `
  -dbms DB2                     <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -nlp 4                        <# number of data loader pods #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# gather optimizer statistics (RUNSTATS) after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_db2_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS DB2 storage  sf=1"


#### YCSB workload a, persistent storage, reset
bexhoma ycsb `
  -dbms DB2                     <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2                       <# throughput target as a multiple of the base ops/s #> `
  -xnlf 1                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 4                        <# number of data loader pods #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_db2_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB DB2 workload a  sf=1"


#### YCSB workload e (scans with LIMIT)
bexhoma ycsb `
  -dbms DB2                     <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl e                        <# YCSB workload template (95% scan / 5% insert) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -xnlf 1                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 4                        <# number of data loader pods #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_db2_workload_e.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB DB2 workload e  sf=1"


#### Benchbase tpcc (profile db2 of the bexhoma image, the only Benchbase benchmark with a Db2 config)
bexhoma benchbase `
  -dbms DB2                     <# DBMS under test #> `
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
  -lr 12Gi                      <# RAM limit for the SUT container (Db2 uses at most 8 GB) #> `
  -rr 12Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_tpcc_db2_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase DB2 tpcc  sf=16"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
