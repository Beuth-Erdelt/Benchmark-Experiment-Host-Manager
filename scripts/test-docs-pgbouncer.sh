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


# -dbms PGBouncer               DBMS under test
# -sf 16                        scaling factor (number of records x 1000)
# -xwl c                        YCSB workload template (c = 100%% read)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 11                      throughput target as a multiple of the base ops/s
# -xnlf 11                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 16                       number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 16                       benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xnpp 4                       number of PGBouncer proxy pods
# -xnpi 128                     maximum incoming connections per PGBouncer instance
# -xnpo 64                      maximum outgoing connections per PGBouncer instance
# -xop 16                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 16 \
  -xwl c \
  -xtb 16384 \
  -xnbf 11 \
  -xnlf 11 \
  -nc 1 \
  -ne 1 \
  -nlp 16 \
  -nlt 64 \
  -nbp 16 \
  -nbt 128 \
  -xnpp 4 \
  -xnpi 128 \
  -xnpo 64 \
  -xop 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_pgbouncer_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer  sf=16  nbp=16"


# -dbms PGBouncer               DBMS under test
# -sf 16                        scaling factor (number of records x 1000)
# -xwl c                        YCSB workload template (c = 100%% read)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 11                      throughput target as a multiple of the base ops/s
# -xnlf 11                      loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 16                       number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 16                       benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xnpp 4                       number of PGBouncer proxy pods
# -xnpi 128                     maximum incoming connections per PGBouncer instance
# -xnpo 64                      maximum outgoing connections per PGBouncer instance
# -xop 16                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 100Gi                    size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PGBouncer \
  -sf 16 \
  -xwl c \
  -xtb 16384 \
  -xnbf 11 \
  -xnlf 11 \
  -nc 2 \
  -ne 1 \
  -nlp 16 \
  -nlt 64 \
  -nbp 16 \
  -nbt 128 \
  -xnpp 4 \
  -xnpi 128 \
  -xnpo 64 \
  -xop 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 100Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_ycsb_testcase_pgbouncer_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer storage  sf=16  nbp=16  nc=2"


####################################################
############### Benchbase PGBouncer ################
####################################################


# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 10                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -xconn                        use a new connection per transaction
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xconn \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_newconn.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase new-connection PostgreSQL  sf=16  nbp=1,2"


#### Benchbase PGBouncer (Example-PGBouncer.md)
# -dbms PGBouncer               DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 10                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -xnpp 2                       number of PGBouncer proxy pods
# -xnpi 32                      maximum incoming connections per PGBouncer instance
# -xnpo 32                      maximum outgoing connections per PGBouncer instance
# -xconn                        use a new connection per transaction
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PGBouncer \
  -sf 16 \
  -xsd 10 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 32 \
  -xnpp 2 \
  -xnpi 32 \
  -xnpo 32 \
  -xconn \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_newconn_pool.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase new-connection PGBouncer  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
