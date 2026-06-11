#Requires -Version 5.1
# Generates documentation summaries for HammerDB experiments.
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
################ HammerDB #################
###########################################




#### HammerDB Scale (Example-HammerDB.md)
bexhoma hammerdb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_scale.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB scale  sf=16  nbp=1,2"


#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_monitoring.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
Start-Sleep -Seconds 30


#### HammerDB Persistent Storage (Example-HammerDB.md)
bexhoma hammerdb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlt 8                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_storage.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
Start-Sleep -Seconds 30


#### HammerDB Keying and Thinking Time (Example-HammerDB.md)
bexhoma hammerdb `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -sd 20                        <# benchmark duration in minutes #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -dbms PostgreSQL              <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -nlt 8                        <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod (virtual users) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_testcase_keytime.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB keytime  sf=16  nbp=1,2  nc=2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
