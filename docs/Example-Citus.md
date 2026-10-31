# Example: Benchmark Citus

This differs from the default behaviour of bexhoma, since we benchmark **a distributed DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Citus is a PostgreSQL extension, that introduces sharding [1].
A cluster has an instance of PostgreSQL with Citus as a coordinator (here called master, managed by a Kubernetes deployment).
More instances can register at the master as worker nodes (here managed by Kubernetes stateful sets).
Bexhoma also deploys a service for communication external to Citus (from within the cluster) and a headless service for communication between the pods of the Citus cluster.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Citus: https://www.citusdata.com/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Benchbase Repository: https://github.com/cmu-db/benchbase/wiki/TPC-C
1. OLTP-Bench: An Extensible Testbed for Benchmarking Relational Databases: http://www.vldb.org/pvldb/vol7/p277-difallah.pdf
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
BEXHOMA_NODES_WORKER_4="cl-worker36+cl-worker37+cl-worker29+cl-worker39"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example: 
```bash
bexhoma ycsb \
  -dbms Citus \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_citus_1.log
```

This
* loops over `n` in [8] and `t` in [4]
  * starts a clean instance of Citus (`-dbms`) with 3 workers (`-nw`), no replication (one instance `-nwr`) and 32 shards (`-nws`)
    * data directory inside a Docker container
  * creates YCSB schema in each database
  * starts `n` loader pods per DBMS
    * with a loading container each
      * threads = 64/`n` (`-nlt`)
      * target throughput is `t` * 16384
      * generates YCSB data = 10.000.000 rows (i.e., SF=10, `-sf`)
      * imports it into the DBMS
  * loops over `m` in [1] and `s` in [4]
    * runs `m` parallel streams of YCSB queries per DBMS
      * 10.000.000 operations (`-xop`)
      * workload A = 50% read / 50% write (`--workload`)
      * target throughput is `s` * 16384
      * threads = 64/`m` (`-nbt`)
    * with a maximum of 1 DBMS per time (`-ms`)
* tests if results match workflow (`-tr`)
* monitors (`-m`) all components (`-mc`)
* shows a summary

### Status

You can watch the status while benchmark is running via `bexhoma status`

```bash
Dashboard: Running
Cluster Prometheus: Running
Message Queue: Running
Data directory: Running
Result directory: Running
+------------------+--------------+------------+-------------+
| 1741884177       | sut          | use case   | worker      |
+==================+==============+============+=============+
| Citus-64-8-65536 | (1. Running) | ycsb       | (3 Running) |
+------------------+--------------+------------+-------------+
```

The code `1730133803` is the unique identifier of the experiment.
You can find the number also in the output of `ycsb.py`.

### Cleanup

The script is supposed to clean up and remove everything from the cluster that is related to the experiment after finishing.
If something goes wrong, you can also clean up manually with `bexperiment stop` (removes everything) or `bexperiment stop -e 1730133803` (removes everything that is related to experiment `1730133803`).

## Evaluate Results

At the end of a benchmark you will see a summary like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_citus_1_summary.md" target="_blank" rel="noopener">docs_ycsb_citus_1.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 956s 
* Code: 1792797544
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:959179
  * datadisk:42
  * volume_size:1.8T
  * volume_used:937G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:959179
    * datadisk:884
    * volume_size:1.8T
    * volume_used:937G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:471922
    * datadisk:869
    * volume_size:1.8T
    * volume_used:461G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:351700
    * datadisk:887
    * volume_size:879G
    * volume_used:344G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792797544
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-citus-1-1792797544-7598c6c864-jngl2: 0
* bexhoma-worker-citus-ycsb-1-0: 0
* bexhoma-worker-citus-ycsb-1-1: 0
* bexhoma-worker-citus-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| citus-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7675.30 |                16286.00 |            125000.00 |                               902.00 | 1.00 |              221.05 |
| citus-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7637.79 |                16366.00 |            125000.00 |                               935.00 | 1.00 |              219.97 |
| citus-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7657.44 |                16324.00 |            125000.00 |                               940.00 | 1.00 |              220.53 |
| citus-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7071.74 |                17676.00 |            125000.00 |                               940.00 | 1.00 |              203.67 |
| citus-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7668.24 |                16301.00 |            125000.00 |                              1015.00 | 1.00 |              220.85 |
| citus-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7659.78 |                16319.00 |            125000.00 |                               910.00 | 1.00 |              220.60 |
| citus-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7632.66 |                16377.00 |            125000.00 |                               913.00 | 1.00 |              219.82 |
| citus-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7626.60 |                16390.00 |            125000.00 |                               972.00 | 1.00 |              219.65 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Citus-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              203.67 |                        60629.54 |                17676.00 |           1000000.00 |                               940.88 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 | Citus-1         |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        63945.98 |               156382.00 |            4998603 |                            1167.00 |              5001397 |                              1752.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        63945.98 |               156382.00 |            4998603 |                            1167.00 |              5001397 |                              1752.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       121.81 |      4.79 |           0.54 |                  0.58 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       207.53 |      5.63 |           2.92 |                  5.46 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |         0.42 |      0.00 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |         0.27 |      0.00 |           0.54 |                  0.58 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      3552.71 |     26.95 |           5.62 |                 10.10 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      1036.50 |     12.01 |           1.37 |                  1.38 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>

To see the summary again you can simply call `bexhoma summary -e 1730133803` with the experiment code.

### Detailed Evaluation

Results are transformed into pandas DataFrames and can be inspected in detail.
See for example
* [Jupyter Notebooks](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/evaluator_dbmsbenchmarker/notebooks/)

You can connect to an evaluation server locally by `bexhoma jupyter`.
This forwards ports, so you have
* a Jupyter notebook server at http://localhost:8888




## Monitoring

[Monitoring](Monitoring.html) can be activated for DBMS only (`-m`) or for all components (`-mc`).

All metrics in monitoring are summed across all matching components.
In this example, this means that used memory, CPU time, etc. are summed across all 3 nodes of the Citus cluster ("worker") and the coordinator ("SUT deployment").


## Use Persistent Storage

The default behaviour of bexhoma is that the database is stored inside the ephemeral storage of the Docker container.
If your cluster allows dynamic provisioning of volumes, you might request a persistent storage of a certain type (storageClass) and size.
With repetitions (`-nc`), `-rsr` removes an existing volume only before the first repetition and later repetitions reuse it without loading; `-rsrp` removes it before every repetition. See [Concepts](Concepts.html).

Example:
```bash
bexhoma ycsb \
  -dbms Citus \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_ycsb_citus_2.log
```
The following status shows we have one volume of type `shared`.
Every Citus experiment will take the databases from these volumes and skip loading.
In this example `-nc` is set to two, that is the complete experiment is repeated twice for statistical confidence.
The first instance of Citus mounts the volume and generates the data.
All other instances just use the database without generating and loading data.
Bexhoma uses two types of volumes.
The first one is attached to the coordinator and is used to persist infos across experiments (and not to store actual data).
The other volumes (worker volumes) are attached to the worker pods and store the actual data.


```bash
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+
| Volumes                                | configuration   | experiment   | loaded [s]   |   timeLoading [s] | dbms            | storage_class_name   | storage   | status   | size   | used   |
+========================================+=================+==============+==============+===================+=================+======================+===========+==========+========+========+
| bexhoma-storage-citus-ycsb-1           | citus           | ycsb-1       | True         |                26 | Citus           | shared               | 50Gi      | Bound    | 50.0G  | 40.0M  |
+----------------------------------------+-----------------+--------------+--------------+-------------------+-----------------+----------------------+-----------+----------+--------+--------+

+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| Volumes of Workers                | configuration     |   experiment | dbms   | storage_class_name   | storage   | status   | size   | used   |
+===================================+===================+==============+========+======================+===========+==========+========+========+
| bxw-bexhoma-worker-citus-ycsb-1-0 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-citus-ycsb-1-1 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.4G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
| bxw-bexhoma-worker-citus-ycsb-1-2 | Citus-64-8-65536  |   1742471862 | Citus  | shared               | 50Gi      | Bound    | 50.0G  | 1.2G   |
+-----------------------------------+-------------------+--------------+--------+----------------------+-----------+----------+--------+--------+
```

The result looks something like

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_ycsb_citus_2_summary.md" target="_blank" rel="noopener">docs_ycsb_citus_2.log</a></summary>

```markdown
## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1840s 
* Code: 1793434499
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:860691
  * datadisk:42
  * volume_size:49G
  * volume_used:42M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:860691
    * datadisk:868
    * volume_size:49G
    * volume_used:868M
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:538284
    * datadisk:869
    * volume_size:49G
    * volume_used:869M
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:573723
    * datadisk:870
    * volume_size:49G
    * volume_used:870M
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793434499
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3
* citus-1-2-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:860694
  * datadisk:58
  * volume_size:49G
  * volume_used:58M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:860694
    * datadisk:1716
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:538286
    * datadisk:1791
    * volume_size:49G
    * volume_used:1.8G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:573724
    * datadisk:1624
    * volume_size:49G
    * volume_used:1.6G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793434499
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_shards:48
    * ddl_num_worker_replicas:1

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Citus-1-2

### Data Parameters of Reused Volumes
* Citus-1: DDL values of the volume: num_worker_shards=48, num_worker_replicas=1, fillfactor=100
* Citus-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-citus-1-1793434499-775564cdf4-7z4ln: 0
* bx-w-citus-nvme-ycsb-1-0: 0
* bx-w-citus-nvme-ycsb-1-1: 0
* bx-w-citus-nvme-ycsb-1-2: 0
* bexhoma-sut-citus-1-1793434499-675c4c8755-hqc7z: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Citus-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Citus-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| citus-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7720.82 |                16190.00 |            125000.00 |                              1405.00 | 1.00 |              222.36 |
| citus-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7674.83 |                16287.00 |            125000.00 |                              1336.00 | 1.00 |              221.04 |
| citus-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7697.52 |                16239.00 |            125000.00 |                              1284.00 | 1.00 |              221.69 |
| citus-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7600.17 |                16447.00 |            125000.00 |                              1228.00 | 1.00 |              218.88 |
| citus-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7714.62 |                16203.00 |            125000.00 |                              1398.00 | 1.00 |              222.18 |
| citus-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7635.45 |                16371.00 |            125000.00 |                              1301.00 | 1.00 |              219.90 |
| citus-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7689.47 |                16256.00 |            125000.00 |                              1402.00 | 1.00 |              221.46 |
| citus-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         7659.31 |                16320.00 |            125000.00 |                              1413.00 | 1.00 |              220.59 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Citus-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              218.88 |                        61392.19 |                16447.00 |           1000000.00 |                              1345.88 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 | Citus-1         |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        39329.82 |               254260.00 |            4998931 |                            1631.00 |              5001069 |                             19631.00 |
| citus-1-2-1-1-1 | citus-1-2-1 | citus-1-2-1-1 | Citus-1         |                2 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                        42033.05 |               237908.00 |            5001607 |                            1566.00 |              4998393 |                             13687.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                        39329.82 |               254260.00 |            4998931 |                            1631.00 |              5001069 |                             19631.00 |
| citus-1-2-1 | citus-1-2-1 |                2 |        64 |    65536 |               1 |           1 |            0 |                        42033.05 |               237908.00 |            5001607 |                            1566.00 |              4998393 |                             13687.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       118.88 |      2.83 |           0.54 |                  0.58 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       247.04 |      6.37 |           3.34 |                  5.60 |

### Loading phase: component loader

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| citus-1-1-1-1 | n/a          |         0 |           0.30 |                  0.31 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |         0.49 |      0.01 |           0.54 |                  0.58 |
| citus-1-2-1-1 |         0.47 |      0.01 |           0.53 |                  0.55 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      5071.38 |     23.08 |           5.69 |                 10.31 |
| citus-1-2-1-1 |      4385.47 |     22.32 |           5.64 |                  9.92 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      1104.67 |      7.79 |           1.07 |                  1.08 |
| citus-1-2-1-1 |       900.29 |      5.90 |           1.08 |                  1.09 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
```

</details>


## YCSB Example Explained


### Configuration of Bexhoma

In `cluster.config` there is a section:

```python
'Citus': {
    'loadData': 'psql -U postgres < {scriptname}',
    'attachWorker': "psql -U postgres --command=\"SELECT * from master_add_node('{worker}.{service_sut}', 5432);\"",
    'template': {
        'version': '10.0.2',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", "password1234"],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres',#/{dbname}',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```

