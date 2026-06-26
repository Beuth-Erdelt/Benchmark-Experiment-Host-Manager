#!/bin/bash
# Generates documentation summaries for CedarDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




#### TCP-H Monitoring (Example-TPC-H.md)
# -dbms CedarDB                 DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms 5                         max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 30Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms CedarDB \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms 5 \
  -tr \
  -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_cedardb_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H CedarDB monitoring  sf=3"


#### YCSB Scale Loading (Example-YCSB.md)
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1,4                     loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 1,8                      number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ms 5                         max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 5Gi                      size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms CedarDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1,4 \
  -nc 1 \
  -ne 1 \
  -nlp 1,8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms 5 \
  -tr \
  -rss 5Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_cedardb_loading.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CedarDB loading  sf=1  nlp=1,8"


#### Benchbase CH-benCHmark (Example-Benchbase-Others.md)
# -dbms CedarDB                 DBMS under test
# -sf 10                        scaling factor (controls database size)
# -xbt chbenchmark              Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -ms 2                         max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 10Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms CedarDB \
  -sf 10 \
  -xbt chbenchmark \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 100 \
  -ms 2 \
  -tr \
  -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_cedardb_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CedarDB chbenchmark simple  sf=10  nbp=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
