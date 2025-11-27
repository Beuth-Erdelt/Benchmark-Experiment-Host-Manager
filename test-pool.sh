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
################## YCSB PGBouncer ##################
####################################################


nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_1.log &


wait_process "ycsb"


nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  -rst shared -rss 100Gi -rsr \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_2.log &


wait_process "ycsb"


nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn.log &


wait_process "benchbase"


#### Benchbase Scale (Example-Benchbase.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_newconn_pool.log &


wait_process "benchbase"










####################################################
################## YCSB PGBouncer ##################
####################################################







### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 4,16,32 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -npp 4 \
  -npi 64 \
  -npo 64 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_1.log &


wait_process "ycsb"


### YCSB Execution Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 4,16,32 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_2.log &


wait_process "ycsb"


### YCSB Execution Test for Scaling the Driver with PVC (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 4,16,32 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_3.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with 64 connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
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
  -nci 64 \
  -nco 1,2,4,8,16 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_4.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with 128 connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
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
  -nci 128 \
  -nco 4,8,16,32 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_tmp_6.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with number of incoming and outgoing connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
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
  -nci 16,32,64,128,256 \
  -nco 16,32,64,128,256 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_tmp_7.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with number of incoming and outgoing connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 131072 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -nci 64 \
  -nco 64 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_tmp_8.log &


wait_process "ycsb"















####################################################
################### Cloud-native ###################
####################################################


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16


### Small functional test
### Fixed nodes
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 64 \
  -nbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_0.log &


wait_process "ycsb"


### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 98304 to 229376
### threads range from 48 to 120 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -nbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_1.log &


wait_process "ycsb"


### Same with PVC
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 98304 to 229376
### threads range from 48 to 120 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -nbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_2.log &


wait_process "ycsb"


### Same with workload C2
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 98304 to 229376
### threads range from 48 to 120 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -nbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_3.log &


wait_process "ycsb"


BEXHOMA_YCSB_SF_DATA=1
BEXHOMA_YCSB_SF_OPS=16


### Fixed nodes
### Try small amount of data
### repeat for 1 driver and 8 drivers
### TODO: Set target and threads
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_4.log &


wait_process "ycsb"


BEXHOMA_YCSB_SF_DATA=64
BEXHOMA_YCSB_SF_OPS=16

### Fixed nodes
### Try big amount of data
### repeat for 1 driver and 8 drivers
### TODO: Set target and threads
### TODO: Size possible?
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_5.log &


wait_process "ycsb"


BEXHOMA_YCSB_SF_DATA=64
BEXHOMA_YCSB_SF_OPS=64


### Same with higher number of data and ops
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 98304 to 229376
### threads range from 48 to 120 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -nbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_6.log &


wait_process "ycsb"


BEXHOMA_YCSB_SF_DATA=64
BEXHOMA_YCSB_SF_OPS=128


### Same with higher number of data and ops
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -nbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_7.log &


wait_process "ycsb"



BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=256


### Same with higher number of data and ops
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -nbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_8.log &


wait_process "ycsb"



BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=512


### Same with higher number of data and ops
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -nbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_9.log &


wait_process "ycsb"



BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16

### 16 pods
### Fixed nodes
### Try big amount of data
### repeat for 1 driver and 8 drivers
### TODO: Set target and threads
### TODO: Size possible?
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,16 \
  -nbt 64 \
  -nbf 12 \
  -ne 2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_10.log &


wait_process "ycsb"





BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16

### target = 0
### Fixed nodes
### Try big amount of data
### repeat for 1 driver and 8 drivers
### TODO: Set target and threads
### TODO: Size possible?
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 0 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 0 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_11.log &


wait_process "ycsb"





BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=512


### High number of data and ops
### no target
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8,16 \
  -nbt 96,104,112,120,128,136 \
  -nbf 0 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_12.log &


wait_process "ycsb"





BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=256


### High number of data and ops
### no target
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers and 16 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -nbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_13.log &


wait_process "ycsb"





BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=256

### same but uniform
### High number of data and ops
### no target
### Fixed nodes
### Scan for peak performance
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -nbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_14.log &


wait_process "ycsb"



BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=256


### High number of data and ops
### Fixed nodes
### only 128 threads, target = 180224
### different measurement of latencies - hdrhistogram
### repeat for 1 driver and 8 drivers and 16 drivers
#-p hdrhistogram.fileoutput=true
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,1,8,16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_15.log &


wait_process "ycsb"




BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=64


### Redis
### Fixed nodes
### only 128 threads, no target
### repeat for 1 driver and 8 drivers and 16 drivers
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,1,8 \
  -nbt 128 \
  -nbf 0 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_16.log &


wait_process "ycsb"




BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=64


### Redis
### Fixed nodes
### scan for 128 threads, no target
### repeat for 1 driver and 8 drivers and 16 drivers
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 1,2,4,8,16,32,48,64,96,128 \
  -nbf 0 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_17.log &


wait_process "ycsb"





BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=256


### High number of data and ops
### no target
### Fixed nodes
### Scan for peak performance
### different measurement of latencies - hdrhistogram
### base is 16384 - scan from 163840 to 229376
### threads range from 104 to 136 in steps of 8
### repeat for 1 driver and 8 drivers and 16 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -nbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_cn_18.log &


wait_process "ycsb"







BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16


### Small functional test
### Fixed nodes
### Workload A
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1,8,16 \
  -nbt 64 \
  -nbf 12 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_workload_a2.log &


wait_process "ycsb"







BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16


### Small functional test - low target
### Fixed nodes
### Workload A
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8,16 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_workload_a3.log &


wait_process "ycsb"




BEXHOMA_YCSB_SF_DATA=16
BEXHOMA_YCSB_SF_OPS=16


### Small functional test - low target - same, but 60s interval ycsb metrics
### Fixed nodes
### Workload A
### repeat for 1 driver and 8 drivers
### TODO: Do the same for PGBouncer sidecar? Check resources first
nohup python ycsb.py -ms 1 -tr \
  -sf $BEXHOMA_YCSB_SF_DATA \
  -sfo $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8,16 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_workload_a4.log &


wait_process "ycsb"



###########################################
############## Clean Folder ###############
###########################################


clean_logs
