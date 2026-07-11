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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 150Gi                    <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 1000Gi                   <# size of the persistent volume claim #> `
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
  -rss 1000Gi                   <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hammerdb_mysql_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB MySQL simple  sf=16"



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
  -rss 128Gi                    <# size of the persistent volume claim #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
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
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_ycsb_mariadb_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB MariaDB monitoring  sf=1"


###########################################
################ Hardware #################
###########################################
# Eight fio sweeps that supplement the four typical-use-case fio examples in
# Example-Hardware.md (queue-depth sweep, block-size sweep, random_page_cost
# calibration, WAL sync-write fsync latency) with the rest of the full sweep
# for TestCases.md: elbow refinement, numjobs, the PostgreSQL-page-size (8k)
# depth sweep, fdatasync, WAL group-commit and record-size sweeps, checkpoint
# writeback bandwidth, and the OLTP/WAL contention proxy. All sysbench,
# netperf, and sockperf Hardware commands are already fully covered by
# Example-Hardware.md and are not repeated here.
#
# These share the same Hardware-1 SUT/PVC and must run sequentially, same as
# in test-docs-hardware.ps1/.sh; each passes -rsr to start from a freshly
# recreated, empty volume.


#### 1. Hardware fio depth-sweep refinement around the elbow
# The coarse queue-depth sweep in Example-Hardware.md's fio section only
# localizes the elbow to "somewhere between 64 and 128" (each doubling step
# covers a wide range). This does a linear pass inside that bracket to
# pinpoint the actual knee instead of just the bracket containing it.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k                         <# fio block size, fixed #> `
  -xfid 64,80,96,112,128           <# linear refinement around the elbow (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_depth_sweep_refine.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 1. Hardware fio depth sweep refine  rw=randread,randwrite  iodepth=64,80,96,112,128"


#### 2. Hardware fio numjobs sweep at fixed queue depth (elbow check)
# Fixes -xfid 64 (the elbow found above) and sweeps -nbt (numjobs per pod)
# instead of depth: if IOPS keep climbing with more threads at the same
# depth, 64 was a per-queue submission limit, not a real device ceiling; if
# IOPS stay flat, 64 is the actual hardware limit.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 4k                         <# fio block size, fixed #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1,2,4,8,16                  <# numjobs per pod to sweep (comma-separated) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 80Gi                        <# fio makes one -xts-sized file per numjobs thread; 16*4G=64G peak, so 50Gi is not enough #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_numjobs_sweep.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 2. Hardware fio numjobs sweep  rw=randread,randwrite  iodepth=64  numjobs=1..16"


#### 3. Hardware fio depth sweep at PostgreSQL's page size (8k)
# Same shape as the original depth sweep, but bs=8k instead of 4k. This is the
# number that actually calibrates effective_io_concurrency /
# maintenance_io_concurrency, PostgreSQL's own prefetch-depth knobs.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randread,randwrite         <# I/O patterns to sweep (comma-separated) #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 1,2,4,8,16,32,64,128       <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_depth_sweep_8k.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 3. Hardware fio depth sweep 8k  rw=randread,randwrite  iodepth=1..128"


#### 4. Hardware fio WAL sync-write latency (fdatasync)
# Same as the WAL sync-write fsync example in Example-Hardware.md but
# fdatasync instead of fsync. fdatasync skips the inode-metadata sync fsync
# does, and is PostgreSQL's Linux default (wal_sync_method=fdatasync) -
# compare its latency against that fsync result to confirm it is actually
# cheaper on this storage.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xffd 1                          <# fdatasync after every write (wal_sync_method=fdatasync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (single backend) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_wal_sync_fdatasync.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 4. Hardware fio WAL sync-write fdatasync  bs=8k  iodepth=1"


