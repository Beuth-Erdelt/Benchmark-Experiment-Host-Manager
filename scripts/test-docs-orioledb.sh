#!/bin/bash
# Generates documentation summaries for OrioleDB experiments (Example-OrioleDB.md).
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# OrioleDB is PostgreSQL 18 with the storage engine orioledb; it uses the
# scripts of PostgreSQL. Only OLTP workloads are run (YCSB, Benchbase, HammerDB).
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




####################################################
#### Main Example ##################################
####################################################


# Main example: YCSB workload A on OrioleDB, quick, without monitoring
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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
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
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb.log

report_result $? "YCSB OrioleDB  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: YCSB workload A for about 5 minutes, with application metrics
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
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_monitoring.log

report_result $? "YCSB OrioleDB monitoring  sf=1"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: two runs, the second restarts the SUT on the loaded volume
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
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
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
  -nc 2 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -ms $BEXHOMA_MS \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_storage.log

report_result $? "YCSB OrioleDB storage  sf=1"


####################################################
#### Comparison with PostgreSQL ####################
####################################################


# Comparison: YCSB workload A on PostgreSQL and OrioleDB, one after the other on the same node
# -dbms PostgreSQL OrioleDB     DBMS under test: heap tables and OrioleDB tables
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 8                       throughput target as a multiple of the base ops/s (above what both reach)
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4                        number of data loader pods
# -nlt 16                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ms 1                         one DBMS at a time, so they do not share the node
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL OrioleDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 8 \
  -xnlf 1 \
  -ne 1 \
  -nlp 4 \
  -nlt 16 \
  -nbp 1 \
  -nbt 32 \
  -xop 10 \
  -m \
  -ms 1 \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_orioledb_postgresql.log

report_result $? "YCSB PostgreSQL vs OrioleDB  sf=1"


####################################################
#### Benchbase #####################################
####################################################


# Benchbase TPC-C
# -dbms OrioleDB                DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xbt tpcc                     Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms OrioleDB \
  -sf 16 \
  -xbt tpcc \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_tpcc_orioledb.log

report_result $? "Benchbase OrioleDB tpcc  sf=16"


####################################################
#### HammerDB ######################################
####################################################


# HammerDB TPC-C
# -dbms OrioleDB                DBMS under test
# -sf 16                        scaling factor (number of warehouses)
# -xsd 5                        benchmark duration in minutes
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms OrioleDB \
  -sf 16 \
  -xsd 5 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_orioledb.log

report_result $? "HammerDB OrioleDB  sf=16"


###########################################
############## Clean Folder ###############
###########################################


report_total
clean_logs
