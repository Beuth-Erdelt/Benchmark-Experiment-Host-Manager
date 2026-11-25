#!/bin/bash
# Generates test logs for MariaDB ColumnStore, one run per workload that works on it.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and
# extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H on MariaDB ColumnStore, quick, without monitoring
# -dbms MariaDBCS               DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         two runs, the second restarts the SUT on the same data
# -ks no                        remove the SUT at the end
# -nlp 8                        number of data loader pods (MariaDBCS always uses 1)
# -xis                          run ANALYZE after data load
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 16Gi                      RAM limit for the SUT container
# -rr 16Gi                      RAM requested for the SUT container
bexhoma tpch \
  -dbms MariaDBCS \
  -sf 1 \
  -nc 1 \
  -ks no \
  -nlp 8 \
  -xis \
  -ms $BEXHOMA_MS \
  -lr 16Gi \
  -rr 16Gi \
  run &>$LOG_DIR/docs_tpch_mariadbcs.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDBCS  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H on MariaDB ColumnStore at SF 10, at least 1 minute of benchmarking
# -dbms MariaDBCS               DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nc 1                         two runs, the second restarts the SUT on the same data
# -ks no                        remove the SUT at the end
# -nlp 8                        number of data loader pods (MariaDBCS always uses 1)
# -xis                          run ANALYZE after data load
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
bexhoma tpch \
  -dbms MariaDBCS \
  -sf 10 \
  -nc 1 \
  -ks no \
  -nlp 8 \
  -xis \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  -rr 64Gi \
  run &>$LOG_DIR/docs_tpch_mariadbcs_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDBCS monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H next to MariaDB, the result sets of both are stored per connection
# -dbms MariaDB MariaDBCS       DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         two runs, the second restarts the SUT on the same data
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
# -nlp 8                        number of data loader pods (MariaDBCS always uses 1)
# -xii                          create indexes after data load (MariaDB: Q20 times out without)
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          store the result sets of the queries
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 16Gi                      RAM limit for the SUT container
# -rr 16Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 20Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
bexhoma tpch \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -nc 2 \
  -ar \
  -ks no \
  -nlp 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 20Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpch_mariadbcs_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB MariaDBCS  sf=1"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS next to MariaDB; the test SQL warnings fails on Q39, which has columns of the same name
# -dbms MariaDB MariaDBCS
# -sf 1
# -nc 2
# -ar
# -ks no
# -xii
# -xic
# -xis
# -xdt
# -m
# -ms $BEXHOMA_MS
# -lr 32Gi
# -rr 32Gi
# -rsr
# -rss 30Gi
# -rst $BEXHOMA_STORAGE_CLASS
bexhoma tpcds \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -nc 2 \
  -ar \
  -ks no \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -lr 32Gi \
  -rr 32Gi \
  -rsr \
  -rss 30Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_tpcds_mariadbcs.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MariaDBCS  sf=1"


####################################################
#### SSB ###########################################
####################################################


# SSB star schema
# -dbms MariaDBCS
# -sf 1
# -nc 2
# -ar
# -ks no
# -xis
# -m
# -ms $BEXHOMA_MS
# -lr 16Gi
# -rr 16Gi
# -rsr
# -rss 20Gi
# -rst $BEXHOMA_STORAGE_CLASS
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -nc 2 \
  -ar \
  -ks no \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 20Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_ssb_mariadbcs.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MariaDBCS  sf=1"


# SSB flat schema
# -dbms MariaDBCS
# -sf 1
# -xsv flat                     one denormalized table lineorder_flat
# -nc 2
# -ar
# -ks no
# -xis
# -m
# -ms $BEXHOMA_MS
# -lr 16Gi
# -rr 16Gi
# -rsr
# -rss 20Gi
# -rst $BEXHOMA_STORAGE_CLASS
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -xsv flat \
  -nc 2 \
  -ar \
  -ks no \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 20Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  run &>$LOG_DIR/docs_ssb_mariadbcs_flat.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MariaDBCS flat  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MariaDBCS: 3 query streams and one RF1/RF2 stream in parallel
# -dbms MariaDBCS               DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne 3                         parallel query streams
# -xrs 3                        refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT
# -rnl $BEXHOMA_NODE_LOAD
# -rnb $BEXHOMA_NODE_BENCHMARK
bexhoma tpch \
  -dbms MariaDBCS \
  -sf 1 \
  -ne 3 \
  -xrs 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadbcs_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDBCS refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