where
* `loadData`: This command is used to create the schema
* `JDBC`: These infos are used to configure YCSB


Citus uses the PostgreSQL JDBC driver.



### Schema SQL File

Before ingestion, we run a script to create and distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/Citus/initschema-ycsb.sql

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/ycsb/Citus/checkschema-ycsb.sql








## Benchbase's TPC-C

Before ingestion, we run a script to create and distribute the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/benchbase/Citus/initschema-benchbase.sql

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/benchbase/Citus/checkschema-benchbase.sql

### Benchbase Simple Example

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.

```bash
bexhoma benchbase \
  -dbms Citus \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_benchbase_citus_1.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_citus_1_summary.md" target="_blank" rel="noopener">docs_benchbase_citus_1.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=16
* Type: benchbase
* Duration: 1301s 
* Code: 1793436377
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 16. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 5 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:863683
  * datadisk:43
  * volume_size:1.8T
  * volume_used:844G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:863609
    * datadisk:2200
    * volume_size:1.8T
    * volume_used:844G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539081
    * datadisk:793
    * volume_size:879G
    * volume_used:527G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574745
    * datadisk:1021
    * volume_size:1.8T
    * volume_used:562G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793436377
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3
* citus-1-1-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:864991
  * datadisk:77
  * volume_size:1.8T
  * volume_used:845G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:864991
    * datadisk:3371
    * volume_size:1.8T
    * volume_used:845G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539372
    * datadisk:1083
    * volume_size:879G
    * volume_used:527G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:575136
    * datadisk:1412
    * volume_size:1.8T
    * volume_used:562G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793436377
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-citus-1-1793436377-8c69ffb68-rtmgn: 0
* bx-w-citus-1-1793436377-0: 0
* bx-w-citus-1-1793436377-1: 0
* bx-w-citus-1-1793436377-2: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |   16 |      118.00 |           4.00 |            0.00 |        104.00 |           10.00 |              1 |           1 |             | None           |             0 | False         |              488.14 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 |                1 |          16 |    16384 |        1 |               1 |       1 |          -1 | 300.00 |            0 |                        1458.35 |                     1451.89 |         0.00 |                                                      28542.00 |                                              10963.00 |
| citus-1-1-2-1-1 | citus-1-1-2 | citus-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       1 |          -1 | 300.00 |            1 |                         677.81 |                      671.92 |         0.00 |                                                      29955.00 |                                              11792.00 |
| citus-1-1-2-1-2 | citus-1-1-2 | citus-1-1-2-1 |                1 |           8 |     8192 |        2 |               1 |       2 |          -1 | 300.00 |            0 |                         694.90 |                      688.85 |         0.00 |                                                      29613.00 |                                              11501.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |   time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|-------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |          16 |    16384 |               1 |           1 |          -1 | 300.00 |            0 |                        1458.35 |                     1451.89 |         0.00 |                                                      28542.00 |                                              10963.00 |
| citus-1-1-2 | citus-1-1-2 |                1 |          16 |    16384 |               1 |           2 |          -1 | 300.00 |            1 |                        1372.72 |                     1360.78 |         0.00 |                                                      29955.00 |                                              11646.50 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>

### Benchbase More Complex

TPC-C is performed at 128 warehouses.
The 64 threads of the client are split into a cascading sequence of 1,2,4 and 8 pods.
Old PVCs of the workers are removed before loading (`-rsr`).

The benchmark is run via

```bash
bexhoma benchbase \
  -dbms Citus \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 100Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_benchbase_citus_2.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_citus_2_summary.md" target="_blank" rel="noopener">docs_benchbase_citus_2.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 7549s 
* Code: 1793437718
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [16]. Benchmarking runs for 20 minutes.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.11.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29, cl-worker39.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:862789
  * datadisk:43
  * volume_size:98G
  * volume_used:43M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:862789
    * datadisk:6466
    * volume_size:98G
    * volume_used:6.4G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:538980
    * datadisk:8547
    * volume_size:98G
    * volume_used:8.4G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:234080
    * datadisk:9264
    * volume_size:98G
    * volume_used:9.1G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:573725
    * datadisk:6218
    * volume_size:98G
    * volume_used:6.1G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793437718
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:862758
  * datadisk:438
  * volume_size:98G
  * volume_used:438M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:862758
    * datadisk:18115
    * volume_size:98G
    * volume_used:18G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:538983
    * datadisk:14940
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:235771
    * datadisk:16497
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:573725
    * datadisk:10192
    * volume_size:98G
    * volume_used:10G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793437718
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:863864
  * datadisk:453
  * volume_size:98G
  * volume_used:453M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:863864
    * datadisk:27806
    * volume_size:98G
    * volume_used:28G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:538971
    * datadisk:21581
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:235798
    * datadisk:23118
    * volume_size:98G
    * volume_used:23G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:573726
    * datadisk:14378
    * volume_size:98G
    * volume_used:15G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793437718
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:863624
  * datadisk:730
  * volume_size:98G
  * volume_used:730M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:863624
    * datadisk:30951
    * volume_size:98G
    * volume_used:31G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:540124
    * datadisk:23948
    * volume_size:98G
    * volume_used:24G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:235807
    * datadisk:25856
    * volume_size:98G
    * volume_used:26G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:575684
    * datadisk:17299
    * volume_size:98G
    * volume_used:17G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793437718
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4

### SUT Container Restarts
* bexhoma-sut-citus-1-1793437718-6685597896-g7z6v: 0
* bx-w-citus-nvme-benchbase-tpcc-128-0: 0
* bx-w-citus-nvme-benchbase-tpcc-128-1: 0
* bx-w-citus-nvme-benchbase-tpcc-128-2: 0
* bx-w-citus-nvme-benchbase-tpcc-128-3: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS Citus-1 - Experiment 1 Client 4: benchbase (8 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: benchbase (4 pods)
* DBMS Citus-1 - Experiment 1 Client 4: benchbase (8 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |  128 |     1719.00 |           4.00 |            0.00 |       1699.00 |           16.00 |              1 |           1 |             | None           |             0 | False         |              268.06 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 |                1 |          64 |    16384 |        1 |               1 |       1 |          -1 | 1200.00 |            0 |                        5417.35 |                     5393.26 |         0.00 |                                                      31178.00 |                                              11810.00 |
| citus-1-1-2-1-1 | citus-1-1-2 | citus-1-1-2-1 |                1 |          32 |     8192 |        2 |               1 |       1 |          -1 | 1200.00 |            9 |                        2441.27 |                     2420.73 |         0.00 |                                                      33646.00 |                                              13103.00 |
| citus-1-1-2-1-2 | citus-1-1-2 | citus-1-1-2-1 |                1 |          32 |     8192 |        2 |               1 |       2 |          -1 | 1200.00 |           11 |                        2427.75 |                     2407.35 |         0.00 |                                                      33599.00 |                                              13176.00 |
| citus-1-1-3-1-1 | citus-1-1-3 | citus-1-1-3-1 |                1 |          16 |     4096 |        3 |               1 |       1 |          -1 | 1200.00 |           15 |                         979.87 |                      967.28 |         0.00 |                                                      39320.00 |                                              16321.00 |
| citus-1-1-3-1-2 | citus-1-1-3 | citus-1-1-3-1 |                1 |          16 |     4096 |        3 |               1 |       2 |          -1 | 1200.00 |            6 |                        1001.69 |                      988.98 |         0.00 |                                                      38210.00 |                                              15966.00 |
| citus-1-1-3-1-3 | citus-1-1-3 | citus-1-1-3-1 |                1 |          16 |     4096 |        3 |               1 |       3 |          -1 | 1200.00 |           16 |                         988.64 |                      975.84 |         0.00 |                                                      39114.00 |                                              16177.00 |
| citus-1-1-3-1-4 | citus-1-1-3 | citus-1-1-3-1 |                1 |          16 |     4096 |        3 |               1 |       4 |          -1 | 1200.00 |            6 |                         981.39 |                      968.94 |         0.00 |                                                      39105.00 |                                              16297.00 |
| citus-1-1-4-1-1 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       1 |          -1 | 1200.00 |            7 |                         303.49 |                      299.33 |         0.00 |                                                      74694.00 |                                              26348.00 |
| citus-1-1-4-1-2 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       2 |          -1 | 1200.00 |            4 |                         298.71 |                      294.60 |         0.00 |                                                      76878.00 |                                              26772.00 |
| citus-1-1-4-1-3 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       3 |          -1 | 1200.00 |            4 |                         296.75 |                      292.75 |         0.00 |                                                      76748.00 |                                              26948.00 |
| citus-1-1-4-1-4 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       4 |          -1 | 1200.00 |            3 |                         305.33 |                      301.12 |         0.00 |                                                      74731.00 |                                              26191.00 |
| citus-1-1-4-1-5 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       5 |          -1 | 1200.00 |            1 |                         292.95 |                      288.94 |         0.00 |                                                      78030.00 |                                              27298.00 |
| citus-1-1-4-1-6 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       6 |          -1 | 1200.00 |            2 |                         305.84 |                      301.71 |         0.00 |                                                      72160.00 |                                              26147.00 |
| citus-1-1-4-1-7 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       7 |          -1 | 1200.00 |            4 |                         298.09 |                      293.99 |         0.00 |                                                      74966.00 |                                              26825.00 |
| citus-1-1-4-1-8 | citus-1-1-4 | citus-1-1-4-1 |                1 |           8 |     2048 |        4 |               1 |       8 |          -1 | 1200.00 |            4 |                         301.19 |                      297.04 |         0.00 |                                                      75306.00 |                                              26551.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |          64 |    16384 |               1 |           1 |          -1 | 1200.00 |            0 |                        5417.35 |                     5393.26 |         0.00 |                                                      31178.00 |                                              11810.00 |
| citus-1-1-2 | citus-1-1-2 |                1 |          64 |    16384 |               1 |           2 |          -1 | 1200.00 |           20 |                        4869.02 |                     4828.08 |         0.00 |                                                      33646.00 |                                              13139.50 |
| citus-1-1-3 | citus-1-1-3 |                1 |          64 |    16384 |               1 |           4 |          -1 | 1200.00 |           43 |                        3951.59 |                     3901.05 |         0.00 |                                                      39320.00 |                                              16190.25 |
| citus-1-1-4 | citus-1-1-4 |                1 |          64 |    16384 |               1 |           8 |          -1 | 1200.00 |           29 |                        2402.34 |                     2369.48 |         0.00 |                                                      78030.00 |                                              26635.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       870.48 |      2.67 |           2.07 |                  2.11 |
| citus-1-1-2-1 |       870.48 |      2.67 |           2.07 |                  2.11 |
| citus-1-1-3-1 |       870.48 |      2.67 |           2.07 |                  2.11 |
| citus-1-1-4-1 |       870.48 |      2.67 |           2.07 |                  2.11 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      4681.64 |      8.82 |          15.83 |                 45.53 |
| citus-1-1-2-1 |      4681.64 |      8.82 |          15.83 |                 45.53 |
| citus-1-1-3-1 |      4681.64 |      8.82 |          15.83 |                 45.53 |
| citus-1-1-4-1 |      4681.64 |      8.82 |          15.83 |                 45.53 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |    189554.53 |    120.94 |           0.40 |                  0.40 |
| citus-1-1-2-1 |    189554.53 |    120.94 |           0.40 |                  0.40 |
| citus-1-1-3-1 |    189554.53 |    120.94 |           0.40 |                  0.40 |
| citus-1-1-4-1 |    189554.53 |    120.94 |           0.40 |                  0.40 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |     15305.20 |     13.60 |           0.90 |                  1.32 |
| citus-1-1-2-1 |     13501.65 |     12.45 |           0.90 |                  1.33 |
| citus-1-1-3-1 |     10421.12 |     10.18 |           0.91 |                  1.62 |
| citus-1-1-4-1 |      5778.91 |      5.34 |           0.91 |                  1.78 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |     35092.91 |     31.66 |          26.43 |                 83.89 |
| citus-1-1-2-1 |     33423.49 |     29.02 |          32.32 |                116.90 |
| citus-1-1-3-1 |     25439.45 |     22.44 |          36.50 |                132.15 |
| citus-1-1-4-1 |     12618.53 |     11.30 |          39.08 |                144.26 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      7301.16 |      6.62 |           0.94 |                  0.94 |
| citus-1-1-2-1 |      7123.43 |      6.29 |           0.86 |                  0.89 |
| citus-1-1-3-1 |      6398.81 |      6.57 |           0.41 |                  0.41 |
| citus-1-1-4-1 |      3971.19 |      5.02 |           0.30 |                  0.30 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Throughput (requests/second) contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey) and the tpcc benchmark)
* TEST passed: Workflow as planned
```

</details>



### Benchbase Realistic

We run a benchmark with
* PVCs for persistent database
* monitoring
* a sensible number of workers (4)
* a sensible size (128 warehouses)
* a sensible number of threads (1024)
* suitable splittings (1x1280, 2x640, 5x256, 10x128)
* logging the state every 30 seconds
* a realistic target (4096 transactions per second)
* a realistic duration (20 minutes)
* a repetition (`-nc` is 2)
* keying and thinking tima activated (`-xkey`)

Note that the number of threads for each pod is a multiple of the number of warehouses.
At start, Benchbase assigns each thread to a fixed warehouse.
This way, we distribute the threads equally to the warehouses.
Each thread also gets assigned a fixed range of districts per warehouse.
Please also note, that this is not compliant to the TPC-C specifications, which state: *For each active warehouse in the database, the SUT must accept requests for transactions from a population of 10 terminals.*

```bash
bexhoma benchbase \
  -dbms Citus \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 4 \
  -nc 2 \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xkey \
  -xli 30 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 100Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_benchbase_citus_3.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_benchbase_citus_3_summary.md" target="_blank" rel="noopener">docs_benchbase_citus_3.log</a></summary>

