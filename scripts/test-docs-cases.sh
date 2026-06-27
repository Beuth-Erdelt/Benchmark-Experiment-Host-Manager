#!/bin/bash
# Extended test runs covering additional DBMS and parameter combinations.
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


#### TCP-H Compare (TestCases.md)
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
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H compare  sf=1"


###########################################
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (TestCases.md)
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
  run &>$LOG_DIR/testcase_tpcds_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS compare  sf=1"


###########################################
############### TPC-H MySQL ###############
###########################################


#### TCP-H Power Test - only MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL simple  sf=1"


#### TCP-H Monitoring - MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpch-1
sleep 30


#### TCP-H Throughput Test - MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL throughput  sf=10  ne=1,2"


#### TPC-H RAM Disk Test - MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect metrics for the whole experiment
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rst ramdisk                  storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mysql_ramdisk.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL ramdisk  sf=10"


###########################################
############ TPC-H PostgreSQL #############
###########################################


#### TCP-H Power Test - only PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
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
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL simple  sf=1"


#### TCP-H Monitoring - PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 100Gi                    size of the persistent volume claim
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
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


#### TCP-H Throughput Test - PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
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
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL throughput  sf=10  ne=1,2"


#### TPC-H RAM Disk Test - PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect metrics for the whole experiment
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rst ramdisk                  storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rst ramdisk \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_postgresql_ramdisk.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL ramdisk  sf=3"


###########################################
############## TPC-H MariaDB ##############
###########################################


#### TCP-H Power Test - only MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB simple  sf=1"


#### TCP-H Monitoring - MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB monitoring  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpch-1
sleep 30


#### TCP-H Throughput Test - MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB throughput  sf=1  ne=1,2"


#### TPC-H RAM Disk Test - MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect metrics for the whole experiment
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rst ramdisk                  storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpch_mariadb_ramdisk.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB ramdisk  sf=10"


###########################################
############### TPC-DS MySQL ##############
###########################################


#### TCP-DS Power Test - only MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL simple  sf=1"


#### TCP-DS Monitoring - MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpcds-1
sleep 30


#### TCP-DS Throughput Test - MySQL (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mysql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL throughput  sf=10  ne=1,2"


###########################################
############ TPC-DS PostgreSQL ############
###########################################


#### TCP-DS Power Test - only PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
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
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL simple  sf=1"


#### TCP-DS Monitoring - PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL monitoring  sf=10"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpcds-1
sleep 30


#### TCP-DS Throughput Test - PostgreSQL (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 100Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_postgresql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL throughput  sf=10  ne=1,2"


###########################################
############## TPC-DS MariaDB #############
###########################################


#### TCP-DS Power Test - only MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MariaDB simple  sf=1"


#### TCP-DS Monitoring - MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MariaDB monitoring  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpcds-1
sleep 30


#### TCP-DS Throughput Test - MariaDB (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_mariadb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MariaDB throughput  sf=1  ne=1,2"


###########################################
############ TPC-DS MonetDB ###############
###########################################


#### TCP-DS Simple - MonetDB (TestCases.md)
# -dbms MonetDB                 DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 1                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB simple  sf=3"


#### TCP-DS Monitoring - MonetDB (TestCases.md)
# -dbms MonetDB                 DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 1                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB monitoring  sf=3"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-3
sleep 30


#### TCP-DS Throughput Test - MonetDB (TestCases.md)
# -dbms MonetDB                 DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 1                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 3 \
  -nlp 8 \
  -nlt 1 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB throughput  sf=3  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-100
sleep 30


#### TCP-DS Power Test Large - MonetDB (TestCases.md)
# -dbms MonetDB                 DBMS under test
# -sf 100                       scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 300Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 300Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power large  sf=100"


#### TCP-DS Throughput Test Large - MonetDB (TestCases.md)
# -dbms MonetDB                 DBMS under test
# -sf 100                       scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -nc 2                         number of repeated runs per configuration
# -ne 1,5                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 300Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MonetDB \
  -sf 100 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -nc 2 \
  -ne 1,5 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 300Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_tpcds_monetdb_5.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB throughput large  sf=100  ne=1,5"


###########################################
########### Benchbase PostgreSQL ##########
###########################################


#### Benchbase Simple (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30


#### Benchbase Persistency (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 1                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_postgresql_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL complex  sf=16  nc=2  ne=1,2"


###########################################
############# Benchbase MySQL #############
###########################################


#### Benchbase Simple (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-benchbase-16
sleep 30


#### Benchbase Persistency (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 1                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mysql_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL complex  sf=16  nc=2  ne=1,2"


###########################################
############ Benchbase MariaDB ############
###########################################


#### Benchbase Simple (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MariaDB simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-benchbase-16
sleep 30


#### Benchbase Persistency (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 1                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MariaDB persistency  sf=16  nc=2"


#### Benchbase Monitoring (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MariaDB monitoring  sf=16"


#### Benchbase Complex (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_benchbase_mariadb_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MariaDB complex  sf=16  nc=2  ne=1,2"


###########################################
########## HammerDB PostgreSQL ############
###########################################


#### HammerDB Simple (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB PostgreSQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


#### HammerDB Monitoring (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB PostgreSQL monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_postgresql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB PostgreSQL complex  sf=16  nc=2  ne=1,2"


###########################################
############# HammerDB MySQL ##############
###########################################


#### HammerDB Simple (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-hammerdb-16
sleep 30


#### HammerDB Monitoring (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mysql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL complex  sf=16  nc=2  ne=1,2"


###########################################
############ HammerDB MariaDB #############
###########################################


#### HammerDB Simple (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MariaDB simple  sf=16"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-hammerdb-16
sleep 30


#### HammerDB Monitoring (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MariaDB monitoring  sf=16"


#### HammerDB Complex (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 16Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_hammerdb_mariadb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MariaDB complex  sf=16  nc=2  ne=1,2"


###########################################
############ YCSB PostgreSQL ##############
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4,8                      number of loader pods
# -nlt 32,64                    total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 30


#### YCSB Loader Test for Persistency (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl e                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 8                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_postgresql_5.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL monitoring  sf=1"


###########################################
############### YCSB MySQL ################
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4,8                      number of loader pods
# -nlt 32,64                    total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mysql-ycsb-1
sleep 30


#### YCSB Loader Test for Persistency (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl e                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 8                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mysql_5.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL monitoring  sf=1"


###########################################
############## YCSB MariaDB ###############
###########################################


#### YCSB Loader Test for Scaling the Driver (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4,8                      number of loader pods
# -nlt 32,64                    total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MariaDB loader scaling  sf=1"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-mariadb-ycsb-1
sleep 30


#### YCSB Loader Test for Persistency (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MariaDB persistency  sf=1  nc=2"


#### YCSB Execution for Scaling and Repetition (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MariaDB scaling  sf=1  nc=2  ne=1,2"


#### YCSB Execution Different Workload (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl e                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 8                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_4.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MariaDB workload e  sf=1"


#### YCSB Execution Monitoring (TestCases.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/testcase_ycsb_mariadb_5.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MariaDB monitoring  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
