#!/bin/bash
# Generates test logs for OrioleDB (#821), one run per OLTP workload.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs to logs_tests/local (not in the repository), and
# extracts summaries into separate files.
#
# The results of OrioleDB are not part of the repository: the logs stay in
# logs_tests/local (git-ignored, check with git check-ignore
# logs_tests/local/x.log), and no docs page shows or links them.
#
# OrioleDB is PostgreSQL 18 with the storage engine orioledb; it uses the
# scripts of PostgreSQL. TPC-H, TPC-DS and SSB are not run (OLTP only).
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh

# after sourcing: testfunctions.sh sets ./logs_tests
LOG_DIR="./logs_tests/local"
prepare_logs


#### YCSB workload a, persistent storage, reset
# -dbms OrioleDB                DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -nc 2                         two runs, the second restarts the SUT on the same data
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4                        number of data loader pods
# -nlt 16                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ycsb \
  -dbms OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ycsb_orioledb_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB OrioleDB workload a  sf=1"


#### YCSB workload a, monitoring and application metrics
# -dbms OrioleDB                DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4                        number of data loader pods
# -nlt 16                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics (postgres-exporter)
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB OrioleDB appmetrics  sf=1"


#### Benchbase tpcc, persistent storage, reset
# -dbms OrioleDB                DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xbt tpcc                     Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nc 2                         two runs, the second restarts the SUT on the same data
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma benchbase \
  -dbms OrioleDB \
  -sf 16 \
  -xbt tpcc \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_benchbase_tpcc_orioledb_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase OrioleDB tpcc  sf=16"


#### HammerDB TPC-C
# -dbms OrioleDB                DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                        benchmark duration in minutes
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma hammerdb \
  -dbms OrioleDB \
  -sf 16 \
  -xsd 5 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_hammerdb_orioledb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB OrioleDB  sf=16"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
