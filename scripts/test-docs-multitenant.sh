#!/bin/bash
# Generates documentation summaries for multi-tenancy experiments.
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
######### Benchbase TPC-H Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb schema                   tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -tr                           verify result meets basic sanity requirements
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size in GB)
# --dbms PostgreSQL             DBMS under test
# -ii                           create indexes after data load
# -ic                           enforce constraints after data load
# -is                           run ANALYZE after data load
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nlt 64                       threads per loader pod
# -ne 1,1                       parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 5Gi                      size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nlt 1 -nbp 1 -nlt 64 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 5Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb schema                   tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 20Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 20Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms PostgreSQL             DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne 1,1                       parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 10Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######## Benchbase TPC-C Multi-Tenant MySQL ########
####################################################

BEXHOMA_NUM_TENANTS=2

# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb database                 tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms MySQL                  DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -rr 64Gi                      RAM requested for the SUT container
# -lr 64Gi                      RAM limit for the SUT container
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -mtb container                tenant isolation level (schema / database / container)
# -sf 1                         scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# --dbms MySQL                  DBMS under test
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -ne 1,1                       parallel client counts for loading and benchmarking
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