```markdown
## Show Summary

### Workload
Benchbase Workload tpcc SF=128
* Type: benchbase
* Duration: 10586s 
* Code: 1792381278
* Benchbase runs a TPC-C experiment.
* This experiment compares run time and resource consumption of Benchbase queries in different DBMS.
  * Benchbase data is generated and loaded using several threads. Loading uses a batch size of 128 rows per INSERT.
  * Benchmark is 'tpcc'. Scaling factor is 128. Target is based on multiples of '1024'. Factors for benchmarking are [4]. Benchmarking has keying and thinking times activated. Benchmarking runs for 20 minutes.
  * Status is logged every 30ms.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 100Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [1280] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567772
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:145016
    * datadisk:43941
    * volume_size:98G
    * volume_used:43G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159963
    * datadisk:29424
    * volume_size:98G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:902220
    * datadisk:22014
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:636596
    * datadisk:22285
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:568168
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:146278
    * datadisk:43941
    * volume_size:98G
    * volume_used:43G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159195
    * datadisk:29424
    * volume_size:98G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884522
    * datadisk:22014
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619034
    * datadisk:22285
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567800
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:145258
    * datadisk:43941
    * volume_size:98G
    * volume_used:43G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159196
    * datadisk:29424
    * volume_size:98G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884523
    * datadisk:22014
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619034
    * datadisk:22285
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567812
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:145761
    * datadisk:43947
    * volume_size:98G
    * volume_used:43G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:158933
    * datadisk:29428
    * volume_size:98G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884425
    * datadisk:22018
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619036
    * datadisk:22290
    * volume_size:98G
    * volume_used:22G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:568178
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:147344
    * datadisk:42460
    * volume_size:98G
    * volume_used:42G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:884249
    * datadisk:28143
    * volume_size:98G
    * volume_used:28G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159143
    * datadisk:21120
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619030
    * datadisk:20926
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:567958
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:146959
    * datadisk:42460
    * volume_size:98G
    * volume_used:42G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:883452
    * datadisk:28143
    * volume_size:98G
    * volume_used:28G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159154
    * datadisk:21120
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619032
    * datadisk:20926
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:568121
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:146711
    * datadisk:42460
    * volume_size:98G
    * volume_used:42G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:883452
    * datadisk:28143
    * volume_size:98G
    * volume_used:28G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159155
    * datadisk:21120
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619032
    * datadisk:20926
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:568173
  * datadisk:886
  * volume_size:98G
  * volume_used:886M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:540590800896
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:145161
    * datadisk:42465
    * volume_size:98G
    * volume_used:42G
    * cpu_list:0-95
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1077382627328
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-1060-nvidia
    * node:cl-worker28
    * disk:883439
    * datadisk:28147
    * volume_size:98G
    * volume_used:28G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:159118
    * datadisk:21124
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:619030
    * datadisk:20930
    * volume_size:98G
    * volume_used:21G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * eval_parameters
    * code:1792381278
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4

### Reused Storage
* loading skipped, loading times inherited from an earlier experiment: Citus-1

### SUT Container Restarts
* bexhoma-sut-citus-1-1792381278-864cf966bd-m6ckj: 0
* bexhoma-worker-citus-nvme-benchbase-tpcc-128-0: 0
* bexhoma-worker-citus-nvme-benchbase-tpcc-128-1: 0
* bexhoma-worker-citus-nvme-benchbase-tpcc-128-2: 0
* bexhoma-worker-citus-nvme-benchbase-tpcc-128-3: 0
* bexhoma-sut-citus-1-1792381278-789497dfb5-fkdp2: 0
no benchbase results for pod gczzn.dbmsbenchmarker, left out of the summary
no benchbase results for pod hqqf8.dbmsbenchmarker, left out of the summary
no benchbase results for pod 8gpns.dbmsbenchmarker, left out of the summary
no benchbase results for pod dfc28.dbmsbenchmarker, left out of the summary
no benchbase results for pod gczzn.dbmsbenchmarker, left out of the summary
no benchbase results for pod hqqf8.dbmsbenchmarker, left out of the summary
no benchbase results for pod 8gpns.dbmsbenchmarker, left out of the summary
no benchbase results for pod dfc28.dbmsbenchmarker, left out of the summary

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS Citus-1 - Experiment 1 Client 4: benchbase (10 pods)
* DBMS Citus-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 2 Client 3: benchbase (5 pods)
* DBMS Citus-1 - Experiment 2 Client 4: benchbase (10 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: benchbase (5 pods)
* DBMS Citus-1 - Experiment 1 Client 4: benchbase (10 pods)
* DBMS Citus-1 - Experiment 2 Client 1: benchbase (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: benchbase (2 pods)
* DBMS Citus-1 - Experiment 2 Client 3: benchbase (5 pods)
* DBMS Citus-1 - Experiment 2 Client 4: benchbase (10 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |  128 |      512.00 |           3.00 |            0.00 |        495.00 |           14.00 |              0 |           1 |             | None           |             0 | False         |              900.00 | True                |
| Citus-1-2 |                2 |  128 |      512.00 |           3.00 |            0.00 |        495.00 |           14.00 |              0 |           1 |             | None           |             0 | False         |              900.00 | True                |

### Benchmarking

#### Per Connection

| DBMS             | phase       | job           |   experiment_run |   terminals |   target |   client |   benchmark_run |   child |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:-----------------|:------------|:--------------|-----------------:|------------:|---------:|---------:|----------------:|--------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1-1-1  | citus-1-1-1 | citus-1-1-1-1 |                1 |        1280 |     4096 |        1 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-3-1-1  | citus-1-1-3 | citus-1-1-3-1 |                1 |         256 |      819 |        3 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-3-1-2  | citus-1-1-3 | citus-1-1-3-1 |                1 |         256 |      819 |        3 |               1 |       2 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-3-1-3  | citus-1-1-3 | citus-1-1-3-1 |                1 |         256 |      819 |        3 |               1 |       3 |          -1 | 1200.00 |            0 |                          12.30 |                       12.26 |        20.10 |                                                      45985.00 |                                              20719.00 |
| citus-1-1-3-1-4  | citus-1-1-3 | citus-1-1-3-1 |                1 |         256 |      819 |        3 |               1 |       4 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-3-1-5  | citus-1-1-3 | citus-1-1-3-1 |                1 |         256 |      819 |        3 |               1 |       5 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-4-1-1  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-4-1-2  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       2 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-4-1-3  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       3 |          -1 | 1200.00 |            0 |                           6.21 |                        6.18 |        10.13 |                                                      41137.00 |                                              18762.00 |
| citus-1-1-4-1-4  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       4 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-4-1-5  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       5 |          -1 | 1200.00 |            0 |                           6.17 |                        6.14 |        10.07 |                                                      40256.00 |                                              18688.00 |
| citus-1-1-4-1-6  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       6 |          -1 | 1200.00 |            0 |                           6.11 |                        6.09 |         9.98 |                                                      39749.00 |                                              18521.00 |
| citus-1-1-4-1-7  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       7 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-4-1-8  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       8 |          -1 | 1200.00 |            0 |                           6.01 |                        5.98 |         9.81 |                                                      40872.00 |                                              18980.00 |
| citus-1-1-4-1-9  | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |       9 |          -1 | 1200.00 |            0 |                           6.12 |                        6.09 |         9.99 |                                                      41030.00 |                                              19033.00 |
| citus-1-1-4-1-10 | citus-1-1-4 | citus-1-1-4-1 |                1 |         128 |      409 |        4 |               1 |      10 |          -1 | 1200.00 |            0 |                           6.18 |                        6.15 |        10.08 |                                                      40993.00 |                                              18800.00 |
| citus-1-2-1-1-1  | citus-1-2-1 | citus-1-2-1-1 |                2 |        1280 |     4096 |        1 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-3-1-1  | citus-1-2-3 | citus-1-2-3-1 |                2 |         256 |      819 |        3 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-3-1-2  | citus-1-2-3 | citus-1-2-3-1 |                2 |         256 |      819 |        3 |               1 |       2 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-3-1-3  | citus-1-2-3 | citus-1-2-3-1 |                2 |         256 |      819 |        3 |               1 |       3 |          -1 | 1200.00 |            0 |                          12.22 |                       12.17 |        19.96 |                                                      46810.00 |                                              21724.00 |
| citus-1-2-3-1-4  | citus-1-2-3 | citus-1-2-3-1 |                2 |         256 |      819 |        3 |               1 |       4 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-3-1-5  | citus-1-2-3 | citus-1-2-3-1 |                2 |         256 |      819 |        3 |               1 |       5 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-1  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-2  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       2 |          -1 | 1200.00 |            0 |                           6.17 |                        6.15 |        10.09 |                                                      42533.00 |                                              19465.00 |
| citus-1-2-4-1-3  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       3 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-4  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       4 |          -1 | 1200.00 |            0 |                           6.00 |                        5.96 |         9.78 |                                                      42641.00 |                                              19556.00 |
| citus-1-2-4-1-5  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       5 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-6  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       6 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-7  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       7 |          -1 | 1200.00 |            0 |                           6.14 |                        6.11 |        10.02 |                                                      42565.00 |                                              19341.00 |
| citus-1-2-4-1-8  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       8 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-9  | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |       9 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-4-1-10 | citus-1-2-4 | citus-1-2-4-1 |                2 |         128 |      409 |        4 |               1 |      10 |          -1 | 1200.00 |            0 |                           6.17 |                        6.13 |        10.06 |                                                      42190.00 |                                              19476.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   terminals |   target |   benchmark_run |   pod_count |   tenant_id |    time |   num_errors |   Throughput (requests/second) |   Goodput (requests/second) |   efficiency |   Latency Distribution.95th Percentile Latency (microseconds) |   Latency Distribution.Average Latency (microseconds) |
|:------------|:------------|-----------------:|------------:|---------:|----------------:|------------:|------------:|--------:|-------------:|-------------------------------:|----------------------------:|-------------:|--------------------------------------------------------------:|------------------------------------------------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        1280 |     4096 |               1 |           1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-1-3 | citus-1-1-3 |                1 |        1280 |     4095 |               1 |           5 |          -1 | 1200.00 |            0 |                          12.30 |                       12.26 |        20.10 |                                                      45985.00 |                                               4143.00 |
| citus-1-1-4 | citus-1-1-4 |                1 |        1280 |     4090 |               1 |          10 |          -1 | 1200.00 |            0 |                          36.79 |                       36.63 |        60.08 |                                                      41137.00 |                                              11278.00 |
| citus-1-2-1 | citus-1-2-1 |                2 |        1280 |     4096 |               1 |           1 |          -1 | 1200.00 |            0 |                           0.00 |                        0.00 |         0.00 |                                                         -1.00 |                                                 -1.00 |
| citus-1-2-3 | citus-1-2-3 |                2 |        1280 |     4095 |               1 |           5 |          -1 | 1200.00 |            0 |                          12.22 |                       12.17 |        19.96 |                                                      46810.00 |                                               4344.00 |
| citus-1-2-4 | citus-1-2-4 |                2 |        1280 |     4090 |               1 |          10 |          -1 | 1200.00 |            0 |                          24.48 |                       24.36 |        39.96 |                                                      42641.00 |                                               7783.20 |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| citus-1-1-1-1 | 6.23         |      0.10 |           2.47 |                  2.48 |
| citus-1-1-2-1 | n/a          |      0.01 |           0.53 |                  0.55 |
| citus-1-1-3-1 | 74.78        |      0.45 |           3.06 |                  3.08 |
| citus-1-1-4-1 | 108.41       |      0.47 |           4.26 |                  4.28 |
| citus-1-2-1-1 | 5.76         |      0.12 |           2.47 |                  2.49 |
| citus-1-2-2-1 | n/a          |      0.00 |           0.53 |                  0.55 |
| citus-1-2-3-1 | 49.34        |      0.26 |           3.08 |                  3.10 |
| citus-1-2-4-1 | 75.07        |      0.20 |           3.32 |                  3.34 |

### Benchmarking phase: component worker

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| citus-1-1-1-1 | 18.71        |      0.04 |          27.37 |                112.70 |
| citus-1-1-2-1 | n/a          |      0.03 |          27.37 |                112.69 |
| citus-1-1-3-1 | 180.81       |      0.32 |          31.39 |                118.61 |
| citus-1-1-4-1 | 431.38       |      0.77 |          38.67 |                126.86 |
| citus-1-2-1-1 | 16.83        |      0.03 |           7.04 |                 11.75 |
| citus-1-2-2-1 | n/a          |      0.01 |           7.03 |                 11.75 |
| citus-1-2-3-1 | 155.28       |      0.26 |          10.26 |                 18.41 |
| citus-1-2-4-1 | 281.81       |      0.47 |          13.28 |                 23.28 |

### Benchmarking phase: component benchmarker

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| citus-1-1-1-1 | 66.23        |      0.33 |           0.18 |                  0.18 |
| citus-1-1-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| citus-1-1-3-1 | 239.62       |      1.38 |           0.97 |                  0.97 |
| citus-1-1-4-1 | 581.72       |      6.53 |           0.54 |                  0.54 |
| citus-1-2-1-1 | 52.67        |      0.32 |           0.22 |                  0.22 |
| citus-1-2-2-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| citus-1-2-3-1 | 199.36       |      1.07 |           0.91 |                  0.91 |
| citus-1-2-4-1 | 480.52       |      4.83 |           0.54 |                  0.54 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (storage reused, loading times inherited: Citus-1)
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST failed: Throughput (requests/second) contains 0 or NaN
* TEST passed: Workflow as planned
```

