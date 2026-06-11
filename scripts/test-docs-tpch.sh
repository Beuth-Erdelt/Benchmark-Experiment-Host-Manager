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


#### TCP-H Compare (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_compare.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H compare  sf=1"


#### TCP-H Monitoring (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms PostgreSQL              DBMS under test
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 10                        scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms PostgreSQL \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_monitoring.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H monitoring  sf=10"


#### TCP-H Throughput (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_throughput.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


#### TCP-H Persistent Storage (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_storage.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H storage  sf=1  nc=2"


#### TCP-H Fractional Scaling Factor (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 0.1                       scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 0.1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 5Gi -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_fractional.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H fractional  sf=0.1  nc=2"


###########################################
############# TPC-H MonetDB ###############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpch-100
sleep 30


#### TCP-H Power 100 (Example-Result-TPC-H-MonetDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 100                       scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -dbms MonetDB                 DBMS under test
# -rr 256Gi                     RAM requested for the SUT container
# -lr 256Gi                     RAM limit for the SUT container
# -t 3600                       query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_1.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=1  ne=1"


#### TCP-H Power 100 repeated (Example-Result-TPC-H-MonetDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 100                       scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -dbms MonetDB                 DBMS under test
# -rr 256Gi                     RAM requested for the SUT container
# -lr 256Gi                     RAM limit for the SUT container
# -t 3600                       query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_2.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=2  ne=1,1"


#### TCP-H Throughput 100 (Example-Result-TPC-H-MonetDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 100                       scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1,1,3                     parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -dbms MonetDB                 DBMS under test
# -rr 256Gi                     RAM requested for the SUT container
# -lr 256Gi                     RAM limit for the SUT container
# -t 3600                       query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
bexhoma tpch -ms $BEXHOMA_MS \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_3.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB throughput  sf=100  ne=1,1,3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
