#Requires -Version 5.1
# Generates documentation summaries for YCSB experiments.
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
################## YCSB ###################
###########################################




#### YCSB Scale Loading (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 1,4                     <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1,8                      <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_loading.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB loading  sf=1  nlp=1,8"


#### YCSB Scale Benchmarking (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2,3                     <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_benchmarking.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB benchmarking  sf=1  nbp=1,8"


#### YCSB Monitoring (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2,3                     <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB monitoring  sf=3  nbp=1,8"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
Start-Sleep -Seconds 30


#### YCSB Persistent Storage (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2,3                     <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB storage  sf=1  nbp=1,8  nc=2"


#### YCSB Custom Loading Parameters (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50%% read / 50%% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2                       <# throughput target as a multiple of the base ops/s #> `
  -xnlf 1                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 <# override deployment configuration parameter #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_loading_patch.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB loading patch  sf=1  nlp=1"


###########################################
############## All Workloads ##############
###########################################


#### YCSB Workload A (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_a.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload a  sf=10  nbp=1,8"


#### YCSB Workload B (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl b                        <# YCSB workload template (b = 95% read / 5% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_b.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload b  sf=10  nbp=1,8"


#### YCSB Workload C (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl c                        <# YCSB workload template (c = 100% read) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_c.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload c  sf=10  nbp=1,8"


#### YCSB Workload D (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl d                        <# YCSB workload template (d = read latest) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xio hashed                   <# index order strategy (hashed / ordered) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_d.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload d  sf=10  nbp=1"


#### YCSB Workload E (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl e                        <# YCSB workload template (e = scan) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xio ordered                  <# index order strategy (hashed / ordered) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_e.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload e  sf=10  nbp=1"


#### YCSB Workload F (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (number of records x 1000) #> `
  -xwl f                        <# YCSB workload template (f = read-modify-write) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_testcase_f.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB workload f  sf=10  nbp=1,8"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
