#!/bin/bash
# Test runs comparing PostgreSQL with and without PGBouncer connection pooling.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

# Config nodes and paths
BEXHOMA_NODE_SUT="cl-worker14"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

# Check for file
if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

# Check for directories
for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."


if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."

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
  -xop 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 4,16,32 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -xnpp 4 \
  -xnpi 64 \
  -xnpo 64 \
  run </dev/null &>$LOG_DIR/docs_ycsb_pgbouncer_1.log &


wait_process "ycsb"


### YCSB Execution Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 4,16,32 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/docs_ycsb_pgbouncer_2.log &


wait_process "ycsb"


### YCSB Execution Test for Scaling the Driver with PVC (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 4,16,32 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_3.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with 64 connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -nci 64 \
  -nco 1,2,4,8,16 \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_4.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with 128 connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -nci 128 \
  -nco 4,8,16,32 \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_tmp_6.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with number of incoming and outgoing connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -nci 16,32,64,128,256 \
  -nco 16,32,64,128,256 \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_pgbouncer_tmp_7.log &


wait_process "ycsb"


### YCSB Loader Test for Scaling the Pooler with number of incoming and outgoing connections (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 16 \
  -xop 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -nci 64 \
  -nco 64 \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -xnbf 6,7,8,9,10,11,12,13,14 \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -xnbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -xnbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 10Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 12 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 200Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 48,56,64,72,80,88,96,104,112,120 \
  -xnbf 6,7,8,9,10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 200Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -xnbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 200Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -xnbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8 \
  -nbt 104,112,120,128,136 \
  -xnbf 10,11,12,13,14 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,16 \
  -nbt 64 \
  -xnbf 12 \
  -ne 2 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 0 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 0 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8,16 \
  -nbt 96,104,112,120,128,136 \
  -xnbf 0 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -xnbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -xnbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,1,8,16 \
  -nbt 128 \
  -xnbf 11 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,1,8 \
  -nbt 128 \
  -xnbf 0 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1 \
  -nbt 1,2,4,8,16,32,48,64,96,128 \
  -xnbf 0 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload c \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8,16 \
  -nbt 80,96,112,128,144,160,176,192 \
  -xnbf 0,9,10,11,12,13,14,15,16 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 12 \
  -nbp 1,8,16 \
  -nbt 64 \
  -xnbf 12 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8,16 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
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
  -xop $BEXHOMA_YCSB_SF_OPS \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8,16 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst $BEXHOMA_STORAGE_CLASS -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_workload_a4.log &


wait_process "ycsb"



###########################################
############## Clean Folder ###############
###########################################


clean_logs
