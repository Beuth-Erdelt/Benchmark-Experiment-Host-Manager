## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 398s 
* Code: 1793489406
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
  * Experiment uses bexhoma version 0.11.11.
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
  * disk:755824
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:755825
    * datadisk:722
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:553083
    * datadisk:803
    * cpu_list:0-127
  * worker 2
    * RAM:1081649795072
    * CPU:AMD EPYC 7453 28-Core Processor
    * Cores:56
    * host:6.8.0-139-generic
    * node:cl-worker34
    * disk:2200343
    * datadisk:714
    * cpu_list:0-55
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793489406
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Valkey-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-valkey-1-1793489406-768c6865bf-p5vk7: 0
* bx-w-valkey-1-1793489406-0: 0
* bx-w-valkey-1-1793489406-1: 0
* bx-w-valkey-1-1793489406-2: 0

### Workflow

#### Actual

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Valkey-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| valkey-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5303.58 |                23569.00 |            125000.00 |                              4299.00 | 1.00 |              152.74 |
| valkey-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5417.35 |                23074.00 |            125000.00 |                              4279.00 | 1.00 |              156.02 |
| valkey-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5353.32 |                23350.00 |            125000.00 |                              4271.00 | 1.00 |              154.18 |
| valkey-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5329.35 |                23455.00 |            125000.00 |                              4303.00 | 1.00 |              153.49 |
| valkey-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5374.96 |                23256.00 |            125000.00 |                              4255.00 | 1.00 |              154.80 |
| valkey-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5374.96 |                23256.00 |            125000.00 |                              4351.00 | 1.00 |              154.80 |
| valkey-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5316.21 |                23513.00 |            125000.00 |                              4299.00 | 1.00 |              153.11 |
| valkey-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         5347.82 |                23374.00 |            125000.00 |                              4335.00 | 1.00 |              154.02 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Valkey-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              152.74 |                        42817.55 |                23569.00 |           1000000.00 |                              4299.00 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1-1-1 | valkey-1-1-1 | valkey-1-1-1-1 | Valkey-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61921.42 |               161495.00 |            5003173 |                            2055.00 |              4996827 |                              2045.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| valkey-1-1-1 | valkey-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61921.42 |               161495.00 |            5003173 |                            2055.00 |              4996827 |                              2045.00 |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |        59.23 |      2.24 |           1.44 |                  1.45 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 | n/a          |         0 |           0.54 |                  0.54 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       257.10 |      1.82 |           1.56 |                  1.57 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| valkey-1-1-1-1 |       678.60 |      5.01 |           1.48 |                  1.48 |

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
