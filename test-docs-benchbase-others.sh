#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - Compare PostgreSQL with and without PGBouncer
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
################# Benchbase Others #################
####################################################



#### Benchbase Scale (Example-Benchbase-Others.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_twitter_simple.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"



#### Benchbase Scale (Example-Benchbase-Others.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 1600 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,4,8 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_twitter_scale.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"



#### Benchbase Scale (Example-Benchbase-Others.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 10 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_simple.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"


#### Benchbase Scale (Example-Benchbase-Others.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 100 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,5,10 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_scale.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"







###########################################
############## Clean Folder ###############
###########################################


clean_logs
