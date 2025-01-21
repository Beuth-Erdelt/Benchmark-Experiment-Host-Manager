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


BEXHOMA_NODE_SUT="cl-worker20"
BEXHOMA_NODE_LOAD="cl-worker13"
BEXHOMA_NODE_BENCHMARK="cl-worker13"
#BEXHOMA_NODE_BENCHMARK="cl-worker11"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR

# Define the wait_process function
wait_process() {
    local process_name=$1

    # Wait until the process with the name passed as an argument has terminated
    while ps aux | grep "[p]ython $process_name.py" > /dev/null; do
        # Process is still running, wait for 5 seconds
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for process python $process_name.py to terminate..."
        sleep 60
    done

    echo "$(date +"%Y-%m-%d %H:%M:%S"): Process python $process_name.py has terminated."
}

# Example usage
#wait_process "tpch"


# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"














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
  -nbp 1 \
  -nbt 64 \
  -nbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_workload_a.log &


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

