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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -sfo 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_citus_1.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-2
Start-Sleep -Seconds 30


bexhoma ycsb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (number of records x 1000) #> `
  -sfo 10                       <# number of operations for the benchmark phase (x 1000) #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  --workload a                  <# YCSB workload template (a = 50% read / 50% update) #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -tb 16384                     <# base ops/s used to compute throughput targets (2^14) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nlf 4                        <# loading throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 4                        <# benchmarking throughput target as a multiple of the base ops/s #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_ycsb_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "ycsb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Citus storage  sf=1  nbp=1  nc=2"


####################################################
################## Benchbase Citus #################
####################################################


bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -sd 5                         <# benchmark duration in minutes #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dbms Citus                   <# DBMS under test #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 128                       <# scaling factor (controls database size) #> `
  -sd 20                        <# benchmark duration in minutes #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dbms Citus                   <# DBMS under test #> `
  -nbp 1,2,4,8                  <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -nbf 16                       <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_citus_2.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase Citus scale  sf=128  nbp=1,2,4,8"


bexhoma benchbase `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 128                       <# scaling factor (controls database size) #> `
  -sd 20                        <# benchmark duration in minutes #> `
  -slg 30                       <# log status to stdout every x seconds #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -dbms Citus                   <# DBMS under test #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 1280                     <# threads per benchmarking pod #> `
  -nbf 4                        <# throughput target as a multiple of the base ops/s #> `
  -tb 1024                      <# base ops/s used to compute the throughput target (2^10) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_benchbase_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "benchbase"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase Citus keytime  sf=128  nbp=1,2,5,10  nc=2"


####################################################
################## HammerDB Citus ##################
####################################################


bexhoma hammerdb `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -dbms Citus                   <# DBMS under test #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -nlt 8                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 128                       <# scaling factor (number of warehouses) #> `
  -sd 30                        <# benchmark duration in minutes #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 128                      <# threads per loader pod #> `
  -nbp 1,2,4,8                  <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod (virtual users) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 500                       <# scaling factor (number of warehouses) #> `
  -sd 20                        <# benchmark duration in minutes #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 250                      <# threads per loader pod #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 250                      <# threads per benchmarking pod (virtual users) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 200Gi                    <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\doc_hammerdb_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "hammerdb"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB Citus large  sf=500  nbp=1,2,5,10  nc=2"


####################################################
#################### TPC-H Citus ###################
####################################################

bexhoma tpch `
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dt                           <# disable result type checking #> `
  -t 1200                       <# query timeout in seconds #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dt                           <# disable result type checking #> `
  -t 14400                      <# query timeout in seconds #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ii                           <# create indexes after data load #> `
  -ic                           <# enforce constraints after data load #> `
  -is                           <# run ANALYZE after data load #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -ms 1                         <# limit to 1 parallel DBMS configuration at a time #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nw 4                         <# number of worker nodes #> `
  -nwr 1                        <# replication factor #> `
  -nws 48                       <# number of shards #> `
  -dt                           <# disable result type checking #> `
  -t 14400                      <# query timeout in seconds #> `
  -dbms Citus                   <# DBMS under test #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -icol                         <# use columnar storage for analytics #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -rst shared                   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_testcase_citus_3.log" -Encoding utf8

Wait-BexhomaProcess "tpch"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H Citus columnar  sf=10  ne=1,1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
