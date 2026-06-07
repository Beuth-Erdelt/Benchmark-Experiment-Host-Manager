#!/bin/bash
# Generates documentation summaries for managed database service experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh

BEXHOMA_MS=2



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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 1                        number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms DatabaseService         DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_ycsb_databaseservice_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB DatabaseService ingestion  sf=1  nbp=1"


#### YCSB Execution (Example-CloudDatabase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms DatabaseService         DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sl                           skip loading phase (reuse existing data)
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_ycsb_databaseservice_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB DatabaseService execution skip-load  sf=1  nbp=1"

# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service placeholder
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml

# we have to be sure the "cloud service" is ready - bexhoma does not check this in case dbms is not managed by bexhoma
sleep 300

# delete pvc of placeholder
kubectl delete pvc bexhoma-storage-databaseservice-ycsb-5

sleep 10


#### YCSB Persistent Storage (Example-CloudDatabase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 5                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms DatabaseService         DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 1Gi                      size of the persistent volume claim
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_ycsb_databaseservice_3.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB DatabaseService storage  sf=5  nbp=1"




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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms DatabaseService         DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_databaseservice_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase DatabaseService  sf=16  nbp=1,2"

# no PVC, skip loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms DatabaseService         DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -sl                           skip loading phase (reuse existing data)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -sl \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_databaseservice_2.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase DatabaseService skip-load  sf=16  nbp=1,2"




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


#### TCP-H Monitoring (Example-CloudDatabase.md) — no PVC
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms DatabaseService         DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -t 1200                       query timeout in seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_1.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService  sf=3"


#### TCP-H Monitoring (Example-TPC-H.md) — no PVC, skip loading
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms DatabaseService         DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -t 1200                       query timeout in seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -sl                           skip loading phase (reuse existing data)
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -sl \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_2.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService skip-load  sf=3"


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


#### TCP-H Monitoring (Example-TPC-H.md) — with PVC, ingestion
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms DatabaseService         DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -t 1200                       query timeout in seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 1Gi                      size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_3.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService PVC ingestion  sf=3"


#### TCP-H Monitoring (Example-TPC-H.md) — with PVC, execution only
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms DatabaseService         DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -t 1200                       query timeout in seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 1Gi                      size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_4.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService PVC execution  sf=3"


# delete database service placeholder
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service


###########################################
############## Clean Folder ###############
###########################################


clean_logs
