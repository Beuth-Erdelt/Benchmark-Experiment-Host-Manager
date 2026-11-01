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


#### TPC-H next to MariaDB, the result sets of both are stored per connection
# -dbms MariaDB MariaDBCS       DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods (MariaDBCS always uses 1)
# -xii                          create indexes after data load (MariaDB: Q20 times out without)
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          store the result sets of the queries
# -m                           collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 16Gi                      RAM limit for the SUT container
# -rr 16Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class of the persistent volume
# -rss 20Gi                     size of the persistent volume claim
# -rsr                          delete any existing PVC for the SUT before starting
# -nc 2                         two runs, the second restarts the SUT on the same data
# -ar                           run the reset scripts before each round
# -ks no                        remove the SUT at the end
bexhoma tpch \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -nlp 8 \
  -xii \
  -xic \
  -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_tpch_mariadbcs_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MariaDB MariaDBCS  sf=1"


#### TPC-DS next to MariaDB; the test SQL warnings fails on Q33, see docs/DBMS.md
bexhoma tpcds \
  -dbms MariaDB MariaDBCS \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 32Gi \
  -rr 32Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 30Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_tpcds_mariadbcs_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MariaDBCS  sf=1"


#### SSB star schema
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mariadbcs_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MariaDBCS  sf=1"


#### SSB flat schema
# -xsv flat                     one denormalized table lineorder_flat
bexhoma ssb \
  -dbms MariaDBCS \
  -sf 1 \
  -xsv flat \
  -xis \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 16Gi \
  -rr 16Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 20Gi \
  -rsr \
  -nc 2 \
  -ar \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mariadbcs_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MariaDBCS flat  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
