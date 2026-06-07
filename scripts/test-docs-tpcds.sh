#!/bin/bash
# Generates documentation summaries for TPC-DS experiments.
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
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_compare.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS compare  sf=1"


#### TCP-DS Monitoring (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms MonetDB                 DBMS under test
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr \
  -dbms MonetDB \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_monitoring.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS monitoring  sf=3"


#### TCP-DS Throughput (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms MonetDB                 DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nc 1                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_throughput.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-1
sleep 30


#### TCP-DS Persistent Storage (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms MonetDB                 DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 1                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_storage.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS storage  sf=1  nc=2"


###########################################
############# TPC-DS MonetDB ##############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-30
sleep 30


#### TCP-DS Power 30 (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 30                        scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -dbms MonetDB                 DBMS under test
# -rr 1024Gi                    RAM requested for the SUT container
# -lr 1024Gi                    RAM limit for the SUT container
# -t 14400                      query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma tpcds -ms $BEXHOMA_MS \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi -rsr \
  run &>$LOG_DIR/doc_tpcds_monetdb_1.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=1  ne=1"


#### TCP-DS Power 30 repeated (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 30                        scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -dbms MonetDB                 DBMS under test
# -rr 1024Gi                    RAM requested for the SUT container
# -lr 1024Gi                    RAM limit for the SUT container
# -t 14400                      query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
bexhoma tpcds -ms $BEXHOMA_MS \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_2.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=2  ne=1,1"


#### TCP-DS Throughput 30 (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sf 30                        scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1,1,3                     parallel client counts to sweep (comma-separated)
# -dbms MonetDB                 DBMS under test
# -rr 1024Gi                    RAM requested for the SUT container
# -lr 1024Gi                    RAM limit for the SUT container
# -t 14400                      query timeout in seconds
# -dt                           disable result type checking
# -rst shared                   storage class for persistent volumes
# -rss 1000Gi                   size of the persistent volume claim
bexhoma tpcds -ms $BEXHOMA_MS \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_3.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB throughput  sf=30  ne=1,1,3"


###########################################
############ Profiling MonetDB ############
###########################################


#### TCP-DS Profiling (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -dbms MonetDB                 DBMS under test
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 10                        scaling factor (controls database size in GB)
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -ne 1,1                       parallel client counts to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr \
  -dbms MonetDB \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -ne 1,1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi \
  profiling &>$LOG_DIR/doc_tpcds_testcase_profiling.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS profiling  sf=10  ne=1,1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
