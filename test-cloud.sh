#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - Test scripts for database services
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


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
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













################################################
################## YugaByteDB ##################
################################################


install_yugabytedb() {
  helm install bexhoma yugabytedb/yugabyte \
  --version 2.23.0 \
  --set \
  gflags.tserver.ysql_enable_packed_row=true,\
  resource.master.limits.cpu=2,\
  resource.master.limits.memory=8Gi,\
  resource.master.requests.cpu=2,\
  resource.master.requests.memory=8Gi,\
  resource.tserver.limits.cpu=8,\
  resource.tserver.limits.memory=8Gi,\
  resource.tserver.requests.cpu=8,\
  resource.tserver.requests.memory=8Gi,\
  storage.master.size=100Gi,\
  storage.tserver.size=100Gi,\
  storage.ephemeral=true,\
  tserver.tolerations[0].effect=NoSchedule,\
  tserver.tolerations[0].key=nvidia.com/gpu,\
  enableLoadBalancer=True
  sleep 60
}

remove_yugabytedb() {
  helm delete bexhoma
  kubectl delete pvc -l app=yb-tserver
  kubectl delete pvc -l app=yb-master
  sleep 60
}

# install YugabyteDB
install_yugabytedb

#### YCSB Ingestion (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_1.log &


wait_process "ycsb"


#### YCSB Execution (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -sl \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_2.log &


wait_process "ycsb"


# remove YugabyteDB installation
remove_yugabytedb

# install YugabyteDB
install_yugabytedb


#### YCSB Dummy Persistent Storage (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_3.log &


wait_process "ycsb"


# remove YugabyteDB installation
remove_yugabytedb

# install YugabyteDB
install_yugabytedb


#### Benchbase Simple (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &


wait_process "benchbase"


# remove YugabyteDB installation
remove_yugabytedb

# install YugabyteDB
install_yugabytedb


#### Benchbase More Complex (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -dbms YugabyteDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_2.log &


wait_process "benchbase"


# remove YugabyteDB installation
remove_yugabytedb







#################################################
################## CockroachDB ##################
#################################################


#### YCSB Ingestion (Example-CockroachDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms CockroachDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_1.log &


wait_process "ycsb"


#### YCSB Execution (Example-CockroachDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sl \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms CockroachDB \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_2.log &


wait_process "ycsb"


#### Benchbase Simple (Example-CockroachDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_1.log &


wait_process "benchbase"


#### Benchbase Complex (Example-CockroachDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_2.log &


wait_process "benchbase"
















###############################################################
################### YCSB Database Service #####################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10


#### YCSB Ingestion (Example-CloudDatabase.md)
nohup python ycsb.py -ms 2 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
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
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_1.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"


#### YCSB Execution (Example-CloudDatabase.md)
nohup python ycsb.py -ms 2 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms DatabaseService \
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
  -sl \
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_2.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"

# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10

# delete pvc of placeholder
kubectl delete pvc bexhoma-storage-databaseservice-ycsb-1

sleep 10


#### YCSB Persistent Storage (Example-CloudDatabase.md)
nohup python ycsb.py -ms 2 -tr \
  -sf 5 \
  -sfo 10 \
  --workload a \
  -dbms DatabaseService \
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
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_databaseservice_3.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"













###############################################################
################# Benchbase Database Service ##################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10


# no PVC
nohup python benchbase.py -ms 2 -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_databaseservice_1.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"

# no PVC, skip loading
nohup python benchbase.py -ms 2 -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -sl \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_databaseservice_2.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"










###############################################################
################### TPC-H Database Service ####################
###############################################################


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10


#### TCP-H Monitoring (Example-CloudDatabase.md)
# no PVC
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_1.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


#### TCP-H Monitoring (Example-TPC-H.md)
# no PVC, skip loading
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -sl \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_2.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


# delete pvc of placeholder
kubectl delete pvc bexhoma-storage-databaseservice-tpch-3

sleep 10

# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

sleep 10

# login into database service placeholder
# kubectl port-forward svc/bexhoma-service 9091:9091

#### TCP-H Monitoring (Example-TPC-H.md)
# with PVC, ingestion
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_3.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


#### TCP-H Monitoring (Example-TPC-H.md)
# with PVC, execution only
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_4.log &

#### Wait so that next experiment receives a different code
#sleep 600
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