#### 5. Hardware fio WAL group-commit scaling
# Same sync-write profile as the WAL sync-write fsync example in
# Example-Hardware.md, sweeping concurrent committing backends (-nbt) instead
# of a single one. If aggregate fsyncs/sec keeps climbing with
# more concurrent writers, the storage/controller coalesces concurrent
# commits well; if it flattens immediately, tune commit_delay/commit_siblings
# in Postgres to force batching in software instead.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 8k                         <# fio block size, one WAL page per write #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write per thread) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (wal_sync_method=fsync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1,2,4,8,16,32               <# concurrent committing backends to sweep (comma-separated) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 150Gi                       <# fio makes one -xts-sized file per backend; 32*4G=128G peak, so 50Gi is not enough #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_wal_group_commit.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 5. Hardware fio WAL group commit  bs=8k  iodepth=1  backends=1..32"


#### 6. Hardware fio WAL record-size sweep
# Same sync-write profile as the WAL sync-write fsync example in
# Example-Hardware.md, sweeping the WAL record size instead of backend count. Bigger transactions (or post-checkpoint full_page_writes bursts)
# write more before fsync - this shows how sync-write latency grows with
# record size.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating WAL append #> `
  -xfbs 1k,8k,16k,32k,64k          <# WAL record sizes to sweep (comma-separated) #> `
  -xfid 1                          <# queue depth, fixed (single outstanding write) #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (wal_sync_method=fsync) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod, fixed (single backend) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_wal_record_size.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 6. Hardware fio WAL record size  bs=1k..64k  iodepth=1"
#### 7. Hardware fio checkpoint writeback bandwidth
# Large-block sequential writes without a per-write fsync, approximating how
# fast checkpointer/bgwriter can flush dirty pages during a checkpoint.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw write                      <# sequential write, simulating checkpoint writeback #> `
  -xfbs 1M,4M,16M                  <# checkpoint writeback block sizes to sweep (comma-separated) #> `
  -xfid 4,16                       <# queue depths to sweep (comma-separated) #> `
  -xfe libaio                      <# fio ioengine #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_checkpoint_writeback.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 7. Hardware fio checkpoint writeback  bs=1M..16M  iodepth=4,16"


#### 8. Hardware fio OLTP/WAL contention proxy
# Single-profile approximation of foreground OLTP traffic contending with WAL
# flushes on one queue: mixed random read/write with fsync on the write side.
# This is NOT the same as true concurrent checkpoint+WAL+OLTP contention
# (that needs several parallel benchmarker jobs with different profiles in
# one round, deliberately out of scope here - see project notes) but it is
# achievable with the single-profile-per-round model used throughout this
# script.
bexhoma hardware `
  -dbms Hardware                   <# hardware target(s) to test #> `
  -xht fio                         <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                          <# fio test file size #> `
  -xtd 60                          <# seconds per fio round #> `
  -xfrw randrw                     <# mixed random read/write, one queue, one profile #> `
  -xfmx 70                         <# read percentage: 70% OLTP reads, 30% WAL-like writes #> `
  -xfbs 8k                         <# fio block size, fixed at PostgreSQL's page size (BLCKSZ) #> `
  -xfid 64                         <# queue depth, fixed at the elbow found earlier #> `
  -xfe libaio                      <# fio ioengine #> `
  -xfsy 1                          <# fsync after every write (approximates WAL flush contention) #> `
  -nbp 1                           <# benchmarking pod count #> `
  -nbt 1                           <# threads per benchmarking pod (fio numjobs) #> `
  -ne 1                            <# parallel client counts to sweep (comma-separated) #> `
  -m                               <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS                  <# max simultaneous DBMS configurations #> `
  -tr                              <# verify result meets basic sanity requirements #> `
  -rsr                             <# delete any existing PVC, so every command starts from a clean volume #> `
  -rss 50Gi                        <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS      <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT           <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK     <# schedule benchmarker pod on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\testcase_hardware_fio_oltp_wal_contention_proxy.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] 8. Hardware fio OLTP/WAL contention proxy  randrw 70/30  bs=8k  iodepth=64"



###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
