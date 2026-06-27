#Requires -Version 5.1
# Extended test runs covering additional DBMS and parameter combinations.
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
################# TPC-H ###################
###########################################


#### TCP-H Compare (TestCases.md)
bexhoma tpch `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_compare.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H compare  sf=1"


###########################################
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (TestCases.md)
bexhoma tpcds `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_compare.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS compare  sf=1"


###########################################
############### TPC-H MySQL ###############
###########################################


#### TCP-H Power Test - only MySQL (TestCases.md)
bexhoma tpch `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MySQL simple  sf=1"


#### TCP-H Monitoring - MySQL (TestCases.md)
bexhoma tpch `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mysql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MySQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpch-1
Start-Sleep -Seconds 30


#### TCP-H Throughput Test - MySQL (TestCases.md)
bexhoma tpch `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mysql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MySQL throughput  sf=10  ne=1,2"


#### TPC-H RAM Disk Test - MySQL (TestCases.md)
bexhoma tpch `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect metrics for the whole experiment #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rst ramdisk                  <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mysql_ramdisk.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MySQL ramdisk  sf=10"


###########################################
############ TPC-H PostgreSQL #############
###########################################


#### TCP-H Power Test - only PostgreSQL (TestCases.md)
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_postgresql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PostgreSQL simple  sf=1"


#### TCP-H Monitoring - PostgreSQL (TestCases.md)
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_postgresql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PostgreSQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
Start-Sleep -Seconds 30


#### TCP-H Throughput Test - PostgreSQL (TestCases.md)
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_postgresql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PostgreSQL throughput  sf=10  ne=1,2"


#### TPC-H RAM Disk Test - PostgreSQL (TestCases.md)
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect metrics for the whole experiment #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst ramdisk                  <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_postgresql_ramdisk.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H PostgreSQL ramdisk  sf=3"


###########################################
############## TPC-H MariaDB ##############
###########################################


#### TCP-H Power Test - only MariaDB (TestCases.md)
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mariadb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB simple  sf=1"


#### TCP-H Monitoring - MariaDB (TestCases.md)
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mariadb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB monitoring  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpch-1
Start-Sleep -Seconds 30


#### TCP-H Throughput Test - MariaDB (TestCases.md)
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mariadb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB throughput  sf=1  ne=1,2"


#### TPC-H RAM Disk Test - MariaDB (TestCases.md)
bexhoma tpch `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ma                           <# collect metrics for the whole experiment #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rst ramdisk                  <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpch_mariadb_ramdisk.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB ramdisk  sf=10"


###########################################
############### TPC-DS MySQL ##############
###########################################


#### TCP-DS Power Test - only MySQL (TestCases.md)
bexhoma tpcds `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MySQL simple  sf=1"


#### TCP-DS Monitoring - MySQL (TestCases.md)
bexhoma tpcds `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mysql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MySQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpcds-1
Start-Sleep -Seconds 30


#### TCP-DS Throughput Test - MySQL (TestCases.md)
bexhoma tpcds `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mysql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MySQL throughput  sf=10  ne=1,2"


###########################################
############ TPC-DS PostgreSQL ############
###########################################


#### TCP-DS Power Test - only PostgreSQL (TestCases.md)
bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_postgresql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS PostgreSQL simple  sf=1"


#### TCP-DS Monitoring - PostgreSQL (TestCases.md)
bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_postgresql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS PostgreSQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpcds-1
Start-Sleep -Seconds 30


#### TCP-DS Throughput Test - PostgreSQL (TestCases.md)
bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_postgresql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS PostgreSQL throughput  sf=10  ne=1,2"


###########################################
############## TPC-DS MariaDB #############
###########################################


#### TCP-DS Power Test - only MariaDB (TestCases.md)
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# query timeout in seconds #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mariadb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB simple  sf=1"


#### TCP-DS Monitoring - MariaDB (TestCases.md)
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mariadb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB monitoring  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpcds-1
Start-Sleep -Seconds 30


