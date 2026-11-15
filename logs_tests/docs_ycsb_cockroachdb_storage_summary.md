## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 901s 
* Code: 1794697142
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['CockroachDB'].
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
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1076544
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2077
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662475
    * datadisk:1741
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1076544
    * datadisk:1741
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-223
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697142
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-2-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1078020
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:662333
    * datadisk:2075
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1381310
    * datadisk:2075
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
  * worker 2
    * RAM:2164173156352
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:1078069
    * datadisk:2146
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-223
  * worker 3
    * node:cl-worker39
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794697142
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CockroachDB-1-2

### Data Parameters of Reused Volumes
* CockroachDB-1: DDL values of the volume: num_worker_replicas=3, pk_hash=hash, bucket_count=default, range_max_bytes=default, column_families=one, pre_split=none
* CockroachDB-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794697142-65f89f577f-479tw: 0
* bx-w-cr-nvme-ycsb-1-0: 0
* bx-w-cr-nvme-ycsb-1-1: 0
* bx-w-cr-nvme-ycsb-1-2: 0
* bexhoma-sut-cockroachdb-1-1794697142-795d64bf77-8km5r: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1769.64 |                70636.00 |            125000.00 |                             11071.00 | 1.00 |               50.97 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1782.81 |                70114.00 |            125000.00 |                             11391.00 | 1.00 |               51.34 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1786.35 |                69975.00 |            125000.00 |                             11375.00 | 1.00 |               51.45 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1771.64 |                70556.00 |            125000.00 |                             11463.00 | 1.00 |               51.02 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1773.33 |                70489.00 |            125000.00 |                             11415.00 | 1.00 |               51.07 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1769.03 |                70660.00 |            125000.00 |                             11279.00 | 1.00 |               50.95 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1782.33 |                70133.00 |            125000.00 |                             11015.00 | 1.00 |               51.33 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1768.88 |                70666.00 |            125000.00 |                             11399.00 | 1.00 |               50.94 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               50.94 |                        14204.02 |                70666.00 |           1000000.00 |                             11301.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    65536 |        0 |                        11327.08 |                88284.00 |             499380 |                            7063.00 |               500620 |                            167935.00 |
| cockroachdb-1-2-1-1-1 | cockroachdb-1-2-1 | cockroachdb-1-2-1-1 |                2 |        1 |               1 |       1 |        64 |    65536 |        0 |                        10252.20 |                97540.00 |             500159 |                            7275.00 |               499841 |                            187647.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    65536 |        0 |                        11327.08 |                88284.00 |             499380 |                            7063.00 |               500620 |                            167935.00 |
| cockroachdb-1-2-1 | cockroachdb-1-2-1 |                2 |        1 |               1 |           1 |        64 |    65536 |        0 |                        10252.20 |                97540.00 |             500159 |                            7275.00 |               499841 |                            187647.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2024.87 |     33.09 |           5.69 |                  9.52 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       112.68 |      1.86 |           0.10 |                  0.10 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |      2161.31 |     27.99 |           7.47 |                 12.26 |
| cockroachdb-1-2-1-1 |      1754.17 |     23.92 |           5.31 |                  9.91 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |        65.76 |      1.40 |           0.32 |                  0.32 |
| cockroachdb-1-2-1-1 |        62.36 |      0.75 |           0.31 |                  0.31 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-2-1-1 (bexhoma-metrics-cockroachdb-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
