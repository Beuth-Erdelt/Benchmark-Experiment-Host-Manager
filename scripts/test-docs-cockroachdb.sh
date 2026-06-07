#!/bin/bash
# Generates documentation summaries for CockroachDB experiments.
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
################## CockroachDB ##################
#################################################


#### YCSB Ingestion (Example-CockroachDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
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
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB ingestion  sf=1  nbp=1"


#### YCSB PVC (Example-CockroachDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
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
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB storage  sf=1  nbp=1  nc=2"


#### YCSB Scale (Example-CockroachDB.md)
bexhoma ycsb -ms 1 -tr \
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
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB scale  sf=10  nbp=1"


#### Benchbase Simple (Example-CockroachDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB simple  sf=16  nbp=1,2"


#### Benchbase Complex (Example-CockroachDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 128 \
  -sd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB complex  sf=128  nbp=1,2,4,8"


#### Benchbase Complex with PVC (Example-CockroachDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 128 \
  -sd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  -rst shared -rss 100Gi -rsr \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB storage  sf=128  nbp=1,2,4,8"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
