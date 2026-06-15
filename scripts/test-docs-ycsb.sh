#!/bin/bash
# Generates documentation summaries for YCSB experiments.
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
################## YCSB ###################
###########################################


#### YCSB Scale Loading (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 1,8                      number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 1,4                      loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 1,8 \
  -nlt 64 \
  -xnlf 1,4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 2 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_loading.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB loading  sf=1  nlp=1,8"


#### YCSB Scale Benchmarking (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2,3                      throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 2,3 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_benchmarking.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB benchmarking  sf=1  nbp=1,8"


#### YCSB Monitoring (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2,3                      throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_monitoring.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB monitoring  sf=3  nbp=1,8"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 30


#### YCSB Persistent Storage (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2,3                      throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 2,3 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_storage.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB storage  sf=1  nbp=1,8  nc=2"


#### YCSB Custom Loading Parameters (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 1                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 1                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 2                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 override deployment configuration parameter
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 1 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 2 \
  -ne 1 \
  -nc 1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 \
  run &>$LOG_DIR/doc_ycsb_testcase_loading_patch.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB loading patch  sf=1  nlp=1"


###########################################
############## All Workloads ##############
###########################################


#### YCSB Workload A (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload a \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_a.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload a  sf=10  nbp=1,8"


#### YCSB Workload B (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload b                  YCSB workload template (b = 95%% read / 5%% update)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload b \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_b.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload b  sf=10  nbp=1,8"


#### YCSB Workload C (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload c                  YCSB workload template (c = 100%% read)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload c \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_c.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload c  sf=10  nbp=1,8"


#### YCSB Workload D (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload d                  YCSB workload template (d = 95%% read / 5%% insert)
# -xio hashed                   key distribution for insert operations
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload d \
  -xio hashed \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_d.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload d  sf=10  nbp=1"


#### YCSB Workload E (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload e                  YCSB workload template (e = 95%% scan / 5%% insert)
# -xio ordered                  key distribution for insert operations
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload e \
  -xio ordered \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_e.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload e  sf=10  nbp=1"


#### YCSB Workload F (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# --workload f                  YCSB workload template (f = 50%% read / 50%% read-modify-write)
# -dbms PostgreSQL              DBMS under test
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  --workload f \
  -dbms PostgreSQL \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rr 64Gi -lr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_f.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB workload f  sf=10  nbp=1,8"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
