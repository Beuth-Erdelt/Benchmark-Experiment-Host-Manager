#!/bin/bash
# Generates documentation summaries for SSB (Star Schema Benchmark) experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




###########################################
################### SSB ###################
###########################################


#### SSB PostgreSQL (Example-SSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_ssb_postgresql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB PostgreSQL  sf=1"


#### SSB MonetDB (Example-SSB.md)
# -dbms MonetDB                 DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms MonetDB \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_monetdb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MonetDB  sf=1"


#### SSB ClickHouse (Example-SSB.md)
# -dbms ClickHouse              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms ClickHouse \
  -sf 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_clickhouse.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB ClickHouse  sf=1"


#### SSB Flat (Example-SSB.md)
# -dbms PostgreSQL MonetDB ClickHouse  DBMS under test (all three)
# -sf 1                                scaling factor (lineorder has about 6 million rows per SF)
# -xsv flat                            one denormalized table lineorder_flat, generated as flat files
# -xii                                 create indexes after data load
# -xis                                 run ANALYZE after data load
# -nlp 8                               number of loader pods (lineorder is generated in 8 chunks)
# -xdt                                 also measure data transfer volume per query
# -ms $BEXHOMA_MS                      max simultaneous DBMS configurations
# -t 1200                              query timeout in seconds
# -tr                                  verify result meets basic sanity requirements
# -lr 64Gi                             RAM limit for the SUT container
# -rr 64Gi                             RAM requested for the SUT container
# -rss 50Gi                            size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT               schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD              schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK         schedule benchmarker pods on this node
# -ks no                               remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL MonetDB ClickHouse \
  -sf 1 \
  -xsv flat \
  -xii \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_ssb_flat.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB flat  sf=1"


#### SSB Random Parameters (Example-SSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xqv random                   random query parameters that keep the filter factor of each query
# -xrcp                         new random parameters for each stream
# -ne 1,2                       parallel client counts to sweep (comma-separated)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -xqv random \
  -xrcp \
  -ne 1,2 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_ssb_random.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB random  sf=1  ne=1,2"


#### SSB Persistent Storage (Example-SSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -nc 2                         number of repeated runs per configuration (2nd run: data survives the SUT restart)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  run &>$LOG_DIR/docs_ssb_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB storage  sf=1  nc=2"


#### SSB Load (Example-SSB.md)
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  load &>$LOG_DIR/docs_ssb_load.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB load  sf=1"


#### SSB Profiling (Example-SSB.md)
# -dbms PostgreSQL MonetDB ClickHouse  DBMS under test (all three)
# -sf 1                                scaling factor (lineorder has about 6 million rows per SF)
# -nlp 8                               number of loader pods (lineorder is generated in 8 chunks)
# -xdt                                 also measure data transfer volume per query
# -ms $BEXHOMA_MS                      max simultaneous DBMS configurations
# -t 1200                              query timeout in seconds
# -tr                                  verify result meets basic sanity requirements
# -lr 64Gi                             RAM limit for the SUT container
# -rr 64Gi                             RAM requested for the SUT container
# -rss 50Gi                            size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT               schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD              schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK         schedule benchmarker pods on this node
# -ks no                               remove the SUT at the end
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 lower planner cost for random reads (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 allow more concurrent prefetch I/O requests (SSD)
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring use io_uring for asynchronous I/O
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 parallel workers per query node
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 total parallel worker pool
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 total background worker processes
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB PostgreSQL buffer cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB planner estimate of OS-level cache size
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB per-operation sort/hash memory
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB memory for index/vacuum maintenance
bexhoma ssb \
  -dbms PostgreSQL MonetDB ClickHouse \
  -sf 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  profiling &>$LOG_DIR/docs_ssb_profiling.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB profiling  sf=1"


#### SSB ClickHouseCluster (Example-SSB.md)
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms ClickHouseCluster \
  -nw 3 \
  -sf 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_ssb_clickhousecluster.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB ClickHouseCluster  sf=1  nw=3"


#### SSB ClickHouseCluster distributed dimensions (Example-SSB.md)
# -dbms ClickHouseCluster       DBMS under test
# -nw 3                         number of worker nodes (shards)
# -xdim distributed             dimensions spread over the shards like lineorder (default: a copy on every node)
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms ClickHouseCluster \
  -nw 3 \
  -xdim distributed \
  -sf 1 \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_ssb_clickhousecluster_distributed.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB ClickHouseCluster distributed dimensions  sf=1  nw=3  xdim=distributed"


#### SSB PgDuckDB (Example-SSB.md)
# -dbms PgDuckDB                DBMS under test
# -xdfe                         run the queries in pg_duckdb's DuckDB engine
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms PgDuckDB \
  -xdfe \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_pgduckdb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB PgDuckDB  sf=1"


#### SSB CedarDB (Example-SSB.md)
# -dbms CedarDB                DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms CedarDB \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_cedardb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB CedarDB  sf=1"


#### SSB Citus (Example-SSB.md)
# -dbms Citus                   DBMS under test
# -nw 3                         number of worker nodes
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -rnw $BEXHOMA_NODES_WORKER    schedule worker pods on these nodes (joined by '+')
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms Citus \
  -nw 3 \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -rnw $BEXHOMA_NODES_WORKER \
  -ks no \
  run &>$LOG_DIR/docs_ssb_citus.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB Citus  sf=1  nw=3"


#### SSB MySQL (Example-SSB.md)
# -dbms MySQL                   DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms MySQL \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mysql.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MySQL  sf=1"


#### SSB MariaDB (Example-SSB.md)
# -dbms MariaDB                 DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run statistics after data load
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -ks no                        remove the SUT at the end
bexhoma ssb \
  -dbms MariaDB \
  -sf 1 \
  -xii \
  -xic \
  -xis \
  -nlp 8 \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  -ks no \
  run &>$LOG_DIR/docs_ssb_mariadb.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] SSB MariaDB  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
