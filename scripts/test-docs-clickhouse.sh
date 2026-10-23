#!/bin/bash
# Generates documentation summaries for ClickHouse experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




################################################
################## ClickHouse ##################
################################################




#### TPC-H ClickHouse (Example-ClickHouse.md)
# -dbms ClickHouse              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration (2nd run: data survives the SUT restart)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container
# -rc 16                        CPU requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouse \
  -sf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouse  sf=1  nc=2"


#### TPC-H ClickHouseCluster (Example-ClickHouse.md)
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration (2nd run: data survives the SUT restart)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container and each worker
# -rc 16                        CPU requested for the SUT container and each worker
# -lr 64Gi                      RAM limit for the SUT container and each worker
# -rr 64Gi                      RAM requested for the SUT container and each worker
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claims
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouseCluster  sf=1  nw=3  nc=2"


#### TPC-DS ClickHouse (Example-ClickHouse.md)
# -dbms ClickHouse              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container
# -rc 16                        CPU requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma tpcds \
  -dbms ClickHouse \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS ClickHouse  sf=1"


#### TPC-DS ClickHouseCluster (Example-ClickHouse.md)
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container and each worker
# -rc 16                        CPU requested for the SUT container and each worker
# -lr 64Gi                      RAM limit for the SUT container and each worker
# -rr 64Gi                      RAM requested for the SUT container and each worker
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claims
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma tpcds \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_clickhouse_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS ClickHouseCluster  sf=1  nw=3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
