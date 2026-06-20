#Requires -Version 5.1
# Generates documentation summaries for bexhoma start/load mode experiments.
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
#################### YCSB Modes ####################
####################################################


bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -xwl c                        <# YCSB workload template (c = 100% read) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_ycsb_start_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_ycsb_start_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -xwl c                        <# YCSB workload template (c = 100% read) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_ycsb_load_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_ycsb_load_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -xwl c                        <# YCSB workload template (c = 100% read) #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 8                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_ycsb_run_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_ycsb_run_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] YCSB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb




####################################################
################## Benchbase Modes #################
####################################################


bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_benchbase_start_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_benchbase_start_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_benchbase_load_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_benchbase_load_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 8                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_benchbase_run_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_benchbase_run_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc




####################################################
################### HammerDB Modes #################
####################################################


bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_hammerdb_start_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_hammerdb_start_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_hammerdb_load_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_hammerdb_load_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod (virtual users) #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_hammerdb_run_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_hammerdb_run_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] HammerDB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc




####################################################
##################### TPC-H Modes ##################
####################################################


bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_tpch_start_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpch_start_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_tpch_load_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpch_load_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpch_run_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpch_run_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h




####################################################
#################### TPC-DS Modes ##################
####################################################


bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  start 2>&1 | Out-File "$LOG_DIR\test_tpcds_start_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpcds_start_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  load 2>&1 | Out-File "$LOG_DIR\test_tpcds_load_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpcds_load_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds `
  -dbms PostgreSQL              <# DBMS under test #> `
  -nlp 1                        <# number of data loader pods #> `
  -nlt 1                        <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 64                       <# threads per benchmarking pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -ss                           <# skip loading phase (reuse existing data) #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\test_tpcds_run_postgresql.log" -Encoding utf8

Wait-BexhomaLog "$LOG_DIR\test_tpcds_run_postgresql.log"
Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
