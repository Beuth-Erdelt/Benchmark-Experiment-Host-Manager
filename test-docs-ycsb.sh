#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - Generate Summaries for Doc Files
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















###########################################
############# Generate Docs ###############
###########################################



###########################################
################## YCSB ###################
###########################################


#### YCSB Scale Loading (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 1,8 \
  -nlt 64 \
  -nlf 1,4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_loading.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "ycsb"


#### YCSB Scale Benchmarking (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_benchmarking.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"


#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_monitoring.log &

#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "ycsb"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 30


#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_storage.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"




###########################################
############## All Workloads ##############
###########################################


#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_a.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload b \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_b.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload c \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_c.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload d \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_d.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload e \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_e.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload f \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_f.log &

#### Wait so that next experiment receives a different code
wait_process "ycsb"











###########################################
############## Clean Folder ###############
###########################################


clean_logs
