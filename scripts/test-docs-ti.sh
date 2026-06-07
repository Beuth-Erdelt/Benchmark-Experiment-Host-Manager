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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 1                        number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -nsr 3                        number of storage replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms TiDB                    DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 1                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 1                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  --workload a \
  -dbms TiDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_tidb_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB TiDB  sf=1  nbp=1"


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -nsr 3                        number of storage replicas
# -dbms TiDB                    DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  -dbms TiDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_tidb_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase TiDB  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
