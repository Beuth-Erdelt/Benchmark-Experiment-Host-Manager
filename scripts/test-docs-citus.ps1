#Requires -Version 5.1
# Generates documentation summaries for Citus experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
#################### YCSB Citus ####################
####################################################


bexhoma ycsb `
  -dbms Citus                   <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_citus_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-2
Start-Sleep -Seconds 30


bexhoma ycsb `
  -dbms Citus                   <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xop 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Citus storage  sf=1  nbp=1  nc=2"


####################################################
################## Benchbase Citus #################
####################################################


bexhoma benchbase `
  -dbms Citus                   <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_citus_1.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase Citus  sf=16  nbp=1,2"

kubectl delete pvc bexhoma-storage-citus-benchbase-tpcc-128
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-3
Start-Sleep -Seconds 30


bexhoma benchbase `
  -dbms Citus                   <# DBMS under test #> `
  -sf 128                       <# scaling factor (controls database size) #> `
  -xsd 20                       <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2,4,8                  <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase Citus scale  sf=128  nbp=1,2,4,8"


bexhoma benchbase `
  -dbms Citus                   <# DBMS under test #> `
  -sf 128                       <# scaling factor (controls database size) #> `
  -xsd 20                       <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 4                       <# throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 1280                     <# threads per benchmarking pod #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -xli 30                       <# log status to stdout every x seconds #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase Citus keytime  sf=128  nbp=1,2,5,10  nc=2"


####################################################
################## HammerDB Citus ##################
####################################################


bexhoma hammerdb `
  -dbms Citus                   <# DBMS under test #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_citus_1.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB Citus  sf=16  nbp=1"

kubectl delete pvc bexhoma-storage-citus-hammerdb-128
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-3
Start-Sleep -Seconds 30


bexhoma hammerdb `
  -dbms Citus                   <# DBMS under test #> `
  -sf 128                       <# scaling factor (number of warehouses) #> `
  -xsd 30                       <# benchmark duration in minutes #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 128                      <# threads per loader pod #> `
  -nbp 1,2,4,8                  <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod (virtual users) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB Citus scale  sf=128  nbp=1,2,4,8"

kubectl delete pvc bexhoma-storage-citus-hammerdb-500
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-3
Start-Sleep -Seconds 30


bexhoma hammerdb `
  -dbms Citus                   <# DBMS under test #> `
  -sf 500                       <# scaling factor (number of warehouses) #> `
  -xsd 20                       <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 250                      <# threads per loader pod #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 250                      <# threads per benchmarking pod (virtual users) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 200Gi                    <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB Citus large  sf=500  nbp=1,2,5,10  nc=2"


####################################################
#################### TPC-H Citus ###################
####################################################

bexhoma tpch `
  -dbms Citus                   <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_testcase_citus_1.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
Start-Sleep -Seconds 30


bexhoma tpch `
  -dbms Citus                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 14400                      <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_testcase_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H Citus storage  sf=10  ne=1,1  nc=2"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
Start-Sleep -Seconds 30


bexhoma tpch `
  -dbms Citus                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xcol                         <# use columnar storage for analytics #> `
  -xdt                          <# disable result type checking #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 14400                      <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst cephcsi                   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_testcase_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H Citus columnar  sf=10  ne=1,1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
