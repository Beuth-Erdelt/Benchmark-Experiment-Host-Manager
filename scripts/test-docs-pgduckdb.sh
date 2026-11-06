#!/bin/bash
# Generates documentation summaries for PgDuckDB experiments (Example-PgDuckDB.md).
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


# Main example: TPC-H power test on PgDuckDB in the DuckDB engine, quick, without monitoring
# -dbms PgDuckDB                DBMS under test
# -xdfe                         run the queries in the DuckDB engine of pg_duckdb
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma tpch \
  -dbms PgDuckDB \
  -xdfe \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_pgduckdb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PgDuckDB  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H power test on PgDuckDB in the DuckDB engine
# -dbms PgDuckDB                DBMS under test
# -xdfe                         run the queries in the DuckDB engine of pg_duckdb
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma tpch \
  -dbms PgDuckDB \
  -xdfe \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_pgduckdb_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PgDuckDB monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H on PgDuckDB in the DuckDB engine, the second run uses the loaded volume
# -dbms PgDuckDB                DBMS under test
# -xdfe                         run the queries in the DuckDB engine of pg_duckdb
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma tpch \
  -dbms PgDuckDB \
  -xdfe \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_pgduckdb_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PgDuckDB storage  sf=1  nc=2"


####################################################
#### Variants ######################################
####################################################


# Variant: TPC-H power test on PgDuckDB in the executor of PostgreSQL (without -xdfe)
# -dbms PgDuckDB                DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma tpch \
  -dbms PgDuckDB \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-pg-duck].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_tpch_pgduckdb_postgresql_engine.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PgDuckDB PostgreSQL engine  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on PgDuckDB: 3 query streams and one RF1/RF2 stream in parallel
# -dbms PgDuckDB                DBMS under test
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
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn/-rnl/-rnb $BEXHOMA_NODE_*      schedule SUT, loader and benchmarker pods on these nodes
bexhoma tpch \
  -dbms PgDuckDB \
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
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_tpch_pgduckdb_refresh.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H PgDuckDB refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
