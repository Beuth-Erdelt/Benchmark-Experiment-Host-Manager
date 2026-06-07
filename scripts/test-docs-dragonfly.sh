#!/bin/bash
# Generates documentation summaries for Dragonfly experiments.
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
################## YCSB Dragonfly ##################
####################################################


# Single host Dragonfly
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Dragonfly \
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
  -rr 64Gi -lr 64Gi \
  run &>$LOG_DIR/doc_ycsb_dragonfly_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly single  sf=1  nbp=1"


# Cluster of 3 Dragonfly instances
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Dragonfly \
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
  -rr 64Gi -lr 64Gi \
  run &>$LOG_DIR/doc_ycsb_dragonfly_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3  sf=1  nbp=1"


# Cluster of 3 Dragonfly instances and replication
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Dragonfly \
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
  run &>$LOG_DIR/doc_ycsb_dragonfly_3.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3 replication  sf=1  nbp=1"


# Single host Dragonfly with PVC
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 50Gi -rsr \
  -rr 64Gi -lr 64Gi \
  run &>$LOG_DIR/doc_ycsb_dragonfly_4.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly single PVC  sf=1  nbp=1  nc=2"


# Cluster of 3 Dragonfly instances and PVC
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Dragonfly \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rst shared -rss 50Gi -rsr \
  -rr 64Gi -lr 64Gi \
  run &>$LOG_DIR/doc_ycsb_dragonfly_5.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3 PVC  sf=1  nbp=1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
