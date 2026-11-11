#!/bin/bash
# Generates test logs for SQL Server 2022 Developer edition (#834), one run per workload.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs to logs_tests/local (not in the repository), and
# extracts summaries into separate files.
#
# The license forbids publishing benchmark results without Microsoft's prior
# written approval: the logs stay in logs_tests/local (git-ignored, check with
# git check-ignore logs_tests/local/x.log), no docs page shows or links them,
# and nothing of them is committed, quoted in issues or PRs, or shown elsewhere.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh

# after sourcing: testfunctions.sh sets ./logs_tests
LOG_DIR="./logs_tests/local"
prepare_logs


#### TPC-H with all post-load steps, persistent storage, reset
# -dbms SQLServer               DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         two runs, the second restarts the SUT on the same data
# -nlp 8                        number of data loader pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run UPDATE STATISTICS after data load
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms SQLServer \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -xii -xic -xis \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_tpch_sqlserver_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H SQLServer storage  sf=1"


#### TPC-H refresh stream
# -dbms SQLServer               DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne 3                         parallel query streams
# -nlp 8                        number of data loader pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run UPDATE STATISTICS after data load
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -xrs 3                        refresh stream: 3 RF1+RF2 pairs per round, parallel to the query streams
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms SQLServer \
  -sf 1 \
  -ne 3 \
  -nlp 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xrs 3 \
  -ks no \
  run &>$LOG_DIR/docs_tpch_sqlserver_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H SQLServer refresh  sf=1  ne=3"


#### YCSB workload a, persistent storage, reset
# -dbms SQLServer               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2                       throughput target as a multiple of the base ops/s
# -xnlf 1                       loading throughput target as a multiple of the base ops/s
# -nc 2                         two runs, the second restarts the SUT on the same data
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma ycsb \
  -dbms SQLServer \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ycsb_sqlserver_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB SQLServer workload a  sf=1"


#### Benchbase tpcc (the only Benchbase benchmark with a SQL Server config)
# -dbms SQLServer               DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xbt tpcc                     Benchbase benchmark type
# -xsd 5                        benchmark duration in minutes
# -xtb 16384                    base ops/s used to compute the throughput target
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nc 2                         two runs, the second restarts the SUT on the same data
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma benchbase \
  -dbms SQLServer \
  -sf 16 \
  -xbt tpcc \
  -xsd 5 \
  -xtb 16384 \
  -xnbf 1 \
  -nc 2 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_benchbase_tpcc_sqlserver_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase SQLServer tpcc  sf=16"


#### HammerDB TPC-C
# -dbms SQLServer               DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma hammerdb \
  -dbms SQLServer \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_hammerdb_sqlserver.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB SQLServer  sf=16"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
