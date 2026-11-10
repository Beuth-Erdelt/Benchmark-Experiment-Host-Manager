#Requires -Version 5.1
# Generates documentation summaries for managed database service experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$BEXHOMA_MS = 2



###############################################################
################### YCSB Database Service #####################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

Start-Sleep -Seconds 10


#### YCSB Ingestion (Example-CloudDatabase.md)
bexhoma ycsb `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
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
  -xop 1                        <# number of operations for the benchmark phase (in millions) #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_databaseservice.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB DatabaseService ingestion  sf=1  nbp=1"


#### YCSB Execution (Example-CloudDatabase.md)
bexhoma ycsb `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
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
  -xop 10                       <# number of operations for the benchmark phase (in millions) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -sl                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_databaseservice_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB DatabaseService execution skip-load  sf=1  nbp=1"

# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

# we have to be sure the "cloud service" is ready
Start-Sleep -Seconds 300


#### YCSB Persistent Storage (Example-CloudDatabase.md)
bexhoma ycsb `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 5                         <# scaling factor (number of records in millions) #> `
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
  -xop 10                       <# number of operations for the benchmark phase (in millions) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_databaseservice_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB DatabaseService storage  sf=5  nbp=1"




###############################################################
################# Benchbase Database Service ##################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

Start-Sleep -Seconds 10


# no PVC
bexhoma benchbase `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_databaseservice.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase DatabaseService  sf=16  nbp=1,2"

# no PVC, skip loading
bexhoma benchbase `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -sl                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_databaseservice_execution.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase DatabaseService skip-load  sf=16  nbp=1,2"




###############################################################
################### TPC-H Database Service ####################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

Start-Sleep -Seconds 10


#### TPC-H Monitoring (Example-CloudDatabase.md) — no PVC
bexhoma tpch `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_databaseservice.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DatabaseService  sf=3"


#### TPC-H Monitoring (Example-CloudDatabase.md) — no PVC, skip loading
bexhoma tpch `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -sl                           <# skip loading phase (reuse existing data) #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_databaseservice_execution.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DatabaseService skip-load  sf=3"


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

Start-Sleep -Seconds 10


#### TPC-H Monitoring (Example-CloudDatabase.md) — with PVC, ingestion
bexhoma tpch `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_databaseservice_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DatabaseService PVC ingestion  sf=3"


#### TPC-H Monitoring (Example-CloudDatabase.md) — with PVC, execution only
bexhoma tpch `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_databaseservice_storage_execution.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DatabaseService PVC execution  sf=3"


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

Start-Sleep -Seconds 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

Start-Sleep -Seconds 10


####################################################
#### Refresh Stream ################################
####################################################


#### TPC-H Refresh Stream (Example-CloudDatabase.md)
# TPC-H with a refresh stream on a database service: the loader image of PostgreSQL applies RF1 and RF2 to the service
bexhoma tpch `
  -dbms DatabaseService         <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -ne 3                         <# parallel query streams #> `
  -xrs 3                        <# refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_databaseservice_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H DatabaseService refresh  sf=1  ne=3"


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
