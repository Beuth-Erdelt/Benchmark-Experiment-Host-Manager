#!/bin/bash
# Generates test logs for CedarDB, one run per workload that works on it.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs to logs_tests/local (not in the repository), and
# extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh

LOG_DIR="./logs_tests/local"
prepare_logs


#### TPC-H Monitoring (Example-TPC-H.md)
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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms CedarDB \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii \
  -xic \
  -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_tpch_testcase_cedardb_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H CedarDB monitoring  sf=3"


#### SSB normal schema
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms CedarDB \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_ssb_testcase_cedardb_normal.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB CedarDB normal  sf=1"


#### SSB flat schema
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xsv flat                     one denormalized table lineorder_flat
# -xii                          create indexes after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms CedarDB \
  -sf 1 \
  -xsv flat \
  -xii \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_ssb_testcase_cedardb_flat.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB CedarDB flat  sf=1"


#### YCSB workload c
# Read-only: the run to judge YCSB by, no write conflicts.
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl c                        YCSB workload template (100% read)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ycsb \
  -dbms CedarDB \
  -sf 1 \
  -xwl c \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_ycsb_testcase_cedardb_read.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CedarDB workload c  sf=1"


#### YCSB workload a
# Known: about 0.4% of the updates fail with "conflict with concurrent transaction",
# YCSB does not retry them, so the test "contains FAILED column" fails.
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ycsb \
  -dbms CedarDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_ycsb_testcase_cedardb_update.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CedarDB workload a  sf=1"


#### YCSB Scale Loading (Example-YCSB.md)
# No -rst: every configuration loads, a volume would be reused.
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl c                        YCSB workload template (100% read)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1,4                     loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 1,8                      number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ycsb \
  -dbms CedarDB \
  -sf 1 \
  -xwl c \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1,4 \
  -nc 1 \
  -ne 1 \
  -nlp 1,8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/doc_ycsb_testcase_cedardb_loading.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CedarDB loading  sf=1  nlp=1,8"


#### Benchbase tpcc
# Target above what the DBMS reaches, so the throughput is not capped.
# READ_COMMITTED runs as repeatable read on CedarDB.
# -dbms CedarDB                 DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xbt tpcc                     Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma benchbase \
  -dbms CedarDB \
  -sf 16 \
  -xbt tpcc \
  -xsd 5 \
  -xtb 16384 \
  -xnbf 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_benchbase_testcase_tpcc_cedardb_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CedarDB tpcc  sf=16"


#### Benchbase ycsb
# -dbms CedarDB                 DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xbt ycsb                     Benchbase benchmark type
# -xwl a                        YCSB workload letter
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma benchbase \
  -dbms CedarDB \
  -sf 1 \
  -xbt ycsb \
  -xwl a \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 100 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_benchbase_testcase_ycsb_cedardb_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CedarDB ycsb  sf=1"


#### Benchbase chbenchmark
# Known: runs, but num_errors is not 0 and no test reports it: Q22 always fails (GROUP BY and
# ORDER BY spell substring() differently), Q15 fails when terminals overlap (same view).
# -dbms CedarDB                 DBMS under test
# -sf 10                        scaling factor (controls database size)
# -xbt chbenchmark              Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 100                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma benchbase \
  -dbms CedarDB \
  -sf 10 \
  -xbt chbenchmark \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1 \
  -nbt 100 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rsr \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_cedardb_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CedarDB chbenchmark  sf=10"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
