#!/bin/bash
# Generates documentation summaries for TPC-H experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




###########################################
################# TPC-H ###################
###########################################


#### TCP-H PostgreSQL (Example-TPC-H.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_postgresql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL  sf=1"


#### TCP-H Monitoring (Example-TPC-H.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H monitoring  sf=10"


#### TCP-H Throughput (Example-TPC-H.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_throughput.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


#### TCP-H Persistent Storage (Example-TPC-H.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 30Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H storage  sf=1  nc=2"


#### TCP-H Fractional Scaling Factor (Example-TPC-H.md)
# -dbms PostgreSQL              DBMS under test
# -sf 0.1                       scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 5Gi                      size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 0.1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 5Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_fractional.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H fractional  sf=0.1  nc=2"

bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -xrs 3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H refresh  sf=1  ne=3"

###########################################
############# TPC-H MonetDB ###############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpch-100
sleep 30


#### TCP-H Power 100 (Example-Result-TPC-H-MonetDB.md)
# -dbms MonetDB                 DBMS under test
# -sf 100                       scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 3600                       query timeout in seconds
# -lr 256Gi                     RAM limit for the SUT container
# -rr 256Gi                     RAM requested for the SUT container
# -rss 1000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_monetdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=1  ne=1"


#### TCP-H Power 100 repeated (Example-Result-TPC-H-MonetDB.md)
# -dbms MonetDB                 DBMS under test
# -sf 100                       scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 3600                       query timeout in seconds
# -lr 256Gi                     RAM limit for the SUT container
# -rr 256Gi                     RAM requested for the SUT container
# -rss 1000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_monetdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=2  ne=1,1"


#### TCP-H Throughput 100 (Example-Result-TPC-H-MonetDB.md)
# -dbms MonetDB                 DBMS under test
# -sf 100                       scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1,1,3                     parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 3600                       query timeout in seconds
# -lr 256Gi                     RAM limit for the SUT container
# -rr 256Gi                     RAM requested for the SUT container
# -rss 1000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MonetDB \
  -sf 100 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 3600 \
  -lr 256Gi \
  -rr 256Gi \
  -rss 1000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_monetdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB throughput  sf=100  ne=1,1,3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
