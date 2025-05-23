#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - Basic Runs for the Test Cases Doc File
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
################## TPC-H ##################
###########################################



### TPC-H Power Test - only PostgreSQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_postgresql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
  -dt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"











###########################################
################ Benchbase ################
###########################################



#### Benchbase Simple (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_1.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30

### Benchbase Persistency (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 16 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Complex (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 8 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_postgresql_4.log


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "benchbase"





###########################################
################ HammerDB #################
###########################################




### HammerDB Simple (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_1.log &


wait_process "hammerdb"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


### HammerDB Monitoring (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_2.log &


wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -xlat \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
    -m -mc \
    -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
#sleep 3000
wait_process "hammerdb"
















###########################################
################## YCSB ###################
###########################################







### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 30

### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_postgresql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_postgresql_4.log


#### Wait so that next experiment receives a different code
#sleep 300
wait_process "ycsb"



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_5.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_postgresql_5.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"












###########################################
############## Clean Folder ###############
###########################################



export MYDIR=$(pwd)
cd $LOG_DIR
# remove connection errors from logs
grep -rl "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens." . | xargs sed -i '/Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens./d'
cd $MYDIR

# Loop over each text file in the source directory
for file in "$LOG_DIR"/*.log; do
    # Get the filename without the path and extension
    echo "Cleaning $file"
    filename=$(basename "$file" .log)
    # Extract lines starting from "## Show Summary" and save as <filename>_summary.txt in the destination directory
    awk '/## Show Summary/ {show=1} show {print}' "$file" > "$LOG_DIR/${filename}_summary.txt"
done

echo "Extraction complete! Files are saved in $LOG_DIR."

