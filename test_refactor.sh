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
LOG_DIR="./logs_tests/local"

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





install_yugabytedb() {
  helm install bexhoma yugabytedb/yugabyte \
  --version 2.23.0 \
  --set \
gflags.tserver.ysql_enable_packed_row=true,\
gflags.tserver.ysql_max_connections=1280,\
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




#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_postgresql_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"






#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms PGBouncer \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  -npi 32 \
  -npo 32 \
  run </dev/null &>$LOG_DIR/refactor_pgbouncer_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"





#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  --workload a \
  -dbms TiDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_tidb_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"




#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_cockroachdb_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"







#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms Citus \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_citus_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"




nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_redis_1.log &


wait_process "ycsb"








################################################
################## YugaByteDB ##################
################################################


# install YugabyteDB
install_yugabytedb
sleep 30





#### YCSB Persistent Storage (Example-YCSB.md)
nohup python ycsb.py -tr \
  -sf 1 \
  --workload a \
  -dbms YugabyteDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 30Gi -rsr \
  run </dev/null &>$LOG_DIR/refactor_yugabytedb_1.log &

#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"




# remove YugabyteDB installation
remove_yugabytedb
sleep 30



