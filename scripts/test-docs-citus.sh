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


# -dbms Citus                   DBMS under test
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
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Citus \
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
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_citus_1.log

wait_log "$LOG_DIR/doc_ycsb_citus_1.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-2
sleep 30


# -dbms Citus                   DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Citus \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_citus_2.log

wait_log "$LOG_DIR/doc_ycsb_citus_2.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus storage  sf=1  nbp=1  nc=2"


####################################################
################## Benchbase Citus #################
####################################################


# -dbms Citus                   DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms Citus \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_citus_1.log

wait_log "$LOG_DIR/doc_benchbase_citus_1.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus  sf=16  nbp=1,2"

kubectl delete pvc bexhoma-storage-citus-benchbase-tpcc-128
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-3
sleep 30


# -dbms Citus                   DBMS under test
# -sf 128                       scaling factor (controls database size)
# -xsd 20                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 100Gi                    size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms Citus \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 100Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_citus_2.log

wait_log "$LOG_DIR/doc_benchbase_citus_2.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus scale  sf=128  nbp=1,2,4,8"


# -dbms Citus                   DBMS under test
# -sf 128                       scaling factor (controls database size)
# -xsd 20                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xkey                         simulate user think time and keying delays
# -xli 30                       log status to stdout every x seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 100Gi                    size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms Citus \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 4 \
  -nc 2 \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xkey \
  -xli 30 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 100Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_citus_3.log

wait_log "$LOG_DIR/doc_benchbase_citus_3.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus keytime  sf=128  nbp=1,2,5,10  nc=2"


####################################################
################## HammerDB Citus ##################
####################################################


# -dbms Citus                   DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xlat                         collect per-operation latency histograms
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms Citus \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_citus_1.log

wait_log "$LOG_DIR/doc_hammerdb_citus_1.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus  sf=16  nbp=1"

kubectl delete pvc bexhoma-storage-citus-hammerdb-128
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-3
sleep 30


# -dbms Citus                   DBMS under test
# -sf 128                       scaling factor (number of warehouses)
# -xsd 30                       benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 1                        number of data loader pods
# -nlt 128                      threads per loader pod
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod (virtual users)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xlat                         collect per-operation latency histograms
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms Citus \
  -sf 128 \
  -xsd 30 \
  -nc 1 \
  -ne 1 \
  -nlp 1 \
  -nlt 128 \
  -nbp 1,2,4,8 \
  -nbt 128 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_citus_2.log

wait_log "$LOG_DIR/doc_hammerdb_citus_2.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus scale  sf=128  nbp=1,2,4,8"

kubectl delete pvc bexhoma-storage-citus-hammerdb-500
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-3
sleep 30


# -dbms Citus                   DBMS under test
# -sf 500                       scaling factor (number of warehouses)
# -xsd 20                       benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 1                        number of data loader pods
# -nlt 250                      threads per loader pod
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 250                      threads per benchmarking pod (virtual users)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xlat                         collect per-operation latency histograms
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 200Gi                    size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms Citus \
  -sf 500 \
  -xsd 20 \
  -nc 2 \
  -ne 1 \
  -nlp 1 \
  -nlt 250 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 200Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_citus_3.log

wait_log "$LOG_DIR/doc_hammerdb_citus_3.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus large  sf=500  nbp=1,2,5,10  nc=2"


####################################################
#################### TPC-H Citus ###################
####################################################

# -dbms Citus                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms Citus \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


# -dbms Citus                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 14400                      query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms Citus \
  -sf 10 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -tr \
  -rss 50Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus storage  sf=10  ne=1,1  nc=2"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


# -dbms Citus                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nw 4                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -nws 48                       number of shards per worker node
# -xcol                         use columnar storage for tables
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 14400                      query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms Citus \
  -sf 10 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xcol \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -tr \
  -rss 50Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_citus_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus columnar  sf=10  ne=1,1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
