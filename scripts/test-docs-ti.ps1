#Requires -Version 5.1
# Generates documentation summaries for TiDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




#################################################
##################### TiDB ######################
#################################################




#### YCSB Ingestion (Example-TiDB.md)
bexhoma ycsb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xop 1                        <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  -xnsr 3                        <# number of storage replicas #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms TiDB                    <# DBMS under test #> `
  -xtb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -xnlf 1                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xnbf 1                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_tidb_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB TiDB  sf=1  nbp=1"


bexhoma benchbase `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                         <# benchmark duration in minutes #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor #> `
  -xnsr 3                        <# number of storage replicas #> `
  -dbms TiDB                    <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -xnbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -xtb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_tidb_1.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase TiDB  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
