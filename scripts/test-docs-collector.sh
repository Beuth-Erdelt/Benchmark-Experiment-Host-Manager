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


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

# Config nodes and paths
BEXHOMA_NODE_SUT="cl-worker38"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

# Check for file
if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

# Check for directories
for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."


if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"




###########################################
############# TPC-C Benchbase #############
###########################################




#### Benchbase Monitoring (Example-Benchbase.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -nc 2                         number of repeated runs per configuration
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
nohup python benchbase.py \
  -ms 1 \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 100Gi \
  -rsr \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_1.log &

wait_process "benchbase"

#### Benchbase Monitoring (Example-Benchbase.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 4,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 20                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -nc 2                         number of repeated runs per configuration
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
nohup python benchbase.py \
  -ms 1 \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 4,8 \
  -nbt 160 \
  -nbf 20 \
  -tb 1024 \
  -m -mc -ma \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 100Gi \
  -rsr \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_2.log &

wait_process "benchbase"




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
# -sd 5                         benchmark duration in minutes
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb schema \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -sd 5 \
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
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_schema.log &

wait_process "benchbase"

# ---------------- DATABASE ----------------
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb database \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -sd 5 \
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
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_database.log &

wait_process "benchbase"

# ---------------- CONTAINER ----------------
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
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
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb container \
  -rr 64Gi \
  -lr 64Gi \
  -sf 1 \
  -sd 5 \
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
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_container.log &

wait_process "benchbase"




###########################################
################## TPC-H ##################
###########################################


# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
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
nohup python tpch.py \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii \
  -ic \
  -is \
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
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_1.log &

wait_process "tpch"

# -tr                           verify result meets basic sanity requirements
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 6                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
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
nohup python tpch.py \
  -tr \
  -rr 64Gi \
  -lr 64Gi \
  -sf 6 \
  --dbms PostgreSQL \
  -ii \
  -ic \
  -is \
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
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_2.log &

wait_process "tpch"




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
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
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
nohup python tpch.py \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb schema \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii \
  -ic \
  -is \
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
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_schema.log &

wait_process "tpch"

# ---------------- DATABASE ----------------
# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
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
nohup python tpch.py \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb database \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii \
  -ic \
  -is \
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
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_database.log &

wait_process "tpch"

# ---------------- CONTAINER ----------------
# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
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
nohup python tpch.py \
  -tr \
  -mtn $BEXHOMA_NUM_TENANTS \
  -mtb container \
  -rr 64Gi \
  -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii \
  -ic \
  -is \
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
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_container.log &

wait_process "tpch"


###########################################
################## YCSB ###################
###########################################


#### YCSB Monitoring (Example-YCSB.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50% read / 50% update)
# -dbms PostgreSQL              DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 2                        benchmarking throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
nohup python ycsb.py \
  -ms 1 \
  -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_collector_1.log &

wait_process "ycsb"


#### YCSB Monitoring (Example-YCSB.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50% read / 50% update)
# -dbms PostgreSQL              DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 3                        benchmarking throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 15Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
nohup python ycsb.py \
  -ms 1 \
  -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 3 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared \
  -rss 15Gi \
  -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_collector_2.log &

wait_process "ycsb"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
nohup python hammerdb.py \
  -ms 1 \
  -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_collector_1.log &

wait_process "hammerdb"

#### HammerDB Monitoring (Example-HammerDB.md)
# -ms 1                         limit to 1 parallel DBMS configuration at a time
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod (virtual users)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
nohup python hammerdb.py \
  -ms 1 \
  -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_collector_2.log &

wait_process "hammerdb"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
