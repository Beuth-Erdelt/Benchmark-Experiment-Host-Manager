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
#################### YCSB Redis ####################
####################################################


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"


# Single host Redis
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_1.log &


wait_process "ycsb"


# Cluster of 3 Redis instances
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_2.log &


wait_process "ycsb"

# Cluster of 3 Redis instances and replication
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_3.log &


wait_process "ycsb"


kubectl delete pvc bexhoma-storage-redis-ycsb-1

# Single host Redis with PVC
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_4.log &


wait_process "ycsb"


# Cluster of 3 Redis instances and PVC
########### does not work - redis nodes rely on IPs and do not find eachother after restart

kubectl delete pvc bexhoma-storage-redis-ycsb-1
kubectl delete pvc bexhoma-workers-bx-w-redis-ycsb-1-0
kubectl delete pvc bexhoma-workers-bx-w-redis-ycsb-1-1
kubectl delete pvc bexhoma-workers-bx-w-redis-ycsb-1-2


nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_redis_5.log &


wait_process "ycsb"












####################################################
#################### YCSB Citus ####################
####################################################


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"


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

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-64-8-65536-citus-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-64-8-65536-citus-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-64-8-65536-citus-2
sleep 30


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
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_citus_2.log &


wait_process "ycsb"


####################################################
################## Benchbase Citus #################
####################################################


nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_1.log &


wait_process "benchbase"


kubectl delete pvc bexhoma-storage-citus-benchbase-128
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-benchbase-128-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-benchbase-128-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-benchbase-128-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-benchbase-128-3
sleep 30


nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_2.log &


wait_process "benchbase"


python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -slg 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 1024 \
  -nbf 4 \
  -tb 1024 \
  -m -mc \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/doc_benchbase_citus_3.log &


wait_process "benchbase"



####################################################
################## HammerDB Citus ##################
####################################################



nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms Citus \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_1.log &


wait_process "hammerdb"


kubectl delete pvc bexhoma-storage-citus-hammerdb-128
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-128-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-128-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-128-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-128-3
sleep 30


nohup python hammerdb.py -ms 1 -tr \
  -sf 128 \
  -sd 30 \
  -xlat \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 128 \
  -nbp 1,2,4,8 \
  -nbt 128 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_2.log &


wait_process "hammerdb"


kubectl delete pvc bexhoma-storage-citus-hammerdb-500
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-500-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-500-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-500-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-hammerdb-500-3
sleep 30


nohup python hammerdb.py -ms 1 -tr \
  -sf 500 \
  -sd 20 \
  -xlat \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 500 \
  -nbp 1,2,5,10 \
  -nbt 5000 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 200Gi \
  run </dev/null &>$LOG_DIR/doc_hammerdb_citus_3.log &


wait_process "hammerdb"




####################################################
#################### TPC-H Citus ###################
####################################################

nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 1200 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_1.log &


wait_process "tpch"


kubectl delete pvc bexhoma-storage-citus-tpch-100
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-3
sleep 30


nohup python tpch.py -ms 1 -tr \
  -sf 100 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 14400 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -rst shared -rss 150Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_2.log &


wait_process "tpch"



kubectl delete pvc bexhoma-storage-citus-tpch-100
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-0
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-1
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-2
kubectl delete pvc bexhoma-workers-bexhoma-worker-citus-tpch-100-3
sleep 30


nohup python tpch.py -ms 1 -tr \
  -sf 100 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 14400 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -icol \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -rst shared -rss 150Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_citus_3.log &


wait_process "tpch"







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

