#!/bin/bash
# Generates documentation summaries for PGBouncer experiments.
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
################## YCSB PGBouncer ##################
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of records x 1000)
# -sfo 16                       number of operations for the benchmark phase (x 1000)
# --workload c                  YCSB workload template (c = 100%% read)
# -dbms PGBouncer               DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 16                       number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 11                       loading throughput target as a multiple of the base ops/s
# -nbp 16                       benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 11                       throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -npp 4                        number of PGBouncer proxy pods
# -npi 128                      maximum incoming connections per PGBouncer instance
# -npo 64                       maximum outgoing connections per PGBouncer instance
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run &>$LOG_DIR/test_ycsb_testcase_pgbouncer_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer  sf=16  nbp=16"


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of records x 1000)
# -sfo 16                       number of operations for the benchmark phase (x 1000)
# --workload c                  YCSB workload template (c = 100%% read)
# -dbms PGBouncer               DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 16                       number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 11                       loading throughput target as a multiple of the base ops/s
# -nbp 16                       benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 11                       throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -npp 4                        number of PGBouncer proxy pods
# -npi 128                      maximum incoming connections per PGBouncer instance
# -npo 64                       maximum outgoing connections per PGBouncer instance
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  -rst shared -rss 100Gi -rsr \
  run &>$LOG_DIR/test_ycsb_testcase_pgbouncer_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer storage  sf=16  nbp=16  nc=2"


####################################################
############### Benchbase PGBouncer ################
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 10                        benchmark duration in minutes
# -xconn                        use a new connection per transaction
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_newconn.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase new-connection PostgreSQL  sf=16  nbp=1,2"


#### Benchbase PGBouncer (Example-PGBouncer.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 10                        benchmark duration in minutes
# -xconn                        use a new connection per transaction
# -dbms PGBouncer               DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -npp 2                        number of PGBouncer proxy pods
# -npi 32                       maximum incoming connections per PGBouncer instance
# -npo 32                       maximum outgoing connections per PGBouncer instance
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_newconn_pool.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase new-connection PGBouncer  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
