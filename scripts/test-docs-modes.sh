#!/bin/bash
# Generates documentation summaries for bexhoma start/load mode experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




####################################################
#################### YCSB Modes ####################
####################################################


# -dbms PostgreSQL              DBMS under test
# -xwl c                        YCSB workload template (c = 100%% read)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_ycsb_postgresql_start.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

# -dbms PostgreSQL              DBMS under test
# -xwl c                        YCSB workload template (c = 100%% read)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_ycsb_postgresql_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

# -dbms PostgreSQL              DBMS under test
# -xwl c                        YCSB workload template (c = 100%% read)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 8                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -xwl c \
  -nlp 8 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_run.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb




####################################################
################## Benchbase Modes #################
####################################################


# -dbms PostgreSQL              DBMS under test
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_benchbase_postgresql_start.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_benchbase_postgresql_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 8                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_run.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc




####################################################
################### HammerDB Modes #################
####################################################


# -dbms PostgreSQL              DBMS under test
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_hammerdb_postgresql_start.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_hammerdb_postgresql_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod (virtual users)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_run.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc




####################################################
##################### TPC-H Modes ##################
####################################################


# -dbms PostgreSQL              DBMS under test
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpch_postgresql_start.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpch_postgresql_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_postgresql_run.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h




####################################################
#################### TPC-DS Modes ##################
####################################################


# -dbms PostgreSQL              DBMS under test
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/docs_tpcds_postgresql_start.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/docs_tpcds_postgresql_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -ss \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_run.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds


###########################################
############## Clean Folder ###############
###########################################


clean_logs
