#Requires -Version 5.1
# Generates documentation summaries for MariaDB experiments (Example-MariaDB.md).
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


# Main example: TPC-H power test on MariaDB, quick, without monitoring
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB simple  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on MariaDB
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB monitoring  sf=1"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H throughput test on MariaDB, the second run uses the loaded volume
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB throughput  sf=1  ne=1,2"


# Persistent storage: TPC-H on MariaDB on a RAM disk
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect metrics for the whole experiment #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rst ramdisk                  <# storage class for persistent volumes #> `
  -rss 150Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadb_ramdisk.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB ramdisk  sf=10"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS power test on MariaDB
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB simple  sf=1"


# TPC-DS monitoring on MariaDB
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_mariadb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB monitoring  sf=1"


# TPC-DS throughput test on MariaDB, on persistent storage
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_mariadb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB throughput  sf=1  ne=1,2"


####################################################
#### Benchbase TPC-C ###############################
####################################################


# Benchbase TPC-C: simple
bexhoma benchbase `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 160                      <# total benchmarking threads #> `
  -xnbf 8                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB simple  sf=16"


# Benchbase TPC-C: persistent storage
bexhoma benchbase `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -xsd 1                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 160                      <# total benchmarking threads #> `
  -xnbf 8                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_mariadb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB persistency  sf=16  nc=2"


# Benchbase TPC-C: monitoring
bexhoma benchbase `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 160                      <# total benchmarking threads #> `
  -xnbf 8                       <# benchmarking thread multiplier factor #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_mariadb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB monitoring  sf=16"


# Benchbase TPC-C: scaling the clients, on the volume of the persistent storage run
bexhoma benchbase `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1,2                      <# number of benchmarking pods #> `
  -nbt 160                      <# total benchmarking threads #> `
  -xnbf 8                       <# benchmarking thread multiplier factor #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_mariadb_scale.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB complex  sf=16  nc=2  ne=1,2"


####################################################
#### HammerDB TPC-C ################################
####################################################


# HammerDB TPC-C: simple
bexhoma hammerdb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_mariadb.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB simple  sf=16"


# HammerDB TPC-C: monitoring, on persistent storage
bexhoma hammerdb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_mariadb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB monitoring  sf=16"


# HammerDB TPC-C: scaling the clients, on the volume of the monitoring run
bexhoma hammerdb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1,2                      <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_mariadb_scale.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB complex  sf=16  nc=2  ne=1,2"


####################################################
#### YCSB ##########################################
####################################################


# YCSB: scaling the loader
bexhoma ycsb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xwl a                        <# YCSB workload letter #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 4,8                      <# number of loader pods #> `
  -nlt 32,64                    <# total loader threads #> `
  -xnlf 1                       <# loader thread multiplier factor #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 64                       <# total benchmarking threads #> `
  -xnbf 1                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_mariadb_loading.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB loader scaling  sf=1"


# YCSB: persistent storage, loads the volume for the following runs
bexhoma ycsb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xwl a                        <# YCSB workload letter #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of loader pods #> `
  -nlt 64                       <# total loader threads #> `
  -xnlf 1                       <# loader thread multiplier factor #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 64                       <# total benchmarking threads #> `
  -xnbf 1                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_mariadb_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB persistency  sf=1  nc=2"


# YCSB: scaling the benchmarker, on the loaded volume
bexhoma ycsb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xwl a                        <# YCSB workload letter #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of loader pods #> `
  -nlt 64                       <# total loader threads #> `
  -xnlf 1                       <# loader thread multiplier factor #> `
  -nbp 1,8                      <# number of benchmarking pods #> `
  -nbt 64                       <# total benchmarking threads #> `
  -xnbf 1                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_mariadb_scale.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB scaling  sf=1  nc=2  ne=1,2"


# YCSB: workload E, on the loaded volume
bexhoma ycsb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xwl e                        <# YCSB workload letter #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of loader pods #> `
  -nlt 64                       <# total loader threads #> `
  -xnlf 1                       <# loader thread multiplier factor #> `
  -nbp 8                        <# number of benchmarking pods #> `
  -nbt 64                       <# total benchmarking threads #> `
  -xnbf 1                       <# benchmarking thread multiplier factor #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_mariadb_workload_e.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB workload e  sf=1"


# YCSB: monitoring, on the loaded volume
bexhoma ycsb `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xwl a                        <# YCSB workload letter #> `
  -xtb 1024                     <# target throughput (ops/s) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of loader pods #> `
  -nlt 64                       <# total loader threads #> `
  -xnlf 1                       <# loader thread multiplier factor #> `
  -nbp 1,8                      <# number of benchmarking pods #> `
  -nbt 64                       <# total benchmarking threads #> `
  -xnbf 1                       <# benchmarking thread multiplier factor #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G <# buffer pool fitting the RAM limit (template: 8G) #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_mariadb_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB monitoring  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MariaDB: 3 query streams and one RF1/RF2 stream in parallel
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
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
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadb_refresh.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
