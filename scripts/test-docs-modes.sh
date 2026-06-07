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


bexhoma ycsb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_ycsb_start_postgresql.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_ycsb_load_postgresql.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

bexhoma ycsb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_run_postgresql.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb




####################################################
################## Benchbase Modes #################
####################################################


bexhoma benchbase -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_benchbase_start_postgresql.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_benchbase_load_postgresql.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc

bexhoma benchbase -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc
kubectl delete all -l app=bexhoma,usecase=benchbase_tpcc




####################################################
################### HammerDB Modes #################
####################################################


bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_hammerdb_start_postgresql.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_hammerdb_load_postgresql.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc

bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_hammerdb_run_postgresql.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc
kubectl delete all -l app=bexhoma,usecase=hammerdb_tpcc




####################################################
##################### TPC-H Modes ##################
####################################################


bexhoma tpch -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_tpch_start_postgresql.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_tpch_load_postgresql.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h

bexhoma tpch -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-h
kubectl delete all -l app=bexhoma,usecase=tpc-h




####################################################
#################### TPC-DS Modes ##################
####################################################


bexhoma tpcds -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start &>$LOG_DIR/test_tpcds_start_postgresql.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS start PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load &>$LOG_DIR/test_tpcds_load_postgresql.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS load PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds

bexhoma tpcds -ms $BEXHOMA_MS -tr \
  --dbms PostgreSQL \
  -m -mc \
  -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_run_postgresql.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS run PostgreSQL"
kubectl get all -l app=bexhoma,usecase=tpc-ds
kubectl delete all -l app=bexhoma,usecase=tpc-ds


###########################################
############## Clean Folder ###############
###########################################


clean_logs
