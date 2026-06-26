#!/bin/bash
# Generates documentation summaries for TiDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




#################################################
##################### TiDB ######################
#################################################


#### YCSB Ingestion (Example-TiDB.md)
# -dbms TiDB                    DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnsr 3                       number of storage replicas
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -xop 1                        number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 5Gi                      size of the persistent volume claim
bexhoma ycsb \
  -dbms TiDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -xop 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 5Gi \
  run &>$LOG_DIR/doc_ycsb_tidb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB TiDB  sf=1  nbp=1"


# -dbms TiDB                    DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -xnsr 3                       number of storage replicas
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 16Gi                     size of the persistent volume claim
bexhoma benchbase \
  -dbms TiDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -xnsr 3 \
  -nw 3 \
  -nwr 3 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 16Gi \
  run &>$LOG_DIR/doc_benchbase_tidb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase TiDB  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
