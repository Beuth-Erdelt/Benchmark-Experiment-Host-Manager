#!/bin/bash
# Core set of reference experiments: the release gate of minor releases.
#
# Runs one experiment per benchmark on PostgreSQL, plus monitoring, application
# monitoring and persistent storage, BEXHOMA_PARALLEL of them at a time. The commands
# are copied unchanged from the test-docs-* scripts (tests/test_reference_experiments.py
# checks that they agree), so the logs are those of the documentation, in logs_tests.
# At the end it checks every log: at least one passed test, no failed test, no
# traceback, and the installed bexhoma version. A minor release needs all of them to pass.
#
# Runs:
#    1. TPC-H with monitoring                        docs_tpch_postgresql_monitoring (test-docs-tpch)
#    2. TPC-H with persistent storage                docs_tpch_postgresql_storage (test-docs-tpch)
#    3. TPC-H refresh stream                         docs_tpch_postgresql_refresh (test-docs-tpch)
#    4. TPC-DS                                       docs_tpcds_postgresql (test-docs-tpcds)
#    5. SSB                                          docs_ssb_postgresql (test-docs-ssb)
#    6. YCSB with monitoring                         docs_ycsb_postgresql_monitoring (test-docs-ycsb)
#    7. Benchbase TPC-C                              docs_benchbase_postgresql_run (test-docs-modes)
#    8. HammerDB TPC-C                               docs_hammerdb_postgresql_run (test-docs-modes)
#    9. application monitoring (Benchbase TPC-C)     docs_benchbase_postgresql_appmetrics (test-docs-appmetrics)
#   10. hardware (fio, WAL sync writes)              docs_hardware_fio_wal_sync_fdatasync (test-docs-hardware)
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# number of experiments that run at the same time
BEXHOMA_PARALLEL="${BEXHOMA_PARALLEL:-4}"

source ./scripts/testfunctions.sh
prepare_logs

BEXHOMA_VERSION=$(python -m pip show bexhoma | awk '/^Version:/ {print $2}')
# without the version, every log would pass the version check
if [[ -z "$BEXHOMA_VERSION" ]]; then
    echo "bexhoma is not installed (python -m pip show bexhoma)" >&2
    exit 1
fi
echo "$(date '+%Y-%m-%d %H:%M:%S') bexhoma $BEXHOMA_VERSION, $BEXHOMA_PARALLEL experiments at a time"


#### 1. TPC-H with monitoring (test-docs-tpch.sh)
reference_tpch_postgresql_monitoring() {
# -dbms PostgreSQL              DBMS under test
# -sf 10                        scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 150Gi                    size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 10 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -m \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  -rr 64Gi \
  -rss 150Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run &>$LOG_DIR/docs_tpch_postgresql_monitoring.log
}


#### 2. TPC-H with persistent storage (test-docs-tpch.sh)
reference_tpch_postgresql_storage() {
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nc 2                         number of repeated runs per configuration
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete any existing PVC for the SUT before starting
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -nc 2 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run &>$LOG_DIR/docs_tpch_postgresql_storage.log
}


#### 3. TPC-H refresh stream (test-docs-tpch.sh)
reference_tpch_postgresql_refresh() {
# -dbms PostgreSQL
# -sf 1
# -ne 3
# -nlp 8
# -nlt 8
# -xii
# -xic
# -xis
# -ms $BEXHOMA_MS
# -xrs 3
# -lr 64Gi
# -rr 64Gi
# -rss 50Gi
# -rnn $BEXHOMA_NODE_SUT
# -rnl $BEXHOMA_NODE_LOAD
# -rnb $BEXHOMA_NODE_BENCHMARK
# --set deployment[bexhoma-deployment-postgres].container[dbms].random_page_cost=1.1
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=200
# --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=io_uring
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers_per_gather=2
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_parallel_workers=4
# --set deployment[bexhoma-deployment-postgres].container[dbms].max_worker_processes=6
# --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB
# --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB
# --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=1GB
# --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB
bexhoma tpch \
  -dbms PostgreSQL \
  -sf 1 \
  -ne 3 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -ms $BEXHOMA_MS \
  -xrs 3 \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run &>$LOG_DIR/docs_tpch_postgresql_refresh.log
}


#### 4. TPC-DS (test-docs-tpcds.sh)
reference_tpcds_postgresql() {
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
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
bexhoma tpcds \
  -dbms PostgreSQL \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
  run &>$LOG_DIR/docs_tpcds_postgresql.log
}


#### 5. SSB (test-docs-ssb.sh)
reference_ssb_postgresql() {
# -dbms PostgreSQL              DBMS under test
# -sf 1                         scaling factor (lineorder has about 6 million rows per SF)
# -nlp 8                        number of loader pods (lineorder is generated in 8 chunks)
# -xii                          create indexes after data load
# -xic                          add primary and foreign keys after data load
# -xis                          run ANALYZE after data load
# -xdt                          also measure data transfer volume per query
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
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
  -nlp 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
}


#### 6. YCSB with monitoring (test-docs-ycsb.sh)
reference_ycsb_postgresql_monitoring() {
# -dbms PostgreSQL              DBMS under test
# -sf 3                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50% read / 50% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 2,3                     throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1,8                      benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms PostgreSQL \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 2,3 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1,8 \
  -nbt 64 \
  -m \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_postgresql_monitoring.log
}


