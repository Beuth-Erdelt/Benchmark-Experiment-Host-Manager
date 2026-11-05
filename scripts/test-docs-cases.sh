#!/bin/bash
# Test runs that compare several DBMS in one experiment (TestCases.md).
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
#### TPC-H #########################################
####################################################


# TPC-H: compare PostgreSQL, MonetDB, MySQL and MariaDB
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H compare  sf=1"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS: compare PostgreSQL, MonetDB, MySQL and MariaDB
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS compare  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
