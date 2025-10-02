#!/bin/bash
######################################################################################
# Bash Script for Application Metrics
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
########## PostgreSQL Application Metrics ##########
####################################################


#### Benchbase Scale (Example-Benchbase.md)
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"



#### YCSB Monitoring Application Metrics (Example-YCSB.md)
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
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log &

wait_process "ycsb"




#### TCP-H Monitoring Application Metrics (Example-TPC-H.md)
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_appmetrics.log &

wait_process "tpch"



#### TCP-DS Monitoring Application Metrics (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log &

wait_process "tpcds"


#### HammerDB Monitoring Application Metrics (Example-HammerDB.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log &

wait_process "hammerdb"








####################################################
############ MySQL Application Metrics #############
####################################################



#### Benchbase Scale (Example-Benchbase.md)
nohup python benchbase.py -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms MySQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log &

#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "benchbase"



#### YCSB Monitoring Application Metrics (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr -lr 64Gi \
  -sf 3 \
  --workload a \
  -dbms MySQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log &

wait_process "ycsb"




#### TCP-H Monitoring Application Metrics (Example-TPC-H.md)
nohup python tpch.py -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log &

wait_process "tpch"



#### TCP-DS Monitoring Application Metrics (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log &

wait_process "tpcds"


#### HammerDB Monitoring Application Metrics (Example-HammerDB.md)
nohup python hammerdb.py -ms 1 -tr -lr 64Gi \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms MySQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log &

wait_process "hammerdb"















###########################################
############## Clean Folder ###############
###########################################


clean_logs
