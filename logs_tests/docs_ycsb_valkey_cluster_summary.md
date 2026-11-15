## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 432s 
* Code: 1794678269
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Valkey'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* valkey-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1039920
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:660447
    * datadisk:721
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1382897
    * datadisk:805
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:860283
    * datadisk:713
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794678269
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Valkey-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-valkey-1-1794678269-55bbb94f59-5fhtb: 0
* bx-w-valkey-1-1794678269-0: 0
* bx-w-valkey-1-1794678269-1: 0
* bx-w-valkey-1-1794678269-2: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4153.51 |                30095.00 |            125000.00 |                              3661.00 | 1.00 |              119.62 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4197.03 |                29783.00 |            125000.00 |                              3641.00 | 1.00 |              120.87 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4163.06 |                30026.00 |            125000.00 |                              3651.00 | 1.00 |              119.90 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4143.33 |                30169.00 |            125000.00 |                              3667.00 | 1.00 |              119.33 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4195.90 |                29791.00 |            125000.00 |                              3665.00 | 1.00 |              120.84 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4167.78 |                29992.00 |            125000.00 |                              3633.00 | 1.00 |              120.03 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4150.20 |                30119.00 |            125000.00 |                              3653.00 | 1.00 |              119.53 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         4159.60 |                30051.00 |            125000.00 |                              3647.00 | 1.00 |              119.80 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              119.33 |                        33330.40 |                30169.00 |           1000000.00 |                              3652.25 |

### Benchmarking

#### Per Connection

| connection       | phase        | job            |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62192.15 |               160792.00 |            4999047 |                            1203.00 |              5000953 |                              1192.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62192.15 |               160792.00 |            4999047 |                            1203.00 |              5000953 |                              1192.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       105.90 |      2.53 |           1.47 |                  1.47 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.31 |                  0.32 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       275.92 |      2.36 |           1.51 |                  1.52 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       671.49 |      4.99 |           1.49 |                  1.49 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection valkey-1-1-1-1 (bexhoma-metrics-valkey-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: component worker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
