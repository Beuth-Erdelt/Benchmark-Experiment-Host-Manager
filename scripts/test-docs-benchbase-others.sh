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
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xbt twitter                  Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xbt twitter \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase twitter simple  sf=16  nbp=1"


#### Benchbase Twitter Scale (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1600                      scaling factor (controls database size)
# -xbt twitter                  Benchbase benchmark type
# -xsd 20                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1600 \
  -xbt twitter \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,4,8 \
  -nbt 160 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_twitter_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase twitter scale  sf=1600  nbp=1,2,4,8"


#### Benchbase CH-benCHmark Simple (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size)
# -xbt chbenchmark              Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 10 \
  -xbt chbenchmark \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 100 \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase chbenchmark simple  sf=10  nbp=1"


#### Benchbase CH-benCHmark Scale (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 100                       scaling factor (controls database size)
# -xbt chbenchmark              Benchbase benchmark type
# -xsd 20                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 100 \
  -xbt chbenchmark \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,5,10 \
  -nbt 100 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase chbenchmark scale  sf=100  nbp=1,2,5,10"


#### Benchbase YCSB Workload C (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl c                        YCSB workload template (c = 100%% read)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl c \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_c.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload c  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload A (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl a \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_a.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload a  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload B (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl b                        YCSB workload template (b = 95%% read / 5%% update)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl b \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_b.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload b  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload D (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl d                        YCSB workload template (d = 95%% read / 5%% insert)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl d \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_d.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload d  sf=1000  nbp=1"


#### Benchbase YCSB Workload E (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl e                        YCSB workload template (e = 95%% scan / 5%% insert)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl e \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_e.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload e  sf=1000  nbp=1"


#### Benchbase YCSB Workload F (Example-Benchbase-Others.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1000                      scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl f                        YCSB workload template (f = 50%% read / 50%% read-modify-write)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nlt 64                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1000 \
  -xbt ycsb \
  -xwl f \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nlt 64 \
  -nbp 1,2 \
  -nbt 32 \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_f.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YCSB workload f  sf=1000  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