</details>





## HammerDB's TPC-C

HammerDB provides an option to benchmark PostgreSQL with citus compatibility activated.
This generates the tables and functions in an empty database and additionally distributes tables and functions: https://github.com/TPC-Council/HammerDB/blob/master/src/postgresql/pgoltp.tcl

After ingestion, we run a script to check the distributions.
The script also vacuums and analyzes the tables: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpcc/Citus/checkschema-tpcc.sql

### HammerDB Simple Example

TPC-C is performed at 16 warehouses.
The 16 threads of the client are split into a cascading sequence of 1 and 2 pods.
Citus has 3 workers.


```bash
bexhoma hammerdb \
  -dbms Citus \
  -sf 16 \
  -nc 1 \
  -ne 1 \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER \
  run &>$LOG_DIR/docs_hammerdb_citus_1.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_citus_1_summary.md" target="_blank" rel="noopener">docs_hammerdb_citus_1.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=16 (warehouses for TPC-C)
* Type: tpcc
* Duration: 1134s 
* Code: 1792818777
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 16. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [8] threads, split into [1] pods.
  * Benchmarking is tested with [16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:966985
  * datadisk:60
  * volume_size:1.8T
  * volume_used:945G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:966986
    * datadisk:1321
    * volume_size:1.8T
    * volume_used:945G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:473481
    * datadisk:1111
    * volume_size:1.8T
    * volume_used:463G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:352593
    * datadisk:1108
    * volume_size:879G
    * volume_used:345G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 16.0 CPU, 256.0 GiB RAM requested in 4 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792818777
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-citus-1-1792818777-659c5756c4-zpbwj: 0
* bexhoma-worker-citus-hammerdb-16-0: 0
* bexhoma-worker-citus-hammerdb-16-1: 0
* bexhoma-worker-citus-hammerdb-16-2: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |   16 |       77.00 |           5.00 |            0.00 |         60.00 |           12.00 |              1 |           8 |             | None           |             0 | False         |              748.05 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |    TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|-------:|-------------:|-----------:|---------:|-----------:|-----------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 |                1 |       16 |        1 |               1 |       1 |  63691 | 146210 |         0.00 |          5 |        0 |      19.80 |      30.81 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |     NOPM |       TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|---------:|----------:|-----------:|---------:|
| citus-1-1-1 | citus-1-1-1 |                1 |       16 |        1 |               1 |           1 |      19.80 |      30.81 |         0.00 | 63691.00 | 146210.00 |          5 |        0 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>

### HammerDB More Complex Example

```bash
bexhoma hammerdb \
  -dbms Citus \
  -sf 128 \
  -xsd 30 \
  -nc 1 \
  -ne 1 \
  -nlp 1 \
  -nlt 128 \
  -nbp 1,2,4,8 \
  -nbt 128 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 100Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_hammerdb_citus_2.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_citus_2_summary.md" target="_blank" rel="noopener">docs_hammerdb_citus_2.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=128 (warehouses for TPC-C)
* Type: tpcc
* Duration: 9264s 
* Code: 1792819959
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 128. Benchmarking runs for 30 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29, cl-worker39.
  * Database is persisted to disk of type nvme and size 100Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [128] threads, split into [1] pods.
  * Benchmarking is tested with [128] threads, split into [1, 2, 4, 8] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:965292
  * datadisk:99
  * volume_size:98G
  * volume_used:99M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:965292
    * datadisk:8286
    * volume_size:98G
    * volume_used:8.1G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:317964
    * datadisk:6240
    * volume_size:98G
    * volume_used:6.1G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472372
    * datadisk:5625
    * volume_size:98G
    * volume_used:5.5G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:351488
    * datadisk:6448
    * volume_size:98G
    * volume_used:6.3G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792819959
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:965640
  * datadisk:99
  * volume_size:98G
  * volume_used:99M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:965640
    * datadisk:47435
    * volume_size:98G
    * volume_used:47G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:317977
    * datadisk:40207
    * volume_size:98G
    * volume_used:40G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472374
    * datadisk:35251
    * volume_size:98G
    * volume_used:35G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:351493
    * datadisk:35621
    * volume_size:98G
    * volume_used:35G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792819959
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:965658
  * datadisk:99
  * volume_size:98G
  * volume_used:99M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:965658
    * datadisk:58276
    * volume_size:98G
    * volume_used:57G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:317980
    * datadisk:47846
    * volume_size:98G
    * volume_used:47G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472376
    * datadisk:46419
    * volume_size:98G
    * volume_used:46G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:351487
    * datadisk:48327
    * volume_size:98G
    * volume_used:48G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792819959
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:965659
  * datadisk:99
  * volume_size:98G
  * volume_used:99M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:965659
    * datadisk:67320
    * volume_size:98G
    * volume_used:66G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:317982
    * datadisk:52536
    * volume_size:98G
    * volume_used:52G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:472378
    * datadisk:51831
    * volume_size:98G
    * volume_used:51G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:351492
    * datadisk:54186
    * volume_size:98G
    * volume_used:53G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792819959
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4

