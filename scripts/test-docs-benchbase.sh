#!/bin/bash
# Generates documentation summaries for Benchbase experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




###########################################
############### Benchbase #################
###########################################


#### Benchbase Scale (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_scale.log

report_result $? "Benchbase scale  sf=16  nbp=1,2"


#### Benchbase Monitoring (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_monitoring.log

report_result $? "Benchbase monitoring  sf=16  nbp=1,2"

#### Benchbase client resources (Example-Benchbase.md)
# Resources of the clients: loader and benchmarker for a growing number of terminals
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 0                        no throughput target, every terminal runs as fast as it can
# -nbp 1                        one benchmarking pod
# -nbt 40,80,160,320            terminals to sweep (comma-separated)
# -m                            collect SUT resource metrics
# -mc                           collect metrics of loader and benchmarker
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start, so the loader is measured
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 0 \
  -nbp 1 \
  -nbt 40,80,160,320 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_clients.log

report_result $? "Benchbase clients  sf=16  nbt=40,80,160,320"



#### Benchbase Persistent Storage (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nc 2 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_storage.log

report_result $? "Benchbase storage  sf=16  nbp=1  nc=2"


#### Benchbase Reset Script (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 4                         scaling factor (controls database size)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration -- reset runs before each
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 40                       threads per benchmarking pod (10x warehouses)
# -ar                           activate configured reset scripts before each round
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 2 \
  -nbp 1 \
  -nbt 40 \
  -ar \
  -ms $BEXHOMA_MS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_reset.log

report_result $? "Benchbase reset script  sf=4  nc=2"


#### Benchbase Unlimited Target and Warmup (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 4                         scaling factor (controls database size)
# -xsd 2                        benchmark duration in minutes (measured, after warmup)
# -xwu 60                       warmup in seconds before the measured duration, not part of the results
# -xtb 0                        no throughput target (unlimited rate)
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep -- 0 stays unlimited when split over pods
# -nbt 40                       threads per benchmarking pod (10x warehouses)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 4 \
  -xsd 2 \
  -xwu 60 \
  -xtb 0 \
  -xnbf 1 \
  -nbp 1,2 \
  -nbt 40 \
  -ms $BEXHOMA_MS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_unlimited.log

report_result $? "Benchbase unlimited target + warmup  sf=4  nbp=1,2"


#### Benchbase Keying and Thinking Time (Example-Benchbase.md)
# -dbms PostgreSQL              DBMS under test
# -sf 160                       scaling factor (controls database size)
# -xsd 30                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 1                       throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1600                     threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 100Gi                    size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=2000 raise connection limit above -nbt terminals
bexhoma benchbase \
  -dbms PostgreSQL \
  -sf 160 \
  -xsd 30 \
  -xtb 1024 \
  -xnbf 1 \
  -nc 1 \
  -ne 1 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -xkey \
  -m \
  -ms $BEXHOMA_MS \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 100Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=2000 \
  run &>$LOG_DIR/docs_benchbase_postgresql_keytime.log

report_result $? "Benchbase keytime  sf=160  nbp=1,2,5,10"


###########################################
############## Clean Folder ###############
###########################################


report_total
clean_logs
