#!/bin/bash
# Generates documentation summaries for application metrics experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

# Config nodes and paths
BEXHOMA_NODE_SUT="cl-worker14"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

# Check for file
if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

# Check for directories
for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."


if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."




####################################################
########## PostgreSQL Application Metrics ##########
####################################################


#### Benchbase Application Metrics (Example-Benchbase.md)
bexhoma benchbase -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_postgresql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PostgreSQL appmetrics  sf=16  nbp=1,2"


#### YCSB Application Metrics (Example-YCSB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_testcase_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PostgreSQL appmetrics  sf=3  nbp=1,8"


#### TPC-H Application Metrics (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PostgreSQL appmetrics  sf=3"


#### TPC-DS Application Metrics (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr -lr 64Gi \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS PostgreSQL appmetrics  sf=3"


#### HammerDB Application Metrics (Example-HammerDB.md)
bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB PostgreSQL appmetrics  sf=16  nbp=1,2"


####################################################
############ MySQL Application Metrics #############
####################################################


#### Benchbase MySQL Application Metrics
bexhoma benchbase -m -mc -ma -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms MySQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_mysql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL appmetrics  sf=16  nbp=1,2"


#### YCSB MySQL Application Metrics
bexhoma ycsb -ms 1 -tr -lr 64Gi \
  -sf 3 \
  --workload a \
  -dbms MySQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2,3 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_run_mysql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL appmetrics  sf=3  nbp=1,8"


#### TPC-H MySQL Application Metrics
bexhoma tpch -ms 1 -dt -tr -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_run_mysql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL appmetrics  sf=3"


#### TPC-DS MySQL Application Metrics
bexhoma tpcds -ms 1 -dt -tr -lr 64Gi \
  -rr 64Gi -lr 64Gi \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_run_mysql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL appmetrics  sf=3"


#### HammerDB MySQL Application Metrics
bexhoma hammerdb -ms 1 -tr -lr 64Gi \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms MySQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_run_mysql_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL appmetrics  sf=16  nbp=1,2"


####################################################
######### CockroachDB Application Metrics ##########
####################################################


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
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_cockroachdb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB appmetrics  sf=10  nbp=1"


#### Benchbase CockroachDB Application Metrics
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
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_cockroachdb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB appmetrics  sf=16  nbp=1,2"


####################################################
############ Redis Application Metrics #############
####################################################


bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
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
  run &>$LOG_DIR/doc_ycsb_run_redis_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis appmetrics  sf=1  nbp=1"


####################################################
############# TiDB Application Metrics #############
####################################################


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
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_tidb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB TiDB appmetrics  sf=1  nbp=1"


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
  run &>$LOG_DIR/doc_benchbase_run_tidb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase TiDB appmetrics  sf=16  nbp=1,2"


####################################################
########### PGBouncer Application Metrics ##########
####################################################


bexhoma ycsb -ms 1 -tr \
  -sf 16 \
  -sfo 16 \
  --workload c \
  -dbms PGBouncer \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rr 64Gi -lr 64Gi \
  -tb 16384 \
  -nlp 16 \
  -nlt 64 \
  -nlf 11 \
  -nbp 16 \
  -nbt 128 \
  -nbf 11 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  -npp 4 \
  -npi 128 \
  -npo 64 \
  run &>$LOG_DIR/doc_ycsb_run_pgbouncer_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB PGBouncer appmetrics  sf=16  nbp=16"


#### Benchbase PGBouncer Application Metrics
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 10 \
  -xconn \
  -dbms PGBouncer \
  -nbp 1,2 \
  -nbt 32 \
  -nbf 16 \
  -tb 1024 \
  -npp 2 \
  -npi 32 \
  -npo 32 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_run_pgbouncer_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase PGBouncer appmetrics  sf=16  nbp=1,2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
