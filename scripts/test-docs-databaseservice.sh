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
# -dbms DatabaseService         DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (x 1000)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_databaseservice_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB DatabaseService ingestion  sf=1  nbp=1"


#### YCSB Execution (Example-CloudDatabase.md)
# -dbms DatabaseService         DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -sl                           skip loading phase (reuse existing data)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
# -dbms DatabaseService         DBMS under test
# -sf 5                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 1Gi                      size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms DatabaseService \
  -sf 5 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 1Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
# -dbms DatabaseService         DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms DatabaseService \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_databaseservice_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase DatabaseService  sf=16  nbp=1,2"

# no PVC, skip loading
# -dbms DatabaseService         DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -sl                           skip loading phase (reuse existing data)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms DatabaseService \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
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
# -dbms DatabaseService         DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_1.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService  sf=3"


#### TCP-H Monitoring (Example-TPC-H.md) — no PVC, skip loading
# -dbms DatabaseService         DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -sl                           skip loading phase (reuse existing data)
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
# -dbms DatabaseService         DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 1Gi                      size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 1Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_databaseservice_3.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H DatabaseService PVC ingestion  sf=3"


#### TCP-H Monitoring (Example-TPC-H.md) — with PVC, execution only
# -dbms DatabaseService         DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 1Gi                      size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms DatabaseService \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 1Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
