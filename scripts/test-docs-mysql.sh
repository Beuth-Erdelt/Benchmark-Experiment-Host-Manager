#!/bin/bash
# Generates documentation summaries for MySQL experiments (Example-MySQL.md).
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
#### Main Example ##################################
####################################################


# Main example: TPC-H power test on MySQL, quick, without monitoring
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL simple  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on MySQL
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL monitoring  sf=10"


# Application metrics (-ma): run in scripts/test-docs-appmetrics.sh, logs docs_<benchmark>_mysql_appmetrics.log


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H throughput test on MySQL, the second run uses the loaded volume
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 128Gi                     RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 150Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 128Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 150Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL throughput  sf=10  ne=1,2"


# Persistent storage: TPC-H on MySQL on a RAM disk
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect metrics for the whole experiment
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rst ramdisk                  storage class for persistent volumes
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rst ramdisk \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_ramdisk.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL ramdisk  sf=10"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS power test on MySQL
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
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
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL simple  sf=1"


# TPC-DS monitoring on MySQL
# -dbms MySQL                   DBMS under test
# -sf 3                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=64Gi tmpdir of MySQL in RAM, larger than the template (32Gi)
# --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=32G internal temp tables stay in RAM instead of spilling to disk (default 1G)
# --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=32G size limit of one in-memory internal temp table (default 16M)
# --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=32G size limit of MEMORY tables (default 16M)
# -rr 128Gi                     RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MySQL \
  -sf 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=32G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=32G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=32G \
  -rr 128Gi \
  -rsr \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL monitoring  sf=3"


# TPC-DS throughput test on MySQL, on persistent storage
# -dbms MySQL                   DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=72Gi tmpdir of MySQL in RAM, larger than the template (32Gi): a 48Gi tmpfs ran full with two clients (counts against the memory limit: 32G pool + 72Gi stays below 128Gi)
# --set deployment[bexhoma-deployment-mysql].container[dbms].sort_buffer_size=32M sorts of TPC-DS stay in memory (default 256K: thousands of merge passes with temporary files)
# --set deployment[bexhoma-deployment-mysql].container[dbms].join_buffer_size=64M hash joins stay in memory (default 256K)
# --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=1G internal temporary tables up to 1G in memory (default 16M)
# --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=1G MEMORY tables up to 1G (default 16M)
# --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=4G RAM of the TempTable engine (default 1G)
# -rr 128Gi                     RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MySQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -nc 2 \
  -ne 1,2 \
  -nbp 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 128Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  --set deployment[bexhoma-deployment-mysql].volume[mysqltmp].sizeLimit=72Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].sort_buffer_size=32M \
  --set deployment[bexhoma-deployment-mysql].container[dbms].join_buffer_size=64M \
  --set deployment[bexhoma-deployment-mysql].container[dbms].tmp_table_size=1G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].max_heap_table_size=1G \
  --set deployment[bexhoma-deployment-mysql].container[dbms].temptable_max_ram=4G \
  -rr 128Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mysql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MySQL throughput  sf=10  ne=1,2"


####################################################
#### Benchbase TPC-C ###############################
####################################################


# Benchbase TPC-C: simple
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL simple  sf=16"


# Benchbase TPC-C: persistent storage
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 1                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL persistency  sf=16  nc=2"


# Benchbase TPC-C: monitoring
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL monitoring  sf=16"


# Benchbase TPC-C: scaling the clients, on the volume of the persistent storage run
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -xnbf 8                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mysql_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MySQL complex  sf=16  nc=2  ne=1,2"


####################################################
#### HammerDB TPC-C ################################
####################################################


# HammerDB TPC-C: simple
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL simple  sf=16"


# HammerDB TPC-C: monitoring, on persistent storage
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nlt 8                        threads per loader pod
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 128Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -nlt 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 128Gi \
  -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL monitoring  sf=16"


# HammerDB TPC-C: scaling the clients, on the volume of the monitoring run
# -dbms MySQL                   DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -nlt 8                        threads per loader pod
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MySQL \
  -sf 16 \
  -xsd 2 \
  -nlt 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mysql_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB MySQL complex  sf=16  nc=2  ne=1,2"


####################################################
#### YCSB ##########################################
####################################################


# YCSB: scaling the loader
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4,8                      number of loader pods
# -nlt 32,64                    total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_loading.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL loader scaling  sf=1"


# YCSB: persistent storage, loads the volume for the following runs
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL persistency  sf=1  nc=2"


# YCSB: scaling the benchmarker, on the loaded volume
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL scaling  sf=1  nc=2  ne=1,2"


# YCSB: workload E, on the loaded volume
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl e                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 8                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_workload_e.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL workload e  sf=1"


# YCSB: monitoring, on the loaded volume
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -xnlf 1                       loader thread multiplier factor
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -xnbf 1                       benchmarking thread multiplier factor
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MySQL \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mysql_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB MySQL monitoring  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MySQL: 3 query streams and one RF1/RF2 stream in parallel
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -ne 3                         parallel query streams
# -xrs 3                        refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn/-rnl/-rnb $BEXHOMA_NODE_*      schedule SUT, loader and benchmarker pods on these nodes
bexhoma tpch \
  -dbms MySQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii \
  -xic \
  -xis \
  -ne 3 \
  -xrs 3 \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mysql_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MySQL refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
