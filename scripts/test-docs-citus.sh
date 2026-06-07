#!/bin/bash
# Generates documentation summaries for Citus experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




####################################################
#################### YCSB Citus ####################
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Citus                   DBMS under test
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
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_ycsb_citus_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-2
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Citus                   DBMS under test
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
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_ycsb_citus_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus storage  sf=1  nbp=1  nc=2"


####################################################
################## Benchbase Citus #################
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dbms Citus                   DBMS under test
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
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_citus_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus  sf=16  nbp=1,2"

kubectl delete pvc bexhoma-storage-citus-benchbase-tpcc-128
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-3
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (controls database size)
# -sd 20                        benchmark duration in minutes
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dbms Citus                   DBMS under test
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 128 \
  -sd 20 \
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
  run &>$LOG_DIR/doc_benchbase_citus_2.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus scale  sf=128  nbp=1,2,4,8"


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (controls database size)
# -sd 20                        benchmark duration in minutes
# -slg 30                       log status to stdout every x seconds
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xkey                         simulate user think time and keying delays
# -dbms Citus                   DBMS under test
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -nc 2                         number of repeated runs per configuration
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 128 \
  -sd 20 \
  -slg 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xkey \
  -dbms Citus \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 4 \
  -tb 1024 \
  -m -mc \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run &>$LOG_DIR/doc_benchbase_citus_3.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus keytime  sf=128  nbp=1,2,5,10  nc=2"


####################################################
################## HammerDB Citus ##################
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -dbms Citus                   DBMS under test
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nlt 8                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_hammerdb_citus_1.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus  sf=16  nbp=1"

kubectl delete pvc bexhoma-storage-citus-hammerdb-128
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-3
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (number of warehouses)
# -sd 30                        benchmark duration in minutes
# -xlat                         collect per-operation latency histograms
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dbms Citus                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nlp 1                        number of data loader pods
# -nlt 128                      threads per loader pod
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod (virtual users)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/doc_hammerdb_citus_2.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus scale  sf=128  nbp=1,2,4,8"

kubectl delete pvc bexhoma-storage-citus-hammerdb-500
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-3
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 500                       scaling factor (number of warehouses)
# -sd 20                        benchmark duration in minutes
# -xlat                         collect per-operation latency histograms
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dbms Citus                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nlp 1                        number of data loader pods
# -nlt 250                      threads per loader pod
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 250                      threads per benchmarking pod (virtual users)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 200Gi                    size of the persistent volume claim
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 500 \
  -sd 20 \
  -xlat \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 250 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 200Gi \
  run &>$LOG_DIR/doc_hammerdb_citus_3.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus large  sf=500  nbp=1,2,5,10  nc=2"


####################################################
#################### TPC-H Citus ###################
####################################################

# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (controls database size in GB)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dt                           disable result type checking
# -t 1200                       query timeout in seconds
# -dbms Citus                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
bexhoma tpch -ms $BEXHOMA_MS -tr \
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
  run &>$LOG_DIR/test_tpch_testcase_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (controls database size in GB)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dt                           disable result type checking
# -t 14400                      query timeout in seconds
# -dbms Citus                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS -tr \
  -sf 10 \
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
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/test_tpch_testcase_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus storage  sf=10  ne=1,1  nc=2"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (controls database size in GB)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -dt                           disable result type checking
# -t 14400                      query timeout in seconds
# -dbms Citus                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -icol                         use columnar storage for tables
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS -tr \
  -sf 10 \
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
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/test_tpch_testcase_citus_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus columnar  sf=10  ne=1,1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
