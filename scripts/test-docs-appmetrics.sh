#!/bin/bash
# Generates documentation summaries for application metrics experiments.
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
########## PostgreSQL Application Metrics ##########
####################################################


#### Benchbase Application Metrics (Example-Benchbase.md)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -m -mc -ma -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL appmetrics  sf=16  nbp=1,2"


#### YCSB Application Metrics (Example-YCSB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 3                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms PostgreSQL              DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 2,3                      throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL appmetrics  sf=3  nbp=1,8"


#### TPC-H Application Metrics (Example-TPC-H.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_appmetrics.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL appmetrics  sf=3"


#### TPC-DS Application Metrics (Example-TPC-DS.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -dbms PostgreSQL              DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL appmetrics  sf=3"


#### HammerDB Application Metrics (Example-HammerDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -sd 5                         benchmark duration in minutes
# -dbms PostgreSQL              DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB PostgreSQL appmetrics  sf=16  nbp=1,2"


####################################################
############ MySQL Application Metrics #############
####################################################


#### Benchbase MySQL Application Metrics
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms MySQL                   DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -m -mc -ma -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms MySQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL appmetrics  sf=16  nbp=1,2"


#### YCSB MySQL Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -sf 3                         scaling factor (number of records x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms MySQL                   DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 2,3                      throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb -ms $BEXHOMA_MS -tr -lr 64Gi \
  -sf 3 \
  --workload a \
  -dbms MySQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL appmetrics  sf=3  nbp=1,8"


#### TPC-H MySQL Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -dbms MySQL                   DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch -ms $BEXHOMA_MS -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL appmetrics  sf=3"


#### TPC-DS MySQL Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -dt                           disable result type checking
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -dbms MySQL                   DBMS under test
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -sf 3                         scaling factor (controls database size in GB)
# -t 1200                       query timeout in seconds
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds -ms $BEXHOMA_MS -dt -tr -lr 64Gi \
  -rr 64Gi -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log

wait_process "tpcds"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL appmetrics  sf=3"


#### HammerDB MySQL Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -sf 16                        scaling factor (number of warehouses)
# -xlat                         collect per-operation latency histograms
# -sd 5                         benchmark duration in minutes
# -dbms MySQL                   DBMS under test
# -nlt 16                       threads per loader pod
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod (virtual users)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb -ms $BEXHOMA_MS -tr -lr 64Gi \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms MySQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log

wait_process "hammerdb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL appmetrics  sf=16  nbp=1,2"


####################################################
######### CockroachDB Application Metrics ##########
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms CockroachDB             DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  -sfo 10 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_cockroachdb_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB appmetrics  sf=10  nbp=1"


#### Benchbase CockroachDB Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -dbms CockroachDB             DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_cockroachdb_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB appmetrics  sf=16  nbp=1,2"


####################################################
############ Redis Application Metrics #############
####################################################


# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_redis_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis appmetrics  sf=1  nbp=1"


####################################################
############# TiDB Application Metrics #############
####################################################


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
# -ma                           collect application-level metrics
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
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_tidb_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB TiDB appmetrics  sf=1  nbp=1"


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
  run &>$LOG_DIR/doc_benchbase_run_tidb_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase TiDB appmetrics  sf=16  nbp=1,2"


####################################################
########### PGBouncer Application Metrics ##########
####################################################


# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (number of records x 1000)
# -sfo 16                       number of operations for the benchmark phase (x 1000)
# --workload c                  YCSB workload template (c = 100%% read)
# -dbms PGBouncer               DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 16                       number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 11                       loading throughput target as a multiple of the base ops/s
# -nbp 16                       benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 11                       throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -npp 4                        number of PGBouncer proxy pods
# -npi 128                      maximum incoming connections per PGBouncer instance
# -npo 64                       maximum outgoing connections per PGBouncer instance
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run &>$LOG_DIR/doc_ycsb_run_pgbouncer_appmetrics.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer appmetrics  sf=16  nbp=16"


#### Benchbase PGBouncer Application Metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 10                        benchmark duration in minutes
# -xconn                        use a new connection per transaction
# -dbms PGBouncer               DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 32                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -npp 2                        number of PGBouncer proxy pods
# -npi 32                       maximum incoming connections per PGBouncer instance
# -npo 32                       maximum outgoing connections per PGBouncer instance
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_pgbouncer_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PGBouncer appmetrics  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
