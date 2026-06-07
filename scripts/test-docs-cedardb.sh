#!/bin/bash
# Generates documentation summaries for CedarDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




#### TCP-H Monitoring (Example-TPC-H.md)
bexhoma tpch -ms 5 -dt -tr \
  -dbms CedarDB \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_cedardb_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H CedarDB monitoring  sf=3"


#### YCSB Scale Loading (Example-YCSB.md)
bexhoma ycsb -ms 5 -tr \
  -sf 1 \
  --workload a \
  -dbms CedarDB \
  -tb 16384 \
  -nlp 1,8 \
  -nlt 64 \
  -nlf 1,4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_cedardb_loading.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CedarDB loading  sf=1  nlp=1,8"


#### Benchbase CH-benCHmark (Example-Benchbase-Others.md)
bexhoma benchbase -ms 2 -tr \
  -sf 10 \
  -sd 5 \
  -dbms CedarDB \
  -nbp 1 \
  -nbt 100 \
  -nbf 16 \
  -tb 1024 \
  -b chbenchmark \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_chbenchmark_cedardb_simple.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CedarDB chbenchmark simple  sf=10  nbp=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