#### 7. Benchbase TPC-C (test-docs-modes.sh)
reference_benchbase_postgresql_run() {
# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 8                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 64 \
  -nbp 8 \
  -nbt 64 \
  -m \
  -ms $BEXHOMA_MS \
  -ss \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_run.log
}


#### 8. HammerDB TPC-C (test-docs-modes.sh)
reference_hammerdb_postgresql_run() {
# -dbms PostgreSQL              DBMS under test
# -nlp 1                        number of data loader pods
# -nlt 1                        threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod (virtual users)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -ss                           skip data generation (assume data exists)
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma hammerdb \
  -dbms PostgreSQL \
  -nlp 1 \
  -nlt 1 \
  -nbp 1 \
  -nbt 64 \
  -m \
  -ms $BEXHOMA_MS \
  -ss \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hammerdb_postgresql_run.log
}


#### 9. application monitoring (Benchbase TPC-C) (test-docs-appmetrics.sh)
reference_benchbase_postgresql_appmetrics() {
# -dbms PostgreSQL              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 160                      threads per benchmarking pod
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
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
  -ma \
  -ms $BEXHOMA_MS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_benchbase_postgresql_appmetrics.log
}


#### 10. hardware (fio, WAL sync writes) (test-docs-hardware.sh)
reference_hardware_fio_wal_sync_fdatasync() {
    # Same as the WAL sync-write fsync example in Example-Hardware.md but
    # fdatasync instead of fsync. fdatasync skips the inode-metadata sync fsync
    # does, and is PostgreSQL's Linux default (wal_sync_method=fdatasync) -
    # compare its latency against that fsync result to confirm it is actually
    # cheaper on this storage.
# -dbms Hardware                hardware target(s) to test
# -xht fio                      benchmark tool: fio (disk I/O)
# -xts 4G                       fio test file size
# -xtd 60                       seconds per fio round
# -xfrw write                   sequential write, simulating WAL append
# -xfbs 8k                      fio block size, one WAL page per write
# -xfid 1                       queue depth, fixed (single outstanding write)
# -xfe libaio                   fio ioengine
# -xffd 1                       fdatasync after every write (wal_sync_method=fdatasync)
# -xfow 1                       prefilled test file: writes go into written blocks, like recycled WAL segments
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nbp 1                        benchmarking pod count
# -nbt 1                        threads per benchmarking pod, fixed (single backend)
# -m                            collect SUT resource metrics
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -rsr                          delete any existing PVC, so every command starts from a clean volume
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pod on this node
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 8k \
  -xfid 1 \
  -xfe libaio \
  -xffd 1 \
  -xfow 1 \
  -ne 1 \
  -nbp 1 \
  -nbt 1 \
  -m \
  -ms $BEXHOMA_MS \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fdatasync.log
}


RUNS=(
    reference_tpch_postgresql_monitoring
    reference_tpch_postgresql_storage
    reference_tpch_postgresql_refresh
    reference_tpcds_postgresql
    reference_ssb_postgresql
    reference_ycsb_postgresql_monitoring
    reference_benchbase_postgresql_run
    reference_hammerdb_postgresql_run
    reference_benchbase_postgresql_appmetrics
    reference_hardware_fio_wal_sync_fdatasync
)


#### run them, BEXHOMA_PARALLEL at a time
for run in "${RUNS[@]}"; do
    while (( $(jobs -rp | wc -l) >= BEXHOMA_PARALLEL )); do
        wait -n
    done
    echo "$(date '+%Y-%m-%d %H:%M:%S') [START] $run"
    ( $run; echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] $run" ) &
    sleep 30
done
wait


#### check the logs
failed=0
for log in docs_tpch_postgresql_monitoring docs_tpch_postgresql_storage docs_tpch_postgresql_refresh docs_tpcds_postgresql docs_ssb_postgresql docs_ycsb_postgresql_monitoring docs_benchbase_postgresql_run docs_hammerdb_postgresql_run docs_benchbase_postgresql_appmetrics docs_hardware_fio_wal_sync_fdatasync; do
    file="$LOG_DIR/$log.log"
    problems=()
    grep -q "TEST passed" "$file" 2>/dev/null || problems+=("no passed test")
    grep -q "TEST failed" "$file" 2>/dev/null && problems+=("failed test")
    grep -q "^Traceback" "$file" 2>/dev/null && problems+=("traceback")
    grep -q "bexhoma version $BEXHOMA_VERSION" "$file" 2>/dev/null || problems+=("not bexhoma $BEXHOMA_VERSION")
    if (( ${#problems[@]} )); then
        echo "FAILED  $log: $(IFS=,; echo "${problems[*]}" | sed 's/,/, /g')"
        failed=1
    else
        echo "passed  $log"
    fi
done


###########################################
############## Clean Folder ###############
###########################################


clean_logs

if (( failed )); then
    echo "Reference experiments: FAILED"
    exit 1
fi
echo "Reference experiments: all passed with bexhoma $BEXHOMA_VERSION"