### SUT Container Restarts
* bexhoma-sut-citus-1-1792819959-56f5c76d9f-dcbjc: 0
* bexhoma-worker-citus-nvme-hammerdb-128-0: 0
* bexhoma-worker-citus-nvme-hammerdb-128-1: 0
* bexhoma-worker-citus-nvme-hammerdb-128-2: 0
* bexhoma-worker-citus-nvme-hammerdb-128-3: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: hammerdb (4 pods)
* DBMS Citus-1 - Experiment 1 Client 4: hammerdb (8 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: hammerdb (4 pods)
* DBMS Citus-1 - Experiment 1 Client 4: hammerdb (8 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |  128 |      163.00 |           5.00 |            0.00 |        142.00 |           16.00 |              1 |         128 |             | None           |             0 | False         |             2826.99 | False               |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |     TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|--------:|-------------:|-----------:|---------:|-----------:|-----------:|
| citus-1-1-1-1-1 | citus-1-1-1 | citus-1-1-1-1 |                1 |      128 |        1 |               1 |       1 | 529670 | 1218380 |         0.00 |         30 |        0 |      23.45 |      36.42 |
| citus-1-1-2-1-1 | citus-1-1-2 | citus-1-1-2-1 |                1 |       64 |        2 |               1 |       1 | 522251 | 1201269 |         0.00 |         30 |        0 |      22.43 |      32.55 |
| citus-1-1-2-1-2 | citus-1-1-2 | citus-1-1-2-1 |                1 |       64 |        2 |               1 |       2 | 522170 | 1201217 |         0.00 |         30 |        0 |      22.40 |      33.12 |
| citus-1-1-3-1-1 | citus-1-1-3 | citus-1-1-3-1 |                1 |       32 |        3 |               1 |       1 | 468661 | 1078030 |         0.00 |         30 |        0 |      23.68 |      34.30 |
| citus-1-1-3-1-2 | citus-1-1-3 | citus-1-1-3-1 |                1 |       32 |        3 |               1 |       2 | 468595 | 1077583 |         0.00 |         30 |        0 |      23.11 |      34.09 |
| citus-1-1-3-1-3 | citus-1-1-3 | citus-1-1-3-1 |                1 |       32 |        3 |               1 |       3 | 468614 | 1077637 |         0.00 |         30 |        0 |      22.48 |      32.26 |
| citus-1-1-3-1-4 | citus-1-1-3 | citus-1-1-3-1 |                1 |       32 |        3 |               1 |       4 | 468665 | 1077834 |         0.00 |         30 |        0 |      23.16 |      33.56 |
| citus-1-1-4-1-1 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       1 | 435819 | 1002522 |         0.00 |         30 |        0 |      23.29 |      34.39 |
| citus-1-1-4-1-2 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       2 | 435861 | 1002845 |         0.00 |         30 |        0 |      22.94 |      34.45 |
| citus-1-1-4-1-3 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       3 | 435783 | 1002465 |         0.00 |         30 |        0 |      22.89 |      33.38 |
| citus-1-1-4-1-4 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       4 | 435821 | 1002547 |         0.00 |         30 |        0 |      23.40 |      35.01 |
| citus-1-1-4-1-5 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       5 | 435854 | 1002845 |         0.00 |         30 |        0 |      22.44 |      33.36 |
| citus-1-1-4-1-6 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       6 | 435786 | 1002465 |         0.00 |         30 |        0 |      23.29 |      34.76 |
| citus-1-1-4-1-7 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       7 | 435815 | 1002505 |         0.00 |         30 |        0 |      22.43 |      32.85 |
| citus-1-1-4-1-8 | citus-1-1-4 | citus-1-1-4-1 |                1 |       16 |        4 |               1 |       8 | 435853 | 1002845 |         0.00 |         30 |        0 |      23.72 |      35.22 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |        TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|-----------:|-----------:|---------:|
| citus-1-1-1 | citus-1-1-1 |                1 |      128 |        1 |               1 |           1 |      23.45 |      36.42 |         0.00 | 529670.00 | 1218380.00 |         30 |        0 |
| citus-1-1-2 | citus-1-1-2 |                1 |      128 |        2 |               1 |           2 |      22.43 |      33.12 |         0.00 | 522210.50 | 1201243.00 |         30 |        0 |
| citus-1-1-3 | citus-1-1-3 |                1 |      128 |        3 |               1 |           4 |      23.68 |      34.30 |         0.00 | 468633.75 | 1077771.00 |         30 |        0 |
| citus-1-1-4 | citus-1-1-4 |                1 |      128 |        4 |               1 |           8 |      23.72 |      35.22 |         0.00 | 435824.00 | 1002629.88 |         30 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       170.62 |      2.58 |           1.03 |                  1.13 |
| citus-1-1-2-1 |       170.62 |      2.58 |           1.03 |                  1.13 |
| citus-1-1-3-1 |       170.62 |      2.58 |           1.03 |                  1.13 |
| citus-1-1-4-1 |       170.62 |      2.58 |           1.03 |                  1.13 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       886.52 |      8.85 |          14.17 |                 32.30 |
| citus-1-1-2-1 |       886.52 |      8.85 |          14.17 |                 32.30 |
| citus-1-1-3-1 |       886.52 |      8.85 |          14.17 |                 32.30 |
| citus-1-1-4-1 |       886.52 |      8.85 |          14.17 |                 32.30 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      1751.86 |     27.52 |           0.71 |                  0.72 |
| citus-1-1-2-1 |      1751.86 |     27.52 |           0.71 |                  0.72 |
| citus-1-1-3-1 |      1751.86 |     27.52 |           0.71 |                  0.72 |
| citus-1-1-4-1 |      1751.86 |     27.52 |           0.71 |                  0.72 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      5700.72 |      3.20 |           1.15 |                  1.25 |
| citus-1-1-2-1 |      5851.57 |      3.23 |           1.16 |                  1.26 |
| citus-1-1-3-1 |      5440.26 |      3.04 |           1.18 |                  1.27 |
| citus-1-1-4-1 |      5275.08 |      2.95 |           1.21 |                  1.31 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |    153378.26 |    122.10 |          50.96 |                203.67 |
| citus-1-1-2-1 |    165506.42 |     95.82 |          75.09 |                253.08 |
| citus-1-1-3-1 |    174842.99 |    104.15 |          90.20 |                255.76 |
| citus-1-1-4-1 |    203477.44 |    121.41 |         100.53 |                255.74 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      6546.63 |      3.58 |           2.77 |                  2.77 |
| citus-1-1-2-1 |      7750.33 |      4.29 |           1.38 |                  1.39 |
| citus-1-1-3-1 |      8498.29 |      4.81 |           0.70 |                  0.71 |
| citus-1-1-4-1 |      8784.45 |      4.98 |           0.35 |                  0.35 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>


### HammerDB Referenced Paper

We here run HammerDB TPROC-C benchmark against Citus similar to [1].
We in particular copy the setting 500 warehouses, 250 virtual users and 4 worker nodes.
There has been made a contribution to HammerDB by [2] and we assume this reflects the configuration used in [1]:
*In case of Citus, we converted the items table to a reference table
and the remaining tables to co-located distributed tables with the
warehouse ID column as the distribution column. Additionally, we
configured Citus to delegate stored procedure calls to worker nodes
based on the warehouse ID argument.*
We configure the experiment to use 48 shards, run for 20 minutes and split the 250 virtual users (sequentially) into 1,2,5 and 10 pods.
Database is persisted on PVCs.
The experiment runs twice for confidence.

Note: In [1] YCSB is run as this: *For this benchmark, the coordinatorâ€™s CPU usage becomes a scaling bottleneck. Hence, we ran the benchmark with every worker node acting as coordinator and configured YCSB to load balance across all nodes.* This apparently uses [4], part of the Citus benchmark toolkit [3], and PostgreSQL loadbalancer feature [5].

[1] [Citus: Distributed PostgreSQL for Data-Intensive Applications](https://dl.acm.org/doi/10.1145/3448016.3457551)
> Umur Cubukcu, Ozgun Erdogan, Sumedh Pathak, Sudhakar Sannakkayala, and Marco Slot.
> 2021. In Proceedings of the 2021 International Conference on Management of Data (SIGMOD '21).
> Association for Computing Machinery, New York, NY, USA, 2490â€“2502.
> https://dl.acm.org/doi/10.1145/3448016.3457551

[2] [How to benchmark performance of Citus and Postgres with HammerDB on Azure](https://techcommunity.microsoft.com/blog/adforpostgresql/how-to-benchmark-performance-of-citus-and-postgres-with-hammerdb-on-azure/3254918)
> JelteF, Microsoft.
> Retrieved April 1, 2025, from https://techcommunity.microsoft.com/blog/adforpostgresql/how-to-benchmark-performance-of-citus-and-postgres-with-hammerdb-on-azure/3254918

[3] [Citus Data Benchmark Toolkit](https://github.com/citusdata/citus-benchmark)
> Citus Data.
> Retrieved April 1, 2025, from https://github.com/citusdata/citus-benchmark

[4] [Citus Data Benchmark Toolkit HammerDB settings](https://github.com/citusdata/citus-benchmark/blob/master/run.tcl)
> Citus Data.
> Retrieved April 1, 2025, from https://github.com/citusdata/citus-benchmark/blob/master/run.tcl

[5] [Adding Postgres 16 support to Citus 12.1, plus schema-based sharding improvements](https://www.citusdata.com/blog/2023/09/22/adding-postgres-16-support-to-citus-12-1)
> Naisila Puka, September 22, 2023.
> Retrieved April 1, 2025, from https://www.citusdata.com/blog/2023/09/22/adding-postgres-16-support-to-citus-12-1

[6] [Understand what you run before publishing your (silly) benchmark results](https://dev.to/yugabyte/understand-what-you-run-before-publishing-your-silly-benchmark-results-48bb)
> Franck Pachot, YugabyteDB.
> Retrieved April 1, 2025, from https://dev.to/yugabyte/understand-what-you-run-before-publishing-your-silly-benchmark-results-48bb


```bash
bexhoma hammerdb \
  -dbms Citus \
  -sf 500 \
  -xsd 20 \
  -nc 2 \
  -ne 1 \
  -nlp 1 \
  -nlt 250 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xlat \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 200Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_hammerdb_citus_3.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hammerdb_citus_3_summary.md" target="_blank" rel="noopener">docs_hammerdb_citus_3.log</a></summary>

```markdown
## Show Summary

### Workload
HammerDB Workload SF=500 (warehouses for TPC-C)
* Type: tpcc
* Duration: 14514s 
* Code: 1792859331
* HammerDB runs the benchmark.
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 500. Benchmarking runs for 20 minutes. Ramp-up period is 2 minutes before measurements begin. Benchmarking also logs latencies.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29, cl-worker39.
  * Database is persisted to disk of type nvme and size 200Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [250] threads, split into [1] pods.
  * Benchmarking is tested with [250] threads, split into [1, 2, 5, 10] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663168
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518881
    * datadisk:29136
    * volume_size:196G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:318092
    * datadisk:23002
    * volume_size:196G
    * volume_used:23G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663169
    * datadisk:21776
    * volume_size:196G
    * volume_used:22G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486433
    * datadisk:28736
    * volume_size:196G
    * volume_used:29G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663080
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518890
    * datadisk:56177
    * volume_size:196G
    * volume_used:55G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:318088
    * datadisk:49900
    * volume_size:196G
    * volume_used:49G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663080
    * datadisk:51059
    * volume_size:196G
    * volume_used:50G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486434
    * datadisk:54606
    * volume_size:196G
    * volume_used:54G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663092
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518897
    * datadisk:63992
    * volume_size:196G
    * volume_used:63G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:318092
    * datadisk:56174
    * volume_size:196G
    * volume_used:55G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663092
    * datadisk:58293
    * volume_size:196G
    * volume_used:57G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486457
    * datadisk:63715
    * volume_size:196G
    * volume_used:63G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-1-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663112
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518905
    * datadisk:71623
    * volume_size:196G
    * volume_used:70G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:332368
    * datadisk:62752
    * volume_size:196G
    * volume_used:62G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663112
    * datadisk:62876
    * volume_size:196G
    * volume_used:62G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486458
    * datadisk:71298
    * volume_size:196G
    * volume_used:70G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663091
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663091
    * datadisk:77742
    * volume_size:196G
    * volume_used:76G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518911
    * datadisk:68780
    * volume_size:196G
    * volume_used:68G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:332419
    * datadisk:69067
    * volume_size:196G
    * volume_used:68G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486461
    * datadisk:77781
    * volume_size:196G
    * volume_used:76G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-2-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663106
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663106
    * datadisk:86434
    * volume_size:196G
    * volume_used:85G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518919
    * datadisk:74486
    * volume_size:196G
    * volume_used:73G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:332426
    * datadisk:74531
    * volume_size:196G
    * volume_used:73G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:486476
    * datadisk:86587
    * volume_size:196G
    * volume_used:85G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-3-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663112
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663112
    * datadisk:92628
    * volume_size:196G
    * volume_used:91G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518926
    * datadisk:79353
    * volume_size:196G
    * volume_used:78G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:332440
    * datadisk:79732
    * volume_size:196G
    * volume_used:78G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:489240
    * datadisk:92032
    * volume_size:196G
    * volume_used:90G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
* citus-1-2-4-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:663138
  * datadisk:217
  * volume_size:196G
  * volume_used:217M
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:663138
    * datadisk:100011
    * volume_size:196G
    * volume_used:98G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:518934
    * datadisk:84757
    * volume_size:196G
    * volume_used:83G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:332445
    * datadisk:84850
    * volume_size:196G
    * volume_used:83G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:490793
    * datadisk:98026
    * volume_size:196G
    * volume_used:96G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792859331
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Citus-1-2

### SUT Container Restarts
* bexhoma-sut-citus-1-1792859331-7444c544cd-8d47g: 0
* bexhoma-worker-citus-nvme-hammerdb-500-0: 0
* bexhoma-worker-citus-nvme-hammerdb-500-1: 0
* bexhoma-worker-citus-nvme-hammerdb-500-2: 0
* bexhoma-worker-citus-nvme-hammerdb-500-3: 0
* bexhoma-sut-citus-1-1792859331-7f5f7bbd4-57j24: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: hammerdb (5 pods)
* DBMS Citus-1 - Experiment 1 Client 4: hammerdb (10 pods)
* DBMS Citus-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 2 Client 3: hammerdb (5 pods)
* DBMS Citus-1 - Experiment 2 Client 4: hammerdb (10 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 1 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 1 Client 3: hammerdb (5 pods)
* DBMS Citus-1 - Experiment 1 Client 4: hammerdb (10 pods)
* DBMS Citus-1 - Experiment 2 Client 1: hammerdb (1 pods)
* DBMS Citus-1 - Experiment 2 Client 2: hammerdb (2 pods)
* DBMS Citus-1 - Experiment 2 Client 3: hammerdb (5 pods)
* DBMS Citus-1 - Experiment 2 Client 4: hammerdb (10 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |  500 |      303.00 |           9.00 |            0.00 |        275.00 |           19.00 |              1 |         250 |             | None           |             0 | False         |             5940.59 | False               |
| Citus-1-2 |                2 |  500 |      303.00 |           9.00 |            0.00 |        275.00 |           19.00 |              1 |         250 |             | None           |             0 | False         |             5940.59 | True                |

### Benchmarking

#### Per Connection

| DBMS             | phase       | job           |   experiment_run |   vusers |   client |   benchmark_run |   child |   NOPM |     TPM |   efficiency |   duration |   errors |   P95 [ms] |   P99 [ms] |
|:-----------------|:------------|:--------------|-----------------:|---------:|---------:|----------------:|--------:|-------:|--------:|-------------:|-----------:|---------:|-----------:|-----------:|
| citus-1-1-1-1-1  | citus-1-1-1 | citus-1-1-1-1 |                1 |      250 |        1 |               1 |       1 | 766104 | 1761835 |         0.00 |         20 |        0 |      26.61 |      72.23 |
| citus-1-1-2-1-1  | citus-1-1-2 | citus-1-1-2-1 |                1 |      125 |        2 |               1 |       1 | 796884 | 1833144 |         0.00 |         20 |        0 |      26.83 |      68.26 |
| citus-1-1-2-1-2  | citus-1-1-2 | citus-1-1-2-1 |                1 |      125 |        2 |               1 |       2 | 796675 | 1832939 |         0.00 |         20 |        0 |      26.42 |      67.08 |
| citus-1-1-3-1-1  | citus-1-1-3 | citus-1-1-3-1 |                1 |       50 |        3 |               1 |       1 | 699152 | 1608433 |         0.00 |         20 |        0 |      27.69 |     108.50 |
| citus-1-1-3-1-2  | citus-1-1-3 | citus-1-1-3-1 |                1 |       50 |        3 |               1 |       2 | 699051 | 1607863 |         0.00 |         20 |        0 |      26.38 |      93.96 |
| citus-1-1-3-1-3  | citus-1-1-3 | citus-1-1-3-1 |                1 |       50 |        3 |               1 |       3 | 699037 | 1607886 |         0.00 |         20 |        0 |      27.81 |     100.60 |
| citus-1-1-3-1-4  | citus-1-1-3 | citus-1-1-3-1 |                1 |       50 |        3 |               1 |       4 | 699034 | 1607801 |         0.00 |         20 |        0 |      25.94 |      88.61 |
| citus-1-1-3-1-5  | citus-1-1-3 | citus-1-1-3-1 |                1 |       50 |        3 |               1 |       5 | 699034 | 1607971 |         0.00 |         20 |        0 |      26.75 |     104.62 |
| citus-1-1-4-1-1  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       1 | 686618 | 1579115 |         0.00 |         20 |        0 |      29.00 |      89.32 |
| citus-1-1-4-1-2  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       2 | 686424 | 1578865 |         0.00 |         20 |        0 |      27.50 |      96.84 |
| citus-1-1-4-1-3  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       3 | 686954 | 1579886 |         0.00 |         20 |        0 |      27.33 |      87.33 |
| citus-1-1-4-1-4  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       4 | 686920 | 1579791 |         0.00 |         20 |        0 |      26.62 |      84.04 |
| citus-1-1-4-1-5  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       5 | 686933 | 1579852 |         0.00 |         20 |        0 |      27.77 |      97.99 |
| citus-1-1-4-1-6  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       6 | 686891 | 1579691 |         0.00 |         20 |        0 |      28.62 |      78.45 |
| citus-1-1-4-1-7  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       7 | 686949 | 1579873 |         0.00 |         20 |        0 |      29.64 |      99.41 |
| citus-1-1-4-1-8  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       8 | 686932 | 1579824 |         0.00 |         20 |        0 |      26.74 |      91.15 |
| citus-1-1-4-1-9  | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |       9 | 686672 | 1579219 |         0.00 |         20 |        0 |      26.88 |      87.46 |
| citus-1-1-4-1-10 | citus-1-1-4 | citus-1-1-4-1 |                1 |       25 |        4 |               1 |      10 | 686535 | 1579013 |         0.00 |         20 |        0 |      27.57 |     101.39 |
| citus-1-2-1-1-1  | citus-1-2-1 | citus-1-2-1-1 |                2 |      250 |        1 |               1 |       1 | 714118 | 1643052 |         0.00 |         20 |        0 |      28.02 |      77.76 |
| citus-1-2-2-1-1  | citus-1-2-2 | citus-1-2-2-1 |                2 |      125 |        2 |               1 |       1 | 671164 | 1543652 |         0.00 |         20 |        0 |      29.59 |      79.13 |
| citus-1-2-2-1-2  | citus-1-2-2 | citus-1-2-2-1 |                2 |      125 |        2 |               1 |       2 | 671108 | 1543782 |         0.00 |         20 |        0 |      29.80 |      82.04 |
| citus-1-2-3-1-1  | citus-1-2-3 | citus-1-2-3-1 |                2 |       50 |        3 |               1 |       1 | 684123 | 1573653 |         0.00 |         20 |        0 |      30.89 |      75.73 |
| citus-1-2-3-1-2  | citus-1-2-3 | citus-1-2-3-1 |                2 |       50 |        3 |               1 |       2 | 684133 | 1573219 |         0.00 |         20 |        0 |      28.79 |      77.74 |
| citus-1-2-3-1-3  | citus-1-2-3 | citus-1-2-3-1 |                2 |       50 |        3 |               1 |       3 | 684043 | 1573487 |         0.00 |         20 |        0 |      29.56 |      67.55 |
| citus-1-2-3-1-4  | citus-1-2-3 | citus-1-2-3-1 |                2 |       50 |        3 |               1 |       4 | 684137 | 1573706 |         0.00 |         20 |        0 |      30.56 |      81.49 |
| citus-1-2-3-1-5  | citus-1-2-3 | citus-1-2-3-1 |                2 |       50 |        3 |               1 |       5 | 684125 | 1573653 |         0.00 |         20 |        0 |      30.02 |      73.10 |
| citus-1-2-4-1-1  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       1 | 706943 | 1625530 |         0.00 |         20 |        0 |      28.67 |      55.38 |
| citus-1-2-4-1-2  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       2 | 706864 | 1625926 |         0.00 |         20 |        0 |      31.45 |      61.93 |
| citus-1-2-4-1-3  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       3 | 706897 | 1625917 |         0.00 |         20 |        0 |      30.80 |      62.11 |
| citus-1-2-4-1-4  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       4 | 706956 | 1625579 |         0.00 |         20 |        0 |      30.05 |      60.58 |
| citus-1-2-4-1-5  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       5 | 706893 | 1625901 |         0.00 |         20 |        0 |      31.26 |      66.60 |
| citus-1-2-4-1-6  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       6 | 706887 | 1625598 |         0.00 |         20 |        0 |      28.80 |      56.12 |
| citus-1-2-4-1-7  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       7 | 706915 | 1625562 |         0.00 |         20 |        0 |      30.97 |      62.56 |
| citus-1-2-4-1-8  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       8 | 706866 | 1625899 |         0.00 |         20 |        0 |      30.12 |      58.45 |
| citus-1-2-4-1-9  | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |       9 | 706864 | 1625629 |         0.00 |         20 |        0 |      29.89 |      57.01 |
| citus-1-2-4-1-10 | citus-1-2-4 | citus-1-2-4-1 |                2 |       25 |        4 |               1 |      10 | 706891 | 1625920 |         0.00 |         20 |        0 |      30.52 |      58.40 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   vusers |   client |   benchmark_run |   pod_count |   P95 [ms] |   P99 [ms] |   efficiency |      NOPM |        TPM |   duration |   errors |
|:------------|:------------|-----------------:|---------:|---------:|----------------:|------------:|-----------:|-----------:|-------------:|----------:|-----------:|-----------:|---------:|
| citus-1-1-1 | citus-1-1-1 |                1 |      250 |        1 |               1 |           1 |      26.60 |      72.23 |         0.00 | 766104.00 | 1761835.00 |         20 |        0 |
| citus-1-1-2 | citus-1-1-2 |                1 |      250 |        2 |               1 |           2 |      26.83 |      68.26 |         0.00 | 796779.50 | 1833041.50 |         20 |        0 |
| citus-1-1-3 | citus-1-1-3 |                1 |      250 |        3 |               1 |           5 |      27.81 |     108.50 |         0.00 | 699061.60 | 1607990.80 |         20 |        0 |
| citus-1-1-4 | citus-1-1-4 |                1 |      250 |        4 |               1 |          10 |      29.64 |     101.39 |         0.00 | 686782.80 | 1579512.90 |         20 |        0 |
| citus-1-2-1 | citus-1-2-1 |                2 |      250 |        1 |               1 |           1 |      28.02 |      77.76 |         0.00 | 714118.00 | 1643052.00 |         20 |        0 |
| citus-1-2-2 | citus-1-2-2 |                2 |      250 |        2 |               1 |           2 |      29.80 |      82.04 |         0.00 | 671136.00 | 1543717.00 |         20 |        0 |
| citus-1-2-3 | citus-1-2-3 |                2 |      250 |        3 |               1 |           5 |      30.89 |      81.49 |         0.00 | 684112.20 | 1573543.60 |         20 |        0 |
| citus-1-2-4 | citus-1-2-4 |                2 |      250 |        4 |               1 |          10 |      31.45 |      66.60 |         0.00 | 706897.60 | 1625746.10 |         20 |        0 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |       766.00 |      6.04 |           1.56 |                  1.79 |
| citus-1-1-2-1 |       766.00 |      6.04 |           1.56 |                  1.79 |
| citus-1-1-3-1 |       766.00 |      6.04 |           1.56 |                  1.79 |
| citus-1-1-4-1 |       766.00 |      6.04 |           1.56 |                  1.79 |

### Loading phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      3506.15 |     24.60 |          47.53 |                117.45 |
| citus-1-1-2-1 |      3506.15 |     24.60 |          47.53 |                117.45 |
| citus-1-1-3-1 |      3506.15 |     24.60 |          47.53 |                117.45 |
| citus-1-1-4-1 |      3506.15 |     24.60 |          47.53 |                117.45 |

### Loading phase: component loader

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      7197.40 |     54.19 |           1.44 |                  1.44 |
| citus-1-1-2-1 |      7197.40 |     54.19 |           1.44 |                  1.44 |
| citus-1-1-3-1 |      7197.40 |     54.19 |           1.44 |                  1.44 |
| citus-1-1-4-1 |      7197.40 |     54.19 |           1.44 |                  1.44 |

### Benchmarking phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      5661.69 |      4.88 |           1.75 |                  1.97 |
| citus-1-1-2-1 |      6097.16 |      5.03 |           1.76 |                  1.98 |
| citus-1-1-3-1 |      4970.74 |      4.18 |           1.79 |                  2.00 |
| citus-1-1-4-1 |      5210.69 |      4.69 |           1.82 |                  2.03 |
| citus-1-2-1-1 |      5846.03 |      5.48 |           1.70 |                  1.73 |
| citus-1-2-2-1 |      5751.73 |      5.23 |           1.70 |                  1.74 |
| citus-1-2-3-1 |      6065.36 |      5.36 |           1.72 |                  1.76 |
| citus-1-2-4-1 |      6271.81 |      5.34 |           1.76 |                  1.80 |

### Benchmarking phase: component worker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |    152968.58 |    132.47 |          89.97 |                255.91 |
| citus-1-1-2-1 |    160046.25 |    132.21 |         109.00 |                255.88 |
| citus-1-1-3-1 |    147369.12 |    121.20 |         135.58 |                255.92 |
| citus-1-1-4-1 |    145625.27 |    125.92 |         166.98 |                255.90 |
| citus-1-2-1-1 |    154792.92 |    137.08 |          97.58 |                255.91 |
| citus-1-2-2-1 |    150053.45 |    132.09 |         144.98 |                255.93 |
| citus-1-2-3-1 |    152408.04 |    131.91 |         174.47 |                255.91 |
| citus-1-2-4-1 |    157399.23 |    134.65 |         203.21 |                255.94 |

### Benchmarking phase: component benchmarker

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| citus-1-1-1-1 |      6897.08 |      5.83 |           4.38 |                  4.39 |
| citus-1-1-2-1 |      8745.26 |      7.04 |           2.25 |                  2.26 |
| citus-1-1-3-1 |      9933.32 |      8.38 |           0.86 |                  0.87 |
| citus-1-1-4-1 |     10720.44 |      9.31 |           0.45 |                  0.45 |
| citus-1-2-1-1 |      6155.26 |      5.51 |           4.32 |                  4.32 |
| citus-1-2-2-1 |      7369.58 |      6.50 |           2.10 |                  2.10 |
| citus-1-2-3-1 |     10023.04 |      8.60 |           0.84 |                  0.84 |
| citus-1-2-4-1 |     11220.52 |      9.33 |           0.45 |                  0.45 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-1-1 (bexhoma-metrics-citus-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-2-1 (bexhoma-metrics-citus-1-1-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-3-1 (bexhoma-metrics-citus-1-1-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-1-4-1 (bexhoma-metrics-citus-1-1-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-1-1 (bexhoma-metrics-citus-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-2-1 (bexhoma-metrics-citus-1-2-2-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-3-1 (bexhoma-metrics-citus-1-2-3-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection citus-1-2-4-1 (bexhoma-metrics-citus-1-2-4-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: NOPM contains no 0 or NaN
* TEST skipped: efficiency (not computed: needs key-and-think time (-xkey))
* TEST passed: Workflow as planned
```

</details>


## TPC-H

We build the schema similar to [2] in https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/experiments/tpch/Citus/initschema-tpch.sql

```sql
select create_reference_table('nation');
select create_reference_table('region');
select create_reference_table('part');
select create_reference_table('supplier');
select create_reference_table('partsupp');
select create_reference_table('customer');
select create_distributed_table('orders', 'o_orderkey');
select create_distributed_table('lineitem', 'l_orderkey');
```

It is also mentioned in [1] that the big tables `orders` and `linetime` should be distributed and the others should be replicated.
As the paper used Citus 9.5, columnar storage has not been included in Citus [3].
Note that columnar storage has some limitations as no UPDATEs, no DELETEs and no FOREIGN KEYs.
Also note that Citus does not support all TPC-H queries.
In a correlated subquery there cannot be a replicated table, so we have to rewrite Q22.

[1] [Citus: Distributed PostgreSQL for Data-Intensive Applications](https://dl.acm.org/doi/10.1145/3448016.3457551)
> Umur Cubukcu, Ozgun Erdogan, Sumedh Pathak, Sudhakar Sannakkayala, and Marco Slot.
> 2021. In Proceedings of the 2021 International Conference on Management of Data (SIGMOD '21).
> Association for Computing Machinery, New York, NY, USA, 2490â€“2502.
> https://dl.acm.org/doi/10.1145/3448016.3457551

[2] [Citus TPC-H tests - schema](https://github.com/dimitri/tpch-citus/tree/master/schema)
> Dimitri Fontaine.
> Retrieved April 1, 2025, from https://github.com/dimitri/tpch-citus/tree/master/schema

[3] [Citus columnar storage](https://docs.citusdata.com/en/stable/admin_guide/table_management.html#columnar-storage)
> Citus Data.
> Retrieved April 1, 2025, from https://docs.citusdata.com/en/stable/admin_guide/table_management.html#columnar-storage


### TPC-H Simple Example


```bash
bexhoma tpch \
  -dbms Citus \
  -sf 1 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_tpch_citus_1.log
```


### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_citus_1_summary.md" target="_blank" rel="noopener">docs_tpch_citus_1.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=1
* Type: tpch
* Duration: 1010s 
* Code: 1792873983
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=1) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 1200.
  * Data transfer volume per query is also measured.
  * Import sets indexes, constraints, statistics recomputation after loading.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.8.
  * Experiment is limited to DBMS ['Citus'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29, cl-worker39.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 4 worker nodes, 1 replicas and 48 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* citus-1-1-1-1-1 uses docker image citusdata/citus:14.2.0
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:665682
  * datadisk:58
  * volume_size:1.8T
  * volume_used:651G
  * cpu_list:0-223
  * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:520542
    * datadisk:1596
    * volume_size:879G
    * volume_used:509G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 1
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:334061
    * datadisk:1596
    * volume_size:439G
    * volume_used:327G
    * cpu_list:0-255
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 2
    * RAM:2164173172736
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-137-generic
    * node:cl-worker36
    * disk:665682
    * datadisk:1595
    * volume_size:1.8T
    * volume_used:651G
    * cpu_list:0-223
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * worker 3
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:492389
    * datadisk:1595
    * volume_size:1.8T
    * volume_used:481G
    * cpu_list:0-127
    * args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'plan_cache_mode=force_custom_plan', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
  * resources_total: 20.0 CPU, 320.0 GiB RAM requested in 5 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
    * worker: 4 x, 16.0 CPU, 256.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792873983
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_SHARDS:48
    * BEXHOMA_WORKERS:4
    * COLUMNAR:False

### SUT Container Restarts
* bexhoma-sut-citus-1-1792873983-58f54cb579-mkgt6: 0
* bexhoma-worker-citus-tpch-1-0: 0
* bexhoma-worker-citus-tpch-1-1: 0
* bexhoma-worker-citus-tpch-1-2: 0
* bexhoma-worker-citus-tpch-1-3: 0

### Workflow

#### Actual

* DBMS Citus-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS Citus-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|           |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] | loading_inherited   |
|:----------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|:--------------------|
| Citus-1-1 |                1 |    1 |       75.00 |           6.00 |           22.00 |         13.00 |           29.00 |              8 |           0 |             | None           |             0 | False         |               48.00 | False               |

### Benchmarking

#### Per Connection

| DBMS            | configuration   | phase       | job           |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod             |
|:----------------|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:----------------|
| citus-1-1-1-1-1 | Citus-1         | citus-1-1-1 | citus-1-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.22 |            16890.81 |           5657.14 |          -1 | citus-1-1-1-1-1 |

#### Per Phase

|             | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   SF |   num_of_queries |   num_of_executions |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|-----:|-----------------:|--------------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| citus-1-1-1 | citus-1-1-1 |                1 |        1 |               1 |           1 | 1.00 |               22 |                  22 |         14 |            0.22 |            16890.81 |           5657.14 |          -1 |

#### Query Completion per Phase

| phase       |   pods | Pricing Summary Report (TPC-H Q1)   | Minimum Cost Supplier Query (TPC-H Q2)   | Shipping Priority (TPC-H Q3)   | Order Priority Checking Query (TPC-H Q4)   | Local Supplier Volume (TPC-H Q5)   | Forecasting Revenue Change (TPC-H Q6)   | Volume Shipping Query (TPC-H Q7)   | National Market Share (TPC-H Q8)   | Product Type Profit Measure (TPC-H Q9)   | Returned Item Reporting Query (TPC-H Q10)   | Important Stock Identification (TPC-H Q11)   | Shipping Modes and Order Priority (TPC-H Q12)   | Customer Distribution (TPC-H Q13)   | Promotion Effect Query (TPC-H Q14)   | Top Supplier Query (TPC-H Q15)   | Parts/Supplier Relationship (TPC-H Q16)   | Small-Quantity-Order Revenue (TPC-H Q17)   | Large Volume Customer (TPC-H Q18)   | Discounted Revenue (TPC-H Q19)   | Potential Part Promotion (TPC-H Q20)   | Suppliers Who Kept Orders Waiting Query (TPC-H Q21)   | Global Sales Opportunity Query (TPC-H Q22)   | complete   |
|:------------|-------:|:------------------------------------|:-----------------------------------------|:-------------------------------|:-------------------------------------------|:-----------------------------------|:----------------------------------------|:-----------------------------------|:-----------------------------------|:-----------------------------------------|:--------------------------------------------|:---------------------------------------------|:------------------------------------------------|:------------------------------------|:-------------------------------------|:---------------------------------|:------------------------------------------|:-------------------------------------------|:------------------------------------|:---------------------------------|:---------------------------------------|:------------------------------------------------------|:---------------------------------------------|:-----------|
| citus-1-1-1 |      1 | 1/1                                 | 1/1                                      | 1/1                            | 1/1                                        | 1/1                                | 1/1                                     | 1/1                                | 1/1                                | 1/1                                      | 1/1                                         | 1/1                                          | 1/1                                             | 1/1                                 | 1/1                                  | 1/1                              | 1/1                                       | 1/1                                        | 1/1                                 | 1/1                              | 1/1                                    | 1/1                                                   | 1/1                                          | yes        |

Pods that completed each query, out of the pods the phase ran (`completed/pods`). Counted per phase, so a failure in one phase does not change another phase's row. `complete` = every pod completed every active query.

### Latency of Timer Execution [ms]
| Queries                                             |   citus-1-1-1-1-1 |
|:----------------------------------------------------|------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            211.22 |
| Minimum Cost Supplier Query (TPC-H Q2)              |            320.19 |
| Shipping Priority (TPC-H Q3)                        |            147.55 |
| Order Priority Checking Query (TPC-H Q4)            |             82.57 |
| Local Supplier Volume (TPC-H Q5)                    |            126.76 |
| Forecasting Revenue Change (TPC-H Q6)               |             68.79 |
| Volume Shipping Query (TPC-H Q7)                    |            137.38 |
| National Market Share (TPC-H Q8)                    |            134.27 |
| Product Type Profit Measure (TPC-H Q9)              |            286.56 |
| Returned Item Reporting Query (TPC-H Q10)           |            159.20 |
| Important Stock Identification (TPC-H Q11)          |             96.80 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            119.60 |
| Customer Distribution (TPC-H Q13)                   |            612.52 |
| Promotion Effect Query (TPC-H Q14)                  |             98.09 |
| Top Supplier Query (TPC-H Q15)                      |            155.18 |
| Parts/Supplier Relationship (TPC-H Q16)             |            356.75 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |           2457.92 |
| Large Volume Customer (TPC-H Q18)                   |            172.32 |
| Discounted Revenue (TPC-H Q19)                      |            125.53 |
| Potential Part Promotion (TPC-H Q20)                |           1535.38 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |            124.87 |
| Global Sales Opportunity Query (TPC-H Q22)          |            716.05 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: All active queries counted in the totals
* TEST skipped: EXPLAIN captured for every active query (-se/--store-explain not used)
* TEST passed: Workflow as planned
```

</details>

### TPC-H More Complex Example

We run TPC-H Power Test at SF=10.
Possibly existing PVCs of the workers are removed before loading (`-rsr`).
Note that this takes a lot of disk space including for indexes.

```bash
bexhoma tpch \
  -dbms Citus \
  -sf 10 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xii -xic -xis \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -tr \
  -rsr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_tpch_citus_2.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_citus_2_summary.md" target="_blank" rel="noopener">docs_tpch_citus_2.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 1891s 
    Code: 1771346573
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Import sets indexes and constraints after loading and recomputes statistics.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-8-1-1-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891932
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360193
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:405675
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:556344
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771346573
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891933
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360193
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:405675
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:556344
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771346573
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:407685
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891857
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360194
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:558495
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771346573
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:407792
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891857
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360195
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:558495
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771346573
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:False

### Errors (failed queries)
No errors

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                                 Citus-BHT-8-1-1-1  Citus-BHT-8-1-2-1  Citus-BHT-8-2-1-1  Citus-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                               146.40             132.92            1015.53             134.61
Minimum Cost Supplier Query (TPC-H Q2)                           15.44              13.73             822.44              17.55
Shipping Priority (TPC-H Q3)                                     33.77              34.58             457.77              33.34
Order Priority Checking Query (TPC-H Q4)                         14.07              12.12              30.72              12.26
Local Supplier Volume (TPC-H Q5)                                 61.25              60.20              91.65              45.73
Forecasting Revenue Change (TPC-H Q6)                            12.00              11.07              12.90              11.64
Forecasting Revenue Change (TPC-H Q7)                            44.10              61.19              61.55              44.29
National Market Share (TPC-H Q8)                                 57.80              67.23              90.10              56.14
Product Type Profit Measure (TPC-H Q9)                           47.01              62.14              74.44              46.62
Forecasting Revenue Change (TPC-H Q10)                           25.28              25.60              25.75              24.72
Important Stock Identification (TPC-H Q11)                        4.43               4.40               4.90               4.49
Shipping Modes and Order Priority (TPC-H Q12)                    17.29              16.70              17.11              16.72
Customer Distribution (TPC-H Q13)                                25.00              34.63              40.37              25.69
Forecasting Revenue Change (TPC-H Q14)                           13.73              13.55              13.49              13.89
Top Supplier Query (TPC-H Q15)                                  126.00              44.52             105.02              35.50
Parts/Supplier Relationship (TPC-H Q16)                           3.45               3.33               3.50               2.98
Small-Quantity-Order Revenue (TPC-H Q17)                         46.28              52.84              41.66              40.03
Large Volume Customer (TPC-H Q18)                                25.17              26.02              25.08              24.90
Discounted Revenue (TPC-H Q19)                                   23.77              23.41              24.10              23.10
Potential Part Promotion (TPC-H Q20)                             88.03             133.04             124.29              39.75
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)              37.93              37.20              30.66              36.50
Global Sales Opportunity Query (TPC-H Q22)                       74.58              31.31              56.44              25.73

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1          16.0           23.0         3.0      111.0     159.0
Citus-BHT-8-1-2-1          16.0           23.0         3.0      111.0     159.0
Citus-BHT-8-2-1-1          16.0           23.0         3.0      111.0     159.0
Citus-BHT-8-2-2-1          16.0           23.0         3.0      111.0     159.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1           0.03
Citus-BHT-8-1-2-1           0.03
Citus-BHT-8-2-1-1           0.05
Citus-BHT-8-2-2-1           0.02

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1         1228092.71
Citus-BHT-8-1-2-1         1273426.74
Citus-BHT-8-2-1-1          739130.20
Citus-BHT-8-2-2-1         1470456.52

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
Citus-BHT-8-1-1 10.0 1              1                  3      1  10.0         264000.0
Citus-BHT-8-1-2 10.0 1              2                  2      1  10.0         396000.0
Citus-BHT-8-2-1 10.0 2              1                  5      1  10.0         158400.0
Citus-BHT-8-2-2 10.0 2              2                  2      1  10.0         396000.0

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
Citus-BHT-8-1-1-1  Citus-BHT-8-1-1  10.0     8               1           1       1771347406     1771347409
Citus-BHT-8-1-2-1  Citus-BHT-8-1-2  10.0     8               1           2       1771347499     1771347501
Citus-BHT-8-2-1-1  Citus-BHT-8-2-1  10.0     8               2           1       1771348297     1771348302
Citus-BHT-8-2-2-1  Citus-BHT-8-2-2  10.0     8               2           2       1771348409     1771348411

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1           0        0           0.0                  0.0
Citus-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1         0.0     0.02          0.53                 0.59
Citus-BHT-8-1-2         0.0     0.01          0.53                 0.58
Citus-BHT-8-2-1         0.0     0.00          0.51                 0.83
Citus-BHT-8-2-2         0.0     0.00          0.51                 0.96

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1         0.0      0.0           0.0                  0.0
Citus-BHT-8-1-2         0.0      0.0           0.0                  0.0
Citus-BHT-8-2-1         0.0      0.0           0.0                  0.0
Citus-BHT-8-2-2         0.0      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST passed: No SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```

</details>


### TPC-H Test Columnar Storage

Citus provides the option to make a table using columnar storage via `USING COLUMNAR`.
For Bexhoma's TPC-H, you can activate makeing the distributed tables `orders` and `lineitem` use columnar storage via `-xcol`.
Note that this also means there will be no foreign key constraints and no indexes on these tables.

Possibly existing PVCs of the workers are removed before loading (`-rsr`).

The experiment runs like this:

```bash
bexhoma tpch \
  -dbms Citus \
  -sf 10 \
  -nc 2 \
  -ne 1,1 \
  -nlp 8 \
  -nbp 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xcol \
  -xdt \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -t 14400 \
  -tr \
  -rsr \
  -rss 50Gi \
  -lr 64Gi \
  -rr 64Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -rnw $BEXHOMA_NODES_WORKER_4 \
  run &>$LOG_DIR/docs_tpch_citus_3.log
```

### Evaluate Results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_tpch_citus_3_summary.md" target="_blank" rel="noopener">docs_tpch_citus_3.log</a></summary>

```markdown
## Show Summary

### Workload
TPC-H Queries SF=10
    Type: tpch
    Duration: 1898s 
    Code: 1771348585
    This includes the reading queries of TPC-H.
    This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
    TPC-H (SF=10) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q22.
    All instances use the same query parameters.
    Timeout per query is 14400.
    Experiment uses bexhoma version 0.8.20.
    System metrics are monitored by a cluster-wide installation.
    Experiment is limited to DBMS ['Citus'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker14.
    Database is persisted to disk of type shared and size 50Gi.
    Loading is tested with [1] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1] times the number of benchmarking pods.
    Experiment is run 2 times.

### Connections
Citus-BHT-8-1-1-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:407742
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891874
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360198
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:558495
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771348585
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-1-2-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:407742
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891871
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360198
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:558495
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771348585
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-1-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:409919
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891866
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360190
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:560646
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771348585
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True
Citus-BHT-8-2-2-1 uses docker image citusdata/citus:13.2.0-alpine
    RAM:541008474112
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-164-generic
    node:cl-worker14
    disk:98902
    volume_size:50.0G
    volume_used:40.0M
    cpu_list:0-63
    args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    requests_cpu:4
    requests_memory:16Gi
    worker 0
        RAM:540579303424
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-94-generic
        node:cl-worker22
        disk:409940
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 1
        RAM:2164173176832
        CPU:INTEL(R) XEON(R) PLATINUM 8570
        Cores:224
        host:6.8.0-90-generic
        node:cl-worker36
        disk:891866
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-223
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 2
        RAM:1077382688768
        CPU:AMD EPYC 7742 64-Core Processor
        Cores:256
        host:6.8.0-1044-nvidia
        node:cl-worker28
        disk:1360191
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-255
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    worker 3
        RAM:1081742745600
        CPU:AMD EPYC 7502 32-Core Processor
        Cores:128
        host:6.8.0-90-generic
        node:cl-worker29
        disk:560646
        volume_size:50.0G
        volume_used:40.0M
        cpu_list:0-127
        args:['-c', 'max_worker_processes=16', '-c', 'max_parallel_workers=16', '-c', 'max_parallel_workers_per_gather=8', '-c', 'max_parallel_maintenance_workers=4', '-c', 'max_wal_size=32GB', '-c', 'shared_buffers=16GB', '-c', 'max_connections=1024', '-c', 'autovacuum_max_workers=10', '-c', 'autovacuum_vacuum_cost_limit=3000', '-c', 'vacuum_cost_limit=1000', '-c', 'checkpoint_completion_target=0.9', '-c', 'cpu_tuple_cost=0.03', '-c', 'effective_cache_size=32GB', '-c', 'maintenance_work_mem=512MB', '-c', 'wal_buffers=64MB', '-c', 'work_mem=64MB', '-c', 'temp_buffers=64MB', '-c', 'autovacuum_work_mem=-1', '-c', 'max_stack_depth=4MB', '-c', 'max_files_per_process=4000', '-c', 'effective_io_concurrency=32', '-c', 'wal_level=replica', '-c', 'max_wal_senders=8', '-c', 'synchronous_commit=local', '-c', 'checkpoint_timeout=1h', '-c', 'checkpoint_warning=0', '-c', 'autovacuum=on', '-c', 'max_locks_per_transaction=64', '-c', 'max_pred_locks_per_transaction=64', '-c', 'default_statistics_target=500', '-c', 'random_page_cost=1.1']
    eval_parameters
        code:1771348585
        BEXHOMA_REPLICAS:1
        BEXHOMA_SHARDS:48
        BEXHOMA_WORKERS:4
        COLUMNAR:True

### Errors (failed queries)
                                                     Citus-BHT-8-1-1-1  Citus-BHT-8-1-2-1  Citus-BHT-8-2-1-1  Citus-BHT-8-2-2-1
Pricing Summary Report (TPC-H Q1)                                 True               True               True               True
Shipping Priority (TPC-H Q3)                                      True               True               True               True
Order Priority Checking Query (TPC-H Q4)                          True               True               True               True
Local Supplier Volume (TPC-H Q5)                                  True               True               True               True
Forecasting Revenue Change (TPC-H Q6)                             True               True               True               True
Forecasting Revenue Change (TPC-H Q7)                             True               True               True               True
National Market Share (TPC-H Q8)                                  True               True               True               True
Product Type Profit Measure (TPC-H Q9)                            True               True               True               True
Forecasting Revenue Change (TPC-H Q10)                            True               True               True               True
Shipping Modes and Order Priority (TPC-H Q12)                     True               True               True               True
Customer Distribution (TPC-H Q13)                                 True               True               True               True
Forecasting Revenue Change (TPC-H Q14)                            True               True               True               True
Top Supplier Query (TPC-H Q15)                                    True               True               True               True
Small-Quantity-Order Revenue (TPC-H Q17)                          True               True               True               True
Large Volume Customer (TPC-H Q18)                                 True               True               True               True
Discounted Revenue (TPC-H Q19)                                    True               True               True               True
Potential Part Promotion (TPC-H Q20)                              True               True               True               True
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)               True               True               True               True
Global Sales Opportunity Query (TPC-H Q22)                        True               True               True               True
Pricing Summary Report (TPC-H Q1)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 357
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 357
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 357
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 357
Shipping Priority (TPC-H Q3)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 111
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 111
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 111
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 111
Order Priority Checking Query (TPC-H Q4)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 54
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 54
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 54
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 54
Local Supplier Volume (TPC-H Q5)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 82
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 82
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 82
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 82
Forecasting Revenue Change (TPC-H Q6)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 56
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 56
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 56
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 56
Forecasting Revenue Change (TPC-H Q7)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 245
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 245
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 245
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 245
National Market Share (TPC-H Q8)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 289
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 289
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 289
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 289
Product Type Profit Measure (TPC-H Q9)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 231
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 231
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 231
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 231
Forecasting Revenue Change (TPC-H Q10)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 169
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 169
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 169
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 169
Shipping Modes and Order Priority (TPC-H Q12)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 256
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 256
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 256
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 256
Customer Distribution (TPC-H Q13)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 129
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 129
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 129
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 129
Forecasting Revenue Change (TPC-H Q14)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 164
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 164
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 164
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 164
Top Supplier Query (TPC-H Q15)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 109
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 109
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 109
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 109
Small-Quantity-Order Revenue (TPC-H Q17)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 57
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 57
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 57
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 57
Large Volume Customer (TPC-H Q18)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 123
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 123
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 123
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 123
Discounted Revenue (TPC-H Q19)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 65
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 65
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 65
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 65
Potential Part Promotion (TPC-H Q20)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 82
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 82
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 82
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 82
Suppliers Who Kept Orders Waiting Query (TPC-H Q21)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 51
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 51
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 51
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "lineitem" does not exist
  Position: 51
Global Sales Opportunity Query (TPC-H Q22)
Citus-BHT-8-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 394
Citus-BHT-8-2-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 394
Citus-BHT-8-2-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 394
Citus-BHT-8-1-2-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: relation "orders" does not exist
  Position: 394

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
DBMS                                        Citus-BHT-8-1-1-1  Citus-BHT-8-1-2-1  Citus-BHT-8-2-1-1  Citus-BHT-8-2-2-1
Minimum Cost Supplier Query (TPC-H Q2)                  67.25              63.76            1159.86              63.86
Important Stock Identification (TPC-H Q11)               6.74               6.19               9.10               6.39
Parts/Supplier Relationship (TPC-H Q16)                  6.41               6.56               7.21               6.88

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
Citus-BHT-8-1-1-1          16.0           23.0         2.0       74.0     118.0
Citus-BHT-8-1-2-1          16.0           23.0         2.0       74.0     118.0
Citus-BHT-8-2-1-1          16.0           23.0         2.0       74.0     118.0
Citus-BHT-8-2-2-1          16.0           23.0         2.0       74.0     118.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
Citus-BHT-8-1-1-1           0.01
Citus-BHT-8-1-2-1           0.01
Citus-BHT-8-2-1-1           0.04
Citus-BHT-8-2-2-1           0.01

### Power@Size ((3600*SF)/(geo times))
                   Power@Size [~Q/h]
DBMS                                
Citus-BHT-8-1-1-1         2523050.45
Citus-BHT-8-1-2-1         2621727.57
Citus-BHT-8-2-1-1          849706.81
Citus-BHT-8-2-2-1         2552136.17

### Throughput@Size ((runs*queries*streams*3600*SF)/(span of time))
                                                time [s]  count    SF  Throughput@Size
DBMS            SF   num_experiment num_client                                        
Citus-BHT-8-1-1 10.0 1              1                  2      1  10.0          54000.0
Citus-BHT-8-1-2 10.0 1              2                  2      1  10.0          54000.0
Citus-BHT-8-2-1 10.0 2              1                  3      1  10.0          36000.0
Citus-BHT-8-2-2 10.0 2              2                  1      1  10.0         108000.0

### Workflow
                         orig_name    SF  pods  num_experiment  num_client  benchmark_start  benchmark_end
Citus-BHT-8-1-1-1  Citus-BHT-8-1-1  10.0     8               1           1       1771349410     1771349412
Citus-BHT-8-1-2-1  Citus-BHT-8-1-2  10.0     8               1           2       1771349509     1771349511
Citus-BHT-8-2-1-1  Citus-BHT-8-2-1  10.0     8               2           1       1771350299     1771350302
Citus-BHT-8-2-2-1  Citus-BHT-8-2-2  10.0     8               2           2       1771350402     1771350403

#### Actual
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

#### Planned
DBMS Citus-BHT-8 - Pods [[1, 1], [1, 1]]

### Ingestion - Loader
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1           0        0           0.0                  0.0
Citus-BHT-8-1-2           0        0           0.0                  0.0

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1         0.0     0.02          0.53                 0.58
Citus-BHT-8-1-2         0.0     0.00          0.53                 0.58
Citus-BHT-8-2-1         0.0     0.01          0.51                 0.83
Citus-BHT-8-2-2         0.0     0.00          0.51                 0.91

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
Citus-BHT-8-1-1         0.0      0.0           0.0                  0.0
Citus-BHT-8-1-2         0.0      0.0           0.0                  0.0
Citus-BHT-8-2-1         0.0      0.0           0.0                  0.0
Citus-BHT-8-2-2         0.0      0.0           0.0                  0.0

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size contains no 0 or NaN
TEST failed: SQL errors
TEST passed: No SQL warnings
TEST passed: Workflow as planned
TEST failed: Ingestion Loader contains 0 or NaN in CPU [CPUs]
TEST failed: Execution SUT contains 0 or NaN in CPU [CPUs]
TEST failed: Execution Benchmarker contains 0 or NaN in CPU [CPUs]
```

</details>





