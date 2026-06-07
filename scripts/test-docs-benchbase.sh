#!/bin/bash
# Generates documentation summaries for Benchbase experiments.
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
############### Benchbase #################
###########################################


#### Benchbase Scale (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_scale.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase scale  sf=16  nbp=1,2"


#### Benchbase Monitoring (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_monitoring.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30


#### Benchbase Persistent Storage (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_storage.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160
sleep 30


#### Benchbase Keying and Thinking Time (Example-Benchbase.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 128Gi                     RAM requested for the SUT container
# -lr 128Gi                     RAM limit for the SUT container
# -sf 160                       scaling factor (controls database size)
# -sd 30                        benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -dbms PostgreSQL              DBMS under test
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1600                     threads per benchmarking pod
# -nbf 1                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -rr 128Gi -lr 128Gi \
  -sf 160 \
  -sd 30 \
  -xkey \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 100Gi \
  run &>$LOG_DIR/doc_benchbase_testcase_keytime.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase keytime  sf=160  nbp=1,2,5,10"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
