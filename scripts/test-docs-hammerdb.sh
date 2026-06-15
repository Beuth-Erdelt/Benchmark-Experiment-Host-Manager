#!/bin/bash
# Generates documentation summaries for HammerDB experiments.
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
################ HammerDB #################
###########################################


#### HammerDB Scale (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_scale.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB scale  sf=16  nbp=1,2"


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
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xlat \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_monitoring.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


#### HammerDB Persistent Storage (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -xsd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 8                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xlat \
  -xsd 5 \
  -dbms PostgreSQL \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_storage.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


#### HammerDB Keying and Thinking Time (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xsd 20                        benchmark duration in minutes
# -xlat                         collect per-operation latency histograms
# -xkey                         simulate user think time and keying delays
# -dbms PostgreSQL              DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -nlt 8                        threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod (virtual users)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 30Gi                     size of the persistent volume claim
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xsd 20 \
  -xlat \
  -xkey \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 160 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run &>$LOG_DIR/doc_hammerdb_testcase_keytime.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB keytime  sf=16  nbp=1,2  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
