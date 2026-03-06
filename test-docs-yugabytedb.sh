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


# Import functions from testfunctions.sh
source ./testfunctions.sh

BEXHOMA_NODE_SUT="cl-worker14"
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













################################################
################## YugaByteDB ##################
################################################


install_yugabytedb() {
  # Parameter: $1 = persistent storage? yes/no
  PERSISTENT=${1:-yes}  # Default: persistent

  if [[ "$PERSISTENT" == "yes" ]]; then
    EPHEMERAL=false
  else
    EPHEMERAL=true
  fi

  helm install bexhoma yugabytedb/yugabyte \
    --version 2025.2.1 \
    --set \
gflags.tserver.ysql_enable_packed_row=true,\
gflags.tserver.ysql_max_connections=1280,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=16Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=16Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=16Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=16Gi,\
storage.master.size=100Gi,\
storage.master.storageClass=shared,\
storage.tserver.size=100Gi,\
storage.tserver.storageClass=shared,\
storage.ephemeral=$EPHEMERAL,\
tserver.livenessProbe.timeoutSeconds=10,\
master.livenessProbe.timeoutSeconds=10,\
enableLoadBalancer=true

  echo "Waiting 60s for pods to start..."
  sleep 60
}

#install_yugabytedb yes   # persistent storage
#install_yugabytedb no    # ephemeral storage
#install_yugabytedb       # default = persistent


remove_yugabytedb() {
  # Parameter: $1 = remove PVCs? yes/no
  REMOVE_PVC=${1:-no}  # default: do NOT remove PVCs

  echo "Deleting Helm release bexhoma..."
  helm delete bexhoma

  if [[ "$REMOVE_PVC" == "yes" ]]; then
    echo "Removing PVCs for yb-tserver and yb-master..."
    kubectl delete pvc -l app=yb-tserver
    kubectl delete pvc -l app=yb-master
  else
    echo "Keeping PVCs (persistent storage not deleted)"
  fi

  echo "Waiting 60s for cleanup..."
  sleep 60
}

#remove_yugabytedb yes   # Helm release + PVCs
#remove_yugabytedb no    # nur Helm release, PVCs behalten
#remove_yugabytedb       # default = no


# install YugabyteDB
install_yugabytedb no

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

# skip loading, because previous process has generated it
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
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30

kubectl delete pvc bexhoma-storage-yugabytedb-ycsb-1
sleep 30

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
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


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
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &


wait_process "benchbase"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30

# kubectl patch statefulset yb-tserver --type=merge -p '
# spec:
#   template:
#     spec:
#       containers:
#       - name: yb-tserver
#         livenessProbe:
#           exec:
#             command: ["true"]
# '

# kubectl patch statefulset yb-master --type=merge -p '
# spec:
#   template:
#     spec:
#       containers:
#       - name: yb-master
#         livenessProbe:
#           exec:
#             command: ["true"]
# '


#### Benchbase More Complex (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -slg 30 \
  -sd 20 \
  -xkey \
  -dbms YugabyteDB \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_2.log &


wait_process "benchbase"


# remove YugabyteDB installation
remove_yugabytedb no






################################################
######## YugaByteDB Application Metrics ########
################################################


# install YugabyteDB
install_yugabytedb no
sleep 30

nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_ycsb_run_yugabytedb_appmetrics.log &

wait_process "ycsb"


# remove YugabyteDB installation
remove_yugabytedb no


# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Simple (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log &

wait_process "benchbase"


# remove YugabyteDB installation
remove_yugabytedb no



###########################################
############## Clean Folder ###############
###########################################


clean_logs
