#Requires -Version 5.1
# Generates documentation summaries for collector experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1

$BEXHOMA_NODE_SUT = "cl-worker36"




###########################################
############# TPC-C Benchbase #############
###########################################




#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -xli 10                       <# log status to stdout every x seconds #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase collector 1/3  sf=16  nbp=1,2  nbf=16"

#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 20                      <# throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nbp 4,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -xli 10                       <# log status to stdout every x seconds #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase collector 2/3  sf=16  nbp=4,8  nbf=20"

#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 20                      <# throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nbp 4,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -xli 10                       <# log status to stdout every x seconds #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase collector 3/3  sf=16  nbp=4,8  nbf=20"




###########################################
########### TPC-C Benchbase MT ############
###########################################


$BEXHOMA_NUM_TENANTS = 2

# ---------------- SCHEMA ----------------
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_tenants_schema.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- DATABASE ----------------
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_tenants_database.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- CONTAINER ----------------
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -nlp 1                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 10                       <# threads per benchmarking pod #> `
  -xkey                         <# simulate user think time and keying delays #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_collector_tenants_container.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




###########################################
################## TPC-H ##################
###########################################


bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -xqr 3                        <# number of times to repeat each query #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H collector 1/3  sf=3"

bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 6                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H collector 2/3  sf=6"

bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 6                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 60Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H collector 3/3  sf=6"




###########################################
################ TPC-H MT #################
###########################################

$BEXHOMA_NUM_TENANTS = 2

# ---------------- SCHEMA ----------------
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -nlp $BEXHOMA_NUM_TENANTS     <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb schema                   <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_tenants_schema.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- DATABASE ----------------
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" <# parallel client counts for loading and benchmarking #> `
  -nlp $BEXHOMA_NUM_TENANTS     <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb database                 <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_tenants_database.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- CONTAINER ----------------
bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -xqr 3                        <# number of times to repeat each query #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne "1,1"                     <# parallel client counts for loading and benchmarking #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -mtb container                <# tenant isolation level (schema / database / container) #> `
  -mtn $BEXHOMA_NUM_TENANTS     <# number of tenants #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_postgresql_collector_tenants_container.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=3"


###########################################
################## YCSB ###################
###########################################


#### YCSB Monitoring (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 2                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# scaling factor for operations (number of operations x 100000) #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "YCSB collector 1/3  nbp=1,8  nbf=2"

#### YCSB Monitoring (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 3                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 1                        <# scaling factor for operations (number of operations x 100000) #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "YCSB collector 2/3  nbp=1,8  nbf=3"

#### YCSB Monitoring (Example-YCSB.md)
bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (number of records in millions) #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xtb 16384                    <# base ops/s used to compute throughput targets (2^14) #> `
  -xnbf 3                       <# benchmarking throughput target as a multiple of the base ops/s #> `
  -xnlf 4                       <# loading throughput target as a multiple of the base ops/s #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,8                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xop 8                        <# scaling factor for operations (number of operations x 100000) #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ycsb_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "YCSB collector 3/3  nbp=1,8  nbf=3"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod (virtual users) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "HammerDB collector 1/3  sf=16  nbp=1,2  nbt=16"

#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod (virtual users) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "HammerDB collector 2/3  sf=16  nbp=1,2  nbt=32"

#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (number of warehouses) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -nlt 16                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod (virtual users) #> `
  -xlat                         <# collect per-operation latency histograms #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hammerdb_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "HammerDB collector 3/3  sf=16  nbp=1,2  nbt=32"


###########################################
################# TPC-DS ##################
###########################################


bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xaq 1,3,7,13,19,25,34,42,43,46,48,52,55,59,63,68,73,79,89,96,98,99 <# 22 of the 99 queries, as many as TPC-H has #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-DS collector 1/3  sf=1  ne=1,2"

bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xaq 1,3,7,13,19,25,34,42,43,46,48,52,55,59,63,68,73,79,89,96,98,99 <# 22 of the 99 queries, as many as TPC-H has #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-DS collector 2/3  sf=3  ne=1,2"

bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xaq 1,3,7,13,19,25,34,42,43,46,48,52,55,59,63,68,73,79,89,96,98,99 <# 22 of the 99 queries, as many as TPC-H has #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-DS collector 3/3  sf=3  reuse PVC"



###########################################
################### SSB ###################
###########################################


bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_postgresql_collector_1.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "SSB collector 1/3  sf=1  star schema"

bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -xsv flat                     <# denormalized flat table lineorder_flat instead of the star schema #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_postgresql_collector_2.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "SSB collector 2/3  sf=3  flat schema"

bexhoma ssb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration #> `
  -ne 1,2                       <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nbp 1                        <# benchmarking pod count #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -t 1200                       <# per-query timeout in seconds #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_postgresql_collector_3.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "SSB collector 3/3  sf=1  reuse PVC"



###########################################
################ Hardware #################
###########################################


bexhoma hardware `
  -dbms Hardware                <# hardware target to test #> `
  -xht fio                      <# benchmark tool: fio (disk I/O) #> `
  -xts 4G                       <# fio test file size #> `
  -xtd 60                       <# seconds per round #> `
  -xfrw write                   <# sequential write #> `
  -xfbs 8k                      <# fio block size #> `
  -xfid 1                       <# queue depth #> `
  -xfe libaio                   <# fio ioengine #> `
  -xffd 1                       <# fdatasync after every write #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 2                        <# threads in total, split across the pods: 1 pod x 2, 2 pods x 1 #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rsr                          <# delete and recreate the PVC at experiment start #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_fio_collector.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Hardware collector 1/4  fio  nbp=1,2"

bexhoma hardware `
  -dbms Hardware                <# hardware target to test #> `
  -xht sysbench                 <# benchmark tool: sysbench (CPU/memory) #> `
  -xtd 60                       <# seconds per round #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1                        <# benchmarking pod count #> `
  -nbt 1,2                      <# threads per benchmarking pod to sweep (comma-separated) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lc 2                         <# CPU limit for the SUT container #> `
  -rc 2                         <# CPU request for the SUT container, matches -lc #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sysbench_collector.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Hardware collector 2/4  sysbench  nbt=1,2"

bexhoma hardware `
  -dbms Hardware                <# hardware target to test #> `
  -xht sockperf                 <# benchmark tool: sockperf (network latency/throughput) #> `
  -xtd 60                       <# seconds per round #> `
  -xspm pp                      <# sockperf mode: ping-pong (synchronous request/reply) #> `
  -xspr max                     <# message rate: uncapped #> `
  -xsps 64                      <# message payload size in bytes #> `
  -xspp tcp                     <# sockperf protocol: tcp #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 1                        <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_sockperf_collector.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Hardware collector 3/4  sockperf  nbp=1,2"

bexhoma hardware `
  -dbms Hardware                <# hardware target to test #> `
  -xht netperf                  <# benchmark tool: netperf (request/response) #> `
  -xtd 60                       <# seconds per round #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 2                        <# threads in total, split across the pods: 1 pod x 2, 2 pods x 1 #> `
  -xnpp tcp                     <# netperf protocol: tcp (TCP_RR) #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_hardware_netperf_collector.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "Hardware collector 4/4  netperf  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


Write-ExperimentTotal
Invoke-CleanLogs
