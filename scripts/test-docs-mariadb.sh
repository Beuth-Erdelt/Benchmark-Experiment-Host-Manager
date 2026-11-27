#!/bin/bash
# Generates documentation summaries for MariaDB experiments (Example-MariaDB.md).
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


# Main example: TPC-H power test on MariaDB, quick, without monitoring
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb.log

report_result $? "TPC-H MariaDB simple  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on MariaDB
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_monitoring.log

report_result $? "TPC-H MariaDB monitoring  sf=1"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H throughput test on MariaDB, the second run uses the loaded volume
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_storage.log

report_result $? "TPC-H MariaDB throughput  sf=1  ne=1,2"


# Persistent storage: TPC-H on MariaDB on a RAM disk
# -dbms MariaDB                 DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ma                           collect metrics for the whole experiment
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 150Gi                    size of the persistent volume claim
# -rst ramdisk                  storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -dbms MariaDB \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ma \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 150Gi \
  -rst ramdisk \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_ramdisk.log

report_result $? "TPC-H MariaDB ramdisk  sf=10"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS power test on MariaDB
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb.log

report_result $? "TPC-DS MariaDB simple  sf=1"


# TPC-DS monitoring on MariaDB
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb_monitoring.log

report_result $? "TPC-DS MariaDB monitoring  sf=1"


# TPC-DS throughput test on MariaDB, on persistent storage
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -dbms MariaDB \
  -sf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 8 \
  -nbp 1 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 128Gi \
  -rr 128Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpcds_mariadb_storage.log

report_result $? "TPC-DS MariaDB throughput  sf=1  ne=1,2"


####################################################
#### Benchbase TPC-C ###############################
####################################################


# Benchbase TPC-C: simple
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -xnbf 8                       benchmarking thread multiplier factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb.log

report_result $? "Benchbase MariaDB simple  sf=16"


# Benchbase TPC-C: persistent storage
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 1                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -xnbf 8                       benchmarking thread multiplier factor
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 1 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 2 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_storage.log

report_result $? "Benchbase MariaDB persistency  sf=16  nc=2"


# Benchbase TPC-C: monitoring
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -xnbf 8                       benchmarking thread multiplier factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 160 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_monitoring.log

report_result $? "Benchbase MariaDB monitoring  sf=16"


# Benchbase TPC-C: scaling the clients, on the volume of the persistent storage run
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -xtb 1024                     target throughput (ops/s)
# -xnbf 8                       benchmarking thread multiplier factor
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nbp 1,2                      number of benchmarking pods
# -nbt 160                      total benchmarking threads
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -xtb 1024 \
  -xnbf 8 \
  -nc 2 \
  -ne 1,2 \
  -nbp 1,2 \
  -nbt 160 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_mariadb_scale.log

report_result $? "Benchbase MariaDB complex  sf=16  nc=2  ne=1,2"


####################################################
#### HammerDB TPC-C ################################
####################################################


# HammerDB TPC-C: simple
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb.log

report_result $? "HammerDB MariaDB simple  sf=16"


# HammerDB TPC-C: monitoring, on persistent storage
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1                        number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_monitoring.log

report_result $? "HammerDB MariaDB monitoring  sf=16"


# HammerDB TPC-C: scaling the clients, on the volume of the monitoring run
# -dbms MariaDB                 DBMS under test
# -sf 16                        scaling factor (controls database size in GB)
# -xsd 2                        benchmark duration in minutes
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlt 8                        threads per loader pod
# -nbp 1,2                      number of benchmarking pods
# -nbt 16                       total benchmarking threads
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms MariaDB \
  -sf 16 \
  -xsd 2 \
  -nc 2 \
  -ne 1,2 \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_mariadb_scale.log

report_result $? "HammerDB MariaDB complex  sf=16  nc=2  ne=1,2"


####################################################
#### YCSB ##########################################
####################################################


# YCSB: scaling the loader
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -xnbf 1                       benchmarking thread multiplier factor
# -xnlf 1                       loader thread multiplier factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 4,8                      number of loader pods
# -nlt 32,64                    total loader threads
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_loading.log

report_result $? "YCSB MariaDB loader scaling  sf=1"


# YCSB: persistent storage, loads the volume for the following runs
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -xnbf 1                       benchmarking thread multiplier factor
# -xnlf 1                       loader thread multiplier factor
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -nbp 1                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_storage.log

report_result $? "YCSB MariaDB persistency  sf=1  nc=2"


# YCSB: scaling the benchmarker, on the loaded volume
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -xnbf 1                       benchmarking thread multiplier factor
# -xnlf 1                       loader thread multiplier factor
# -nc 2                         number of repeated runs per configuration
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 2 \
  -ne 1,2 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_scale.log

report_result $? "YCSB MariaDB scaling  sf=1  nc=2  ne=1,2"


# YCSB: workload E, on the loaded volume
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl e                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -xnbf 1                       benchmarking thread multiplier factor
# -xnlf 1                       loader thread multiplier factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -nbp 8                        number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl e \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_workload_e.log

report_result $? "YCSB MariaDB workload e  sf=1"


# YCSB: monitoring, on the loaded volume
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -xwl a                        YCSB workload letter
# -xtb 1024                     target throughput (ops/s)
# -xnbf 1                       benchmarking thread multiplier factor
# -xnlf 1                       loader thread multiplier factor
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of loader pods
# -nlt 64                       total loader threads
# -nbp 1,8                      number of benchmarking pods
# -nbt 64                       total benchmarking threads
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G buffer pool fitting the RAM limit (template: 8G)
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms MariaDB \
  -sf 1 \
  -xwl a \
  -xtb 1024 \
  -xnbf 1 \
  -xnlf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  --set deployment[bexhoma-deployment-mariadb].container[dbms].innodb_buffer_pool_size=32G \
  -rr 64Gi \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_mariadb_monitoring.log

report_result $? "YCSB MariaDB monitoring  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MariaDB: 3 query streams and one RF1/RF2 stream in parallel
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -ne 3                         parallel query streams
# -xrs 3                        refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 128Gi                     RAM limit for the SUT container
# -rr 128Gi                     RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT
# -rnl $BEXHOMA_NODE_LOAD
# -rnb $BEXHOMA_NODE_BENCHMARK
bexhoma tpch \
  -dbms MariaDB \
  -sf 1 \
  -ne 3 \
  -xrs 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -lr 128Gi \
  -rr 128Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_mariadb_refresh.log

report_result $? "TPC-H MariaDB refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


report_total
clean_logs
