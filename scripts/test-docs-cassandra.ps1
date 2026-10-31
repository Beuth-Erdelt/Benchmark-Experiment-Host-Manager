#Requires -Version 5.1
# Generates documentation summaries for Cassandra experiments.
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
################## YCSB Cassandra ##################
####################################################


# Single host Cassandra
bexhoma ycsb `
  -dbms Cassandra               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 12                      <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -xop 5                        <# number of operations for the benchmark phase (in millions), longer than the scrape interval #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -ar                           <# flush and wait for compactions before each benchmarking round #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_cassandra_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Cassandra single  sf=1  nbp=1"


# Cluster of 3 Cassandra nodes
bexhoma ycsb `
  -dbms Cassandra               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 12                      <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -xop 5                        <# number of operations for the benchmark phase (in millions), longer than the scrape interval #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -ar                           <# flush and wait for compactions before each benchmarking round #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_cassandra_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Cassandra cluster 3  sf=1  nbp=1"


# Cluster of 3 Cassandra nodes and replication factor 3
bexhoma ycsb `
  -dbms Cassandra               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 12                      <# loading throughput target as a multiple of the base ops/s #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor of the keyspace #> `
  -xop 5                        <# number of operations for the benchmark phase (in millions), longer than the scrape interval #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -ar                           <# flush and wait for compactions before each benchmarking round #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_cassandra_3.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Cassandra cluster 3 replication 3  sf=1  nbp=1"


# Single host Cassandra with PVC
bexhoma ycsb `
  -dbms Cassandra               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 12                      <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -xop 5                        <# number of operations for the benchmark phase (in millions), longer than the scrape interval #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -ar                           <# flush and wait for compactions before each benchmarking round #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_cassandra_4.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Cassandra single PVC  sf=1  nbp=1  nc=2"


# Cluster of 3 Cassandra nodes, replication factor 3 and PVC
bexhoma ycsb `
  -dbms Cassandra               <# DBMS under test #> `
  -sf 1                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 4                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 12                      <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 128                      <# threads per benchmarking pod #> `
  -nw 3                         <# number of worker nodes #> `
  -nwr 3                        <# replication factor of the keyspace #> `
  -xop 5                        <# number of operations for the benchmark phase (in millions), longer than the scrape interval #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -ar                           <# flush and wait for compactions before each benchmarking round #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_cassandra_5.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB Cassandra cluster 3 replication 3 PVC  sf=1  nbp=1  nc=2"



###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
