#!/bin/bash
# Generates documentation summaries for collector experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh

BEXHOMA_NODE_SUT="cl-worker38"




###########################################
############# TPC-C Benchbase #############
###########################################




#### Benchbase Monitoring (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xli 10                       log status to stdout every x seconds
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 100Gi                    size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1,2 \
  -nbt 160 \
  -xli 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 1/3  sf=16  nbp=1,2  nbf=16"

#### Benchbase Monitoring (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 20                      throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 4,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xli 10                       log status to stdout every x seconds
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 100Gi                    size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 20 \
  -nc 2 \
  -nbp 4,8 \
  -nbt 160 \
  -xli 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 2/3  sf=16  nbp=4,8  nbf=20"

#### Benchbase Monitoring (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 20                      throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 4,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xli 10                       log status to stdout every x seconds
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 20 \
  -nc 2 \
  -nbp 4,8 \
  -nbt 160 \
  -xli 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 3/3  sf=16  nbp=4,8  nbf=20"




###########################################
########### TPC-C Benchbase MT ############
###########################################


BEXHOMA_NUM_TENANTS=2

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 20Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb schema                   tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -m \
  -ma \
  -mc \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_schema.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 20Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb database                 tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -m \
  -ma \
  -mc \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_database.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -ne "1,1"                     parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 10Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb container                tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -nc 2 \
  -ne "1,1" \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -m \
  -ma \
  -mc \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 10Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_container.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




###########################################
################## TPC-H ##################
###########################################


# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 30Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nbp 1 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 1/3  sf=3"

# -dbms PostgreSQL              DBMS under test
# -sf 6                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 30Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 6 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nbp 1 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 2/3  sf=6"



# -dbms PostgreSQL              DBMS under test
# -sf 6                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 6 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nbp 1 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 3/3  sf=6"




###########################################
################ TPC-H MT #################
###########################################

BEXHOMA_NUM_TENANTS=2

# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 30Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb schema                   tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_schema.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 30Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb database                 tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nc 2 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_database.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne "1,1"                     parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 15Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -mtb container                tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 3 \
  -nc 2 \
  -ne "1,1" \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 15Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_container.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=3"


###########################################
################## YCSB ###################
###########################################


#### YCSB Monitoring (Example-YCSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (number of records x 100000)
# -xwl a                        YCSB workload template (a = 50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        scaling factor for operations (number of operations x 100000)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 15Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 15Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 1/3  nbp=1,8  nbf=2"


#### YCSB Monitoring (Example-YCSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (number of records x 100000)
# -xwl a                        YCSB workload template (a = 50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 3                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        scaling factor for operations (number of operations x 100000)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 15Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 3 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 15Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 2/3  nbp=1,8  nbf=3"

#### YCSB Monitoring (Example-YCSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (number of records x 100000)
# -xwl a                        YCSB workload template (a = 50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 3                       benchmarking throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 1                        scaling factor for operations (number of operations x 100000)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 3 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -xop 1 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 3/3  nbp=1,8  nbf=3"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -xlat                         collect per-operation latency histograms
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 15Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -nc 2 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 15Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 1/3  sf=16  nbp=1,2  nbt=16"

#### HammerDB Monitoring (Example-HammerDB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod (virtual users)
# -xlat                         collect per-operation latency histograms
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 15Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -nc 2 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 15Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 2/3  sf=16  nbp=1,2  nbt=32"

#### HammerDB Monitoring (Example-HammerDB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod (virtual users)
# -xlat                         collect per-operation latency histograms
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -nc 2 \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xlat \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 3/3  sf=16  nbp=1,2  nbt=32"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
