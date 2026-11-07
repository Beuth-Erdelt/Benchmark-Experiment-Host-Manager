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




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H on ClickHouse, quick, without monitoring
# -dbms ClickHouse              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration (2nd run: data survives the SUT restart)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container
# -rc 16                        CPU requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouse \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouse  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H on ClickHouse at SF 10 with application metrics, at least 1 minute of benchmarking
# -dbms ClickHouse              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration (2nd run: data survives the SUT restart)
# -ne 1                         parallel client counts to sweep (comma-separated)
# -xqr 10                       repeat each query 10 times, so the benchmarking phase lasts long enough for monitoring
# -nlp 8                        number of data loader pods
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container
# -rc 16                        CPU requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouse \
  -sf 10 \
  -nc 1 \
  -ne 1 \
  -xqr 10 \
  -nlp 8 \
  -xdt \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouse monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H on ClickHouse, the second run finds the data on the volume
# -dbms ClickHouse              DBMS under test
# -sf 10                         scaling factor (controls database size in GB)
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
  -sf 10 \
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
  run &>$LOG_DIR/docs_tpch_clickhouse_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouse  sf=10  nc=2"


####################################################
#### Variants ######################################
####################################################


# Variant cluster: TPC-H on ClickHouseCluster with 3 shards
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 10                         scaling factor (controls database size in GB)
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
  -sf 10 \
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
  run &>$LOG_DIR/docs_tpch_clickhouse_cluster.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouseCluster  sf=10  nw=3  nc=2"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS on ClickHouse
# -dbms ClickHouse              DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
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
  -sf 3 \
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
  run &>$LOG_DIR/docs_tpcds_clickhouse.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS ClickHouse  sf=3"


# TPC-DS on ClickHouseCluster with 3 shards
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 3                         scaling factor (controls database size in GB)
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
  -sf 3 \
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
  run &>$LOG_DIR/docs_tpcds_clickhouse_cluster.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS ClickHouseCluster  sf=3  nw=3"


####################################################
#### Refresh Stream ################################
####################################################


#### TPC-H Refresh Stream (Example-ClickHouse.md)
# TPC-H with a refresh stream on ClickHouse: 3 query streams and one RF1/RF2 stream in parallel
# -dbms ClickHouse              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -ne 3                         parallel query streams
# -xrs 3                        refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container
# -rc 16                        CPU requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn/-rnl/-rnb $BEXHOMA_NODE_* schedule SUT, loader and benchmarker pods on these nodes
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouse \
  -sf 1 \
  -nlp 8 \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouse refresh  sf=1  ne=3"


#### TPC-H Refresh Stream on ClickHouseCluster (Example-ClickHouse.md)
# TPC-H with a refresh stream on ClickHouseCluster with 3 shards: RF1 inserts through the Distributed tables, RF2 deletes on the shards
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -ne 3                         parallel query streams
# -xrs 3                        refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lc 16                        CPU limit for the SUT container and each worker
# -rc 16                        CPU requested for the SUT container and each worker
# -lr 64Gi                      RAM limit for the SUT container and each worker
# -rr 64Gi                      RAM requested for the SUT container and each worker
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claims
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn/-rnl/-rnb $BEXHOMA_NODE_* schedule SUT, loader and benchmarker pods on these nodes
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
  -nlp 8 \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 16 \
  -rc 16 \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_tpch_clickhouse_cluster_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H ClickHouseCluster refresh  sf=1  nw=3  ne=3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
