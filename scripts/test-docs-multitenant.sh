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

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 10Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb schema                   tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst cephcsi \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -nlp $BEXHOMA_NUM_TENANTS     number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 10Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb database                 tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp $BEXHOMA_NUM_TENANTS \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 10Gi \
  -rst cephcsi \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne 1,1                       parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -tr                           verify result meets basic sanity requirements
# -rsr                          delete and recreate the PVC at experiment start
# -rss 5Gi                      size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb container                tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne 1,1 \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -xii -xic -xis \
  -tr \
  -rsr \
  -rss 5Gi \
  -rst cephcsi \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log

wait_process "tpch"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 20Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb schema                   tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst cephcsi \
  -mtb schema \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 20Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb database                 tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 20Gi \
  -rst cephcsi \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -ne 1,1                       parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 10Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb container                tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 1 \
  -xsd 5 \
  -ne 1,1 \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 10Gi \
  -rst cephcsi \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######## Benchbase TPC-C Multi-Tenant MySQL ########
####################################################

BEXHOMA_NUM_TENANTS=2

# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb database                 tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 1 \
  -xsd 5 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst cephcsi \
  -mtb database \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -ne 1,1                       parallel client counts for loading and benchmarking
# -nlp 1                        number of data loader pods
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 10                       threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 50Gi                     size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -mtb container                tenant isolation level (schema / database / container)
# -mtn $BEXHOMA_NUM_TENANTS     number of tenants
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 1 \
  -xsd 5 \
  -ne 1,1 \
  -nlp 1 \
  -nbp 1 \
  -nbt 10 \
  -xkey \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst cephcsi \
  -mtb container \
  -mtn $BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
