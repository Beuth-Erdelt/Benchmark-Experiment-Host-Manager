## Show Summary

### Workload
YCSB SF=10
* Type: ycsb
* Duration: 10989s 
* Code: 1792333677
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 10000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Experiment uses bexhoma version 0.11.6.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173172736
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:854127
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540590800896
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker24
    * disk:151647
    * datadisk:700899
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-95
  * worker 1
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:681817
    * datadisk:700833
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * worker 2
    * RAM:540579299328
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:252912
    * datadisk:700827
    * volume_size:1000G
    * volume_used:674G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * eval_parameters
    * code:1792333677
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1792333677-f67bb46db-7vp4q: 0
* bexhoma-worker-cockroachdb-ycsb-10-0: 0
* bexhoma-worker-cockroachdb-ycsb-10-1: 0
* bexhoma-worker-cockroachdb-ycsb-10-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |    sf |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|------:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          376.60 |              3319210.00 |           1250000.00 |                            155007.00 | 10.00 |               10.85 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.86 |              3425973.00 |           1250000.00 |                            155903.00 | 10.00 |               10.51 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          366.02 |              3415155.00 |           1250000.00 |                            155775.00 | 10.00 |               10.54 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          376.27 |              3322086.00 |           1250000.00 |                            154751.00 | 10.00 |               10.84 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.05 |              3433639.00 |           1250000.00 |                            155903.00 | 10.00 |               10.48 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          364.71 |              3427389.00 |           1250000.00 |                            155263.00 | 10.00 |               10.50 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          363.76 |              3436320.00 |           1250000.00 |                            156543.00 | 10.00 |               10.48 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                          366.15 |              3413939.00 |           1250000.00 |                            155647.00 | 10.00 |               10.55 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   exceptions |    sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|------:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 10.00 |               10.48 |                         2942.40 |              3436320.00 |          10000000.00 |                            155599.00 |

### Benchmarking

#### Per Connection

| DBMS                  | phase             | job                 | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 | CockroachDB-1   |                1 |        1 |               1 |       1 |        64 |    65536 |           1 |            0 |                         1635.69 |              6113623.00 |            5002464 |                           36703.00 |              4997536 |                           1948671.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        64 |    65536 |               1 |           1 |            0 |                         1635.69 |              6113623.00 |            5002464 |                           36703.00 |              4997536 |                           1948671.00 |

### Monitoring

### Loading phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     29067.12 |     22.25 |          19.25 |                 47.99 |

### Loading phase: component loader

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       901.87 |      1.45 |           0.12 |                  0.13 |

### Benchmarking phase: component worker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |     35013.89 |      8.06 |          22.06 |                 47.99 |

### Benchmarking phase: component benchmarker

| DBMS                |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------------|-------------:|----------:|---------------:|----------------------:|
| cockroachdb-1-1-1-1 |       782.26 |      0.56 |           0.24 |                  0.24 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cockroachdb-1-1-1-1 (bexhoma-metrics-cockroachdb-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                    12891.76 |             17774623.27 |                              0.00 |                                      0.00 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                |   Raft Messages Received (AppResp) [msgs/s] |   Raft Network In [B/s] |   Raft Recovery Snapshot In [B/s] |   Replicate Queue Adds Attempted [adds/s] |   Replicate Queue Purgatory Count |
|:--------------------|--------------------------------------------:|------------------------:|----------------------------------:|------------------------------------------:|----------------------------------:|
| cockroachdb-1-1-1-1 |                                     4374.27 |              3165371.58 |                              0.00 |                                      0.00 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
