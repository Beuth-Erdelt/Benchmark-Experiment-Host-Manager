#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - More Tests to cover more cases like more DBMS 
######################################################################################
#
# This scripts starts a sequence of experiments with varying parameters.
# Each experiment waits until previous tests have been completed.
# Logs are written to a log folder.
# At the end, logs are cleaned and the summaries are extracted and stored in separate files.
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2024-10-01
# Version: 1.0
######################################################################################


# Import functions from testfunctions.sh
source ./testfunctions.sh

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"









kill $(ps aux | grep PostgreSQL | head -n 1 | awk '{print $2}')


###########################################
############### Find Nodes ################
###########################################


# list all cpu or gpu nodes, that are not master
(
  kubectl get nodes -l node-role.kubernetes.io/cpu --no-headers
  kubectl get nodes -l node-role.kubernetes.io/gpu --no-headers
) | grep -v master | awk '$2 == "Ready" {print $1}' | sort -u


# list all cpu or gpu nodes, that are not master
# pack into list
# ready_nodes=("cl-worker17" "cl-worker21" "cl-worker34")
ready_nodes=($(
  (
    kubectl get nodes -l node-role.kubernetes.io/cpu --no-headers
    kubectl get nodes -l node-role.kubernetes.io/gpu --no-headers
  ) | grep -v master | awk '$2 == "Ready" {print $1}' | sort -u
))



###########################################
############ TPC-DS Profiling #############
###########################################


# MonetDB profiles TPC-DS @SF=30
for node in "${ready_nodes[@]}"; do
  echo "Ready node: $node"
  nohup python tpcds.py -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -ne 1,1 \
  -sf 30 \
  -ii -ic -is \
  -m -mc \
  -rnn $node \
  profiling </dev/null &>$LOG_DIR/doc_tpcds_testcase_profiling_30_$node.log &
  sleep 3600
done


###########################################
############### YCSB Read #################
###########################################

# PostgreSQL runs YCSB workload C (100% read) at 16 warehouses
BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=128


# Single test
node="cl-worker36"

python ycsb.py -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $node \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 11 \
  -ne 1,1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_profiling_$node.log &


# loop over all nodes
for node in "${ready_nodes[@]}"; do
  nohup python ycsb.py -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $node \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 11 \
  -ne 1,1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_profiling_$node.log &
  sleep 3600
done




###########################################
############## HammerDB TPC-C #############
###########################################


# Single test
nohup python hammerdb.py -tr \
  -sf 16 \
  -sd 20 \
  -xlat \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1 \
  -nbt 8 \
  -m -mc \
  -ne 1,1 \
  -nc 1 \
  -rnn $node \
  -lc 8 \
  -lr 16Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_profiling_$node.log &


# loop over all nodes
for node in "${ready_nodes[@]}"; do
  nohup python hammerdb.py -tr \
  -sf 16 \
  -sd 20 \
  -xlat \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1 \
  -nbt 8 \
  -m -mc \
  -ne 1,1 \
  -nc 1 \
  -rnn $node \
  -lc 8 \
  -lr 16Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_profiling_$node.log &
  sleep 3600
done



###########################################
############## Clean Folder ###############
###########################################


clean_logs
