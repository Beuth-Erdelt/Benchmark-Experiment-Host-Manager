#Requires -Version 5.1
# Generates documentation summaries for MonetDB experiments (Example-MonetDB.md).
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H power test on MonetDB, quick, without monitoring
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on MonetDB at SF 30, at least 1 minute of benchmarking
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 30                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 3600                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB monitoring  sf=30"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H on MonetDB, the second run uses the loaded volume
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB storage  sf=1  nc=2"


####################################################
#### TPC-H at SF 100 ###############################
####################################################


# TPC-H power test at SF 100, loads the volume
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 3600                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_sf100.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB power  sf=100  nc=1  ne=1"


# TPC-H power test at SF 100, repeated on the loaded volume
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "1,1"                     <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 3600                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_sf100_repeated.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB power  sf=100  nc=2  ne=1,1"


# TPC-H throughput test at SF 100, on the loaded volume
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne "1,1,3"                   <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 3600                       <# query timeout in seconds #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -lr 256Gi                     <# RAM limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -rr 256Gi                     <# RAM requested for the SUT container #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_sf100_throughput.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB throughput  sf=100  ne=1,1,3"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS power test at SF 3
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB simple  sf=3"


# TPC-DS monitoring at SF 3
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB monitoring  sf=3"


# TPC-DS throughput test at SF 3, on persistent storage
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB throughput  sf=3  ne=1,2"


####################################################
#### TPC-DS at SF 30 ###############################
####################################################


# TPC-DS power test at SF 30, loads the volume
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 30                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 14400                      <# query timeout in seconds #> `
  -lr 1024Gi                    <# RAM limit for the SUT container #> `
  -rr 900Gi                     <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 3000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb_sf30.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB power  sf=30  nc=1  ne=1"


# TPC-DS power test at SF 30, repeated on the loaded volume
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 30                        <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,1                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 14400                      <# query timeout in seconds #> `
  -lr 1024Gi                    <# RAM limit for the SUT container #> `
  -rr 900Gi                     <# RAM requested for the SUT container #> `
  -rss 3000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb_sf30_repeated.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB power  sf=30  nc=2  ne=1,1"


# TPC-DS throughput test at SF 30, on the loaded volume
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 30                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1,1,3                     <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 14400                      <# query timeout in seconds #> `
  -lr 1024Gi                    <# RAM limit for the SUT container #> `
  -rr 900Gi                     <# RAM requested for the SUT container #> `
  -rss 3000Gi                   <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_monetdb_sf30_throughput.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB throughput  sf=30  ne=1,1,3"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MonetDB: 3 query streams and one RF1/RF2 stream in parallel
bexhoma tpch `
  -dbms MonetDB                 <# DBMS under test #> `
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
  -lc 16                        <# CPU limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_monetdb_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MonetDB refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
