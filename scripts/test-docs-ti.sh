#!/bin/bash
# Generates documentation summaries for TiDB experiments.
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
##################### TiDB ######################
#################################################


#### YCSB Ingestion (Example-TiDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  --workload a \
  -dbms TiDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_tidb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB TiDB  sf=1  nbp=1"


bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 3 \
  -nsr 3 \
  -dbms TiDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_tidb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase TiDB  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