#### TCP-DS Throughput Test - MariaDB (TestCases.md)
bexhoma tpcds `
  -dbms MariaDB                 <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# disable result type checking #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_mariadb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDB throughput  sf=1  ne=1,2"


###########################################
############ TPC-DS MonetDB ###############
###########################################


#### TCP-DS Simple - MonetDB (TestCases.md)
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
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_monetdb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB simple  sf=3"


#### TCP-DS Monitoring - MonetDB (TestCases.md)
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
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_monetdb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB monitoring  sf=3"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-3
Start-Sleep -Seconds 30


#### TCP-DS Throughput Test - MonetDB (TestCases.md)
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_monetdb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB throughput  sf=3  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-100
Start-Sleep -Seconds 30


#### TCP-DS Power Test Large - MonetDB (TestCases.md)
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
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
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 300Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_monetdb_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB power large  sf=100"


#### TCP-DS Throughput Test Large - MonetDB (TestCases.md)
bexhoma tpcds `
  -dbms MonetDB                 <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,5                       <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 300Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_tpcds_monetdb_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MonetDB throughput large  sf=100  ne=1,5"


###########################################
########### Benchbase PostgreSQL ##########
###########################################


#### Benchbase Simple (TestCases.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_postgresql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PostgreSQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
Start-Sleep -Seconds 30


#### Benchbase Persistency (TestCases.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_postgresql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PostgreSQL persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_postgresql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PostgreSQL monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_postgresql_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase PostgreSQL complex  sf=16  nc=2  ne=1,2"


###########################################
############# Benchbase MySQL #############
###########################################


#### Benchbase Simple (TestCases.md)
bexhoma benchbase `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MySQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-benchbase-16
Start-Sleep -Seconds 30


#### Benchbase Persistency (TestCases.md)
bexhoma benchbase `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mysql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MySQL persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
bexhoma benchbase `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mysql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MySQL monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
bexhoma benchbase `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mysql_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MySQL complex  sf=16  nc=2  ne=1,2"


###########################################
############ Benchbase MariaDB ############
###########################################


#### Benchbase Simple (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mariadb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-benchbase-16
Start-Sleep -Seconds 30


#### Benchbase Persistency (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mariadb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mariadb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_benchbase_mariadb_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase MariaDB complex  sf=16  nc=2  ne=1,2"


###########################################
########## HammerDB PostgreSQL ############
###########################################


#### HammerDB Simple (TestCases.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_postgresql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB PostgreSQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
Start-Sleep -Seconds 30


#### HammerDB Monitoring (TestCases.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_postgresql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB PostgreSQL monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_postgresql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB PostgreSQL complex  sf=16  nc=2  ne=1,2"


###########################################
############# HammerDB MySQL ##############
###########################################


#### HammerDB Simple (TestCases.md)
bexhoma hammerdb `
  -dbms MySQL                   <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size in GB) #> `
  -nlt 8                        <# threads per loader pod #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# number of benchmarking pods #> `
  -nbt 16                       <# total benchmarking threads #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MySQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-hammerdb-16
Start-Sleep -Seconds 30


#### HammerDB Monitoring (TestCases.md)
bexhoma hammerdb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mysql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MySQL monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
bexhoma hammerdb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mysql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MySQL complex  sf=16  nc=2  ne=1,2"


###########################################
############ HammerDB MariaDB #############
###########################################


#### HammerDB Simple (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mariadb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-hammerdb-16
Start-Sleep -Seconds 30


#### HammerDB Monitoring (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mariadb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 16Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mariadb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MariaDB complex  sf=16  nc=2  ne=1,2"


###########################################
############ YCSB PostgreSQL ##############
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_postgresql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
Start-Sleep -Seconds 30


#### YCSB Loader Test for Persistency (TestCases.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_postgresql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_postgresql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_postgresql_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_postgresql_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB PostgreSQL monitoring  sf=1"


###########################################
############### YCSB MySQL ################
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
bexhoma ycsb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-ycsb-1
Start-Sleep -Seconds 30


#### YCSB Loader Test for Persistency (TestCases.md)
bexhoma ycsb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mysql_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
bexhoma ycsb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mysql_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
bexhoma ycsb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mysql_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
bexhoma ycsb `
  -dbms MySQL                   <# DBMS under test #> `
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mysql_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MySQL monitoring  sf=1"


###########################################
############## YCSB MariaDB ###############
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-ycsb-1
Start-Sleep -Seconds 30


#### YCSB Loader Test for Persistency (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
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
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rss 5Gi                      <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB monitoring  sf=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
