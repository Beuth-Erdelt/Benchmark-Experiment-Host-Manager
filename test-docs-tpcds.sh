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
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare.log &


#### Wait so that next experiment receives a different code
#sleep 7200
wait_process "tpcds"


#### TCP-DS Monitoring (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monitoring.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


#### TCP-DS Throughput (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_throughput.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-1
sleep 30


#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


nohup python tpcds.py -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 0.1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 5Gi -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_fractional.log &

wait_process "tpcds"


###########################################
############# TPC-DS MonetDB ##############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-100
sleep 30


#### TCP-DS Power 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_1.log &


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "tpcds"


#### TCP-DS Power 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_2.log &


#### Wait so that next experiment receives a different code
#sleep 4800
wait_process "tpcds"


#### TCP-DS Throughput 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 1000Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_monetdb_3.log &

#### Wait so that next experiment receives a different code
#sleep 4800
wait_process "tpcds"







###########################################
############ Profiling MonetDB ############
###########################################


#### TCP-H Profiling (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -ne 1,1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi \
  profiling </dev/null &>$LOG_DIR/doc_tpcds_testcase_profiling.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"



###########################################
############## Clean Folder ###############
###########################################


clean_logs
