#!/bin/bash
# Basic test runs for the bexhoma test-cases documentation.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


BEXHOMA_NODE_SUT="cl-worker14"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

#!/bin/bash

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














###########################################
################## TPC-H ##################
###########################################



### TPC-H Power Test - only PostgreSQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/testcase_tpch_postgresql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/testcase_tpch_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/testcase_tpch_postgresql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/testcase_tpch_postgresql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 3 \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_tpch_postgresql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/testcase_tpch_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"











###########################################
################ Benchbase ################
###########################################



#### Benchbase Simple (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 16 \
  -xnbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/testcase_benchbase_postgresql_1.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_benchbase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30

### Benchbase Persistency (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 16 \
  -xnbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_benchbase_postgresql_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_benchbase_postgresql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 16 \
  -xnbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/testcase_benchbase_postgresql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_benchbase_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Complex (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1,2 \
  -nbt 8 \
  -xnbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_benchbase_postgresql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_benchbase_postgresql_4.log


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
  run </dev/null &>$LOG_DIR/testcase_hammerdb_postgresql_1.log &


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
  run </dev/null &>$LOG_DIR/testcase_hammerdb_postgresql_2.log &


wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xsd 2 \
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
  run </dev/null &>$LOG_DIR/testcase_hammerdb_postgresql_3.log &


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
  -xtb 131072 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/testcase_ycsb_postgresql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/testcase_ycsb_postgresql_1.log


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
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_ycsb_postgresql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/testcase_ycsb_postgresql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_ycsb_postgresql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_ycsb_postgresql_3.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms PostgreSQL \
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
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/testcase_ycsb_postgresql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_ycsb_postgresql_4.log


#### Wait so that next experiment receives a different code
#sleep 300
wait_process "ycsb"



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 131072 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/testcase_ycsb_postgresql_5.log &

# watch -n 30 tail -n 50 $LOG_DIR/testcase_ycsb_postgresql_5.log


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

