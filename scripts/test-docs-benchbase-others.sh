#!/bin/bash
# Generates documentation summaries for Benchbase experiments on additional DBMS.
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
################# Benchbase Others #################
####################################################


#### Benchbase Twitter Simple (Example-Benchbase-Others.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -b twitter                    Benchbase benchmark type
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_simple.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase twitter simple  sf=16  nbp=1"


#### Benchbase Twitter Scale (Example-Benchbase-Others.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 128Gi                     RAM requested for the SUT container
# -lr 128Gi                     RAM limit for the SUT container
# -sf 1600                      scaling factor (controls database size)
# -sd 20                        benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -b twitter                    Benchbase benchmark type
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -rr 128Gi -lr 128Gi \
  -sf 1600 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,4,8 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -b twitter \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_scale.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase twitter scale  sf=1600  nbp=1,2,4,8"


#### Benchbase CH-benCHmark Simple (Example-Benchbase-Others.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -b chbenchmark                Benchbase benchmark type
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 10 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_simple.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase chbenchmark simple  sf=10  nbp=1"


#### Benchbase CH-benCHmark Scale (Example-Benchbase-Others.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rr 128Gi                     RAM requested for the SUT container
# -lr 128Gi                     RAM limit for the SUT container
# -sf 100                       scaling factor (controls database size)
# -sd 20                        benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -b chbenchmark                Benchbase benchmark type
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -rr 128Gi -lr 128Gi \
  -sf 100 \
  -sd 20 \
  -dbms PostgreSQL \
  -nbp 1,2,5,10 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_scale.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase chbenchmark scale  sf=100  nbp=1,2,5,10"


#### Benchbase YCSB Workload C (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload c                  YCSB workload template (c = 100%% read)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload c \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_c.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload c  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload A (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload a \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_a.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload a  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload B (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload b                  YCSB workload template (b = 95%% read / 5%% update)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload b \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_b.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload b  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload D (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload d                  YCSB workload template (d = 95%% read / 5%% insert)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload d \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_d.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload d  sf=1000  nbp=1"


#### Benchbase YCSB Workload E (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload e                  YCSB workload template (e = 95%% scan / 5%% insert)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload e \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_e.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload e  sf=1000  nbp=1"


#### Benchbase YCSB Workload F (Example-Benchbase-Others.md)
# -tr                           verify result meets basic sanity requirements
# -sf 1000                      scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# --benchmark ycsb              Benchbase benchmark type
# --workload f                  YCSB workload template (f = 50%% read / 50%% read-modify-write)
# -dbms PostgreSQL              DBMS under test
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -tr \
  -sf 1000 \
  -sd 5 \
  --benchmark ycsb \
  --workload f \
  -dbms PostgreSQL \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_f.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload f  sf=1000  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
