#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Modes - Start / Load
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










####################################################
#################### YCSB Modes ####################
####################################################




nohup python ycsb.py -ms 1 -tr \
  --dbms Citus \
  --workload c \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT \
  start </dev/null &>$LOG_DIR/test_ycsb_start_postgresql.log &

wait_process "ycsb"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

nohup python ycsb.py -ms 1 -tr \
  --dbms Citus \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD \
  load </dev/null &>$LOG_DIR/test_ycsb_load_postgresql.log &

wait_process "ycsb"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb

nohup python ycsb.py -ms 1 -tr \
  --dbms Citus \
  --workload c \
  -m -mc \
  -nlp 8 -nlt 64 -nbp 8 -nbt 64 -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_ycsb_run_postgresql.log &

wait_process "ycsb"
kubectl get all -l app=bexhoma,usecase=ycsb
kubectl delete all -l app=bexhoma,usecase=ycsb





bexperiments stop
python .\benchbase.py start -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT | Tee-Object -FilePath "$env:LOG_DIR/test_benchbase_start_postgresql.log"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc

bexperiments stop
python .\benchbase.py load -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -nlp 1 -nlt 64 | Tee-Object -FilePath "$env:LOG_DIR/test_benchbase_load_postgresql.log"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc

bexperiments stop
python .\benchbase.py run -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -nlp 1 -nlt 64 -nbp 8 -nbt 64 -ss | Tee-Object -FilePath "$env:LOG_DIR/test_benchbase_run_postgresql.log"
kubectl get all -l app=bexhoma,usecase=benchbase_tpcc






bexperiments stop
python .\hammerdb.py start -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT | Tee-Object -FilePath "$env:LOG_DIR/test_hammerdb_start_postgresql.log"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc

bexperiments stop
python .\hammerdb.py load -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -nlp 1 -nlt 1 | Tee-Object -FilePath "$env:LOG_DIR/test_hammerdb_load_postgresql.log"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc

bexperiments stop
python .\hammerdb.py run -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss | Tee-Object -FilePath "$env:LOG_DIR/test_hammerdb_run_postgresql.log"
kubectl get all -l app=bexhoma,usecase=hammerdb_tpcc






bexperiments stop
python .\tpch.py start -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT | Tee-Object -FilePath "$env:LOG_DIR/test_tpch_start_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-h

bexperiments stop
python .\tpch.py load -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -ii -ic -is -nlp 1 -nlt 1 | Tee-Object -FilePath "$env:LOG_DIR/test_tpch_load_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-h

bexperiments stop
python .\tpch.py run -m -mc --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss | Tee-Object -FilePath "$env:LOG_DIR/test_tpch_run_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-h






bexperiments stop
python .\tpcds.py start --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT | Tee-Object -FilePath "$env:LOG_DIR/test_tpcds_start_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-ds

bexperiments stop
python .\tpcds.py load --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -ii -ic -is -nlp 1 -nlt 1 | Tee-Object -FilePath "$env:LOG_DIR/test_tpcds_load_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-ds

bexperiments stop
python .\tpcds.py run --dbms PostgreSQL -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -ii -ic -is -nlp 1 -nlt 1 -nbp 1 -nbt 64 -ss | Tee-Object -FilePath "$env:LOG_DIR/test_tpcds_run_postgresql.log"
kubectl get all -l app=bexhoma,usecase=tpc-ds







nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  --workload a \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_citus_1.log &



wait_process "ycsb"






###########################################
############## Clean Folder ###############
###########################################


clean_logs
