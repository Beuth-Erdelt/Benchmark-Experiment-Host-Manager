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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xli 10                       log status to stdout every x seconds
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xnbf 16                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -ms $BEXHOMA_MS \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 16 \
  -xsd 5 \
  -xli 10 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 100Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 1/3  sf=16  nbp=1,2  nbf=16"

#### Benchbase Monitoring (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xli 10                       log status to stdout every x seconds
# -dbms PostgreSQL              DBMS under test
# -nbp 4,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xnbf 20                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -ms $BEXHOMA_MS \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 16 \
  -xsd 5 \
  -xli 10 \
  -dbms PostgreSQL \
  -nbp 4,8 \
  -nbt 160 \
  -xnbf 20 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 100Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_2.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 2/3  sf=16  nbp=4,8  nbf=20"

#### Benchbase Monitoring (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xli 10                       log status to stdout every x seconds
# -dbms PostgreSQL              DBMS under test
# -nbp 4,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -xnbf 20                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -ms $BEXHOMA_MS \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 16 \
  -xsd 5 \
  -xli 10 \
  -dbms PostgreSQL \
  -nbp 4,8 \
  -nbt 160 \
  -xnbf 20 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_3.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase collector 3/3  sf=16  nbp=4,8  nbf=20"




###########################################
########### TPC-C Benchbase MT ############
###########################################


BEXHOMA_NUM_TENANTS=2

# ---------------- SCHEMA ----------------
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb schema                   tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 1                         scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 20Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb schema \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -xsd 5 \
  -xkey \
  --dbms PostgreSQL \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_schema.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- DATABASE ----------------
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 1                         scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 20Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb database \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -xsd 5 \
  -xkey \
  --dbms PostgreSQL \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_database.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# ---------------- CONTAINER ----------------
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 1                         scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne "1,1"                     parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb container \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -xsd 5 \
  -xkey \
  --dbms PostgreSQL \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -ne "1,1" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 10Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_container.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




###########################################
################## TPC-H ##################
###########################################


# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_1.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 1/3  sf=3"

# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 6                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 6 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_2.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 2/3  sf=6"



# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 6                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp 8                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 6 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_3.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H collector 3/3  sf=6"




###########################################
################ TPC-H MT #################
###########################################

BEXHOMA_NUM_TENANTS=2

# ---------------- SCHEMA ----------------
# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb schema                   tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb schema \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_schema.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- DATABASE ----------------
# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb database \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_database.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=3"

# ---------------- CONTAINER ----------------
# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -xii                           create indexes after data load
# -xic                           enforce constraints after data load
# -xis                           run ANALYZE after data load
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ne "1,1"                     parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma tpch \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb container \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -xii \
  -xic \
  -xis \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -ne "1,1" \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_tpch_testcase_collector_tenants_container.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=3"


###########################################
################## YCSB ###################
###########################################


#### YCSB Monitoring (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 100000)
# -xop 1                        scaling factor for operations (number of operations x 100000)
# --workload a                  YCSB workload template (a = 50% read / 50% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2                        benchmarking throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 3 \
  -xop 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 2 \
  -ne 1 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 1/3  nbp=1,8  nbf=2"


#### YCSB Monitoring (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 100000)
# -xop 1                        scaling factor for operations (number of operations x 100000)
# --workload a                  YCSB workload template (a = 50% read / 50% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 3                        benchmarking throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 3 \
  -xop 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 3 \
  -ne 1 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 2/3  nbp=1,8  nbf=3"

#### YCSB Monitoring (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 100000)
# -xop 1                        scaling factor for operations (number of operations x 100000)
# --workload a                  YCSB workload template (a = 50% read / 50% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 3                        benchmarking throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 3 \
  -xop 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 3 \
  -ne 1 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_testcase_collector_3.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB collector 3/3  nbp=1,8  nbf=3"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -xsd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma hammerdb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 16 \
  -xlat \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_1.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 1/3  sf=16  nbp=1,2  nbt=16"

#### HammerDB Monitoring (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -xsd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod (virtual users)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma hammerdb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 16 \
  -xlat \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_2.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 2/3  sf=16  nbp=1,2  nbt=32"

#### HammerDB Monitoring (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -xsd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod (virtual users)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma hammerdb \
  -ms $BEXHOMA_MS \
  -tr \
  -sf 16 \
  -xlat \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -nc 2 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_hammerdb_testcase_collector_3.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB collector 3/3  sf=16  nbp=1,2  nbt=32"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
