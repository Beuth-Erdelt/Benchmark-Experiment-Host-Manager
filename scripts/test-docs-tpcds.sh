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


#### TCP-DS PostgreSQL (Example-TPC-DS.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL  sf=1"


#### TCP-DS Monitoring (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
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
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS monitoring  sf=3"


#### TCP-DS Throughput (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
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
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 1 \
  -nc 1 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_throughput.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-1
sleep 30


#### TCP-DS Persistent Storage (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_postgresql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS storage  sf=1  nc=2"


###########################################
############# TPC-DS MonetDB ##############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-30
sleep 30


#### TCP-DS Power 30 (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
# -sf 30                        scaling factor (controls database size in GB)
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
# -t 14400                      query timeout in seconds
# -lr 1024Gi                    RAM limit for the SUT container
# -rr 1024Gi                    RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 2000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rsr \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=1  ne=1"


#### TCP-DS Power 30 repeated (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
# -sf 30                        scaling factor (controls database size in GB)
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
# -t 14400                      query timeout in seconds
# -lr 1024Gi                    RAM limit for the SUT container
# -rr 1024Gi                    RAM requested for the SUT container
# -rss 2000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=2  ne=1,1"


#### TCP-DS Throughput 30 (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
# -sf 30                        scaling factor (controls database size in GB)
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
# -t 14400                      query timeout in seconds
# -lr 1024Gi                    RAM limit for the SUT container
# -rr 1024Gi                    RAM requested for the SUT container
# -rss 2000Gi                   size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
bexhoma tpcds \
  -dbms MonetDB \
  -sf 30 \
  -nc 1 \
  -ne 1,1,3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -lr 1024Gi \
  -rr 1024Gi \
  -rss 2000Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_monetdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB throughput  sf=30  ne=1,1,3"


###########################################
############ Profiling MonetDB ############
###########################################


#### TCP-DS Profiling (Example-TPC-DS.md)
# -dbms MonetDB                 DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
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
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 10 \
  -ne 1,1 \
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
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  profiling &>$LOG_DIR/docs_tpcds_postgresql_profiling.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS profiling  sf=10  ne=1,1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
