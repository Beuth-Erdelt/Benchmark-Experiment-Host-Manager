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
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
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
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase scale  sf=16  nbp=1,2"


#### Benchbase Monitoring (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
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
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30


#### Benchbase Persistent Storage (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 30Gi                     size of the persistent volume claim
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
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160
sleep 30


#### Benchbase Keying and Thinking Time (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 160                       scaling factor (controls database size)
# -xsd 30                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1600                     threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 100Gi                    size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 160 \
  -xsd 30 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -xkey \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_keytime.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase keytime  sf=160  nbp=1,2,5,10"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
