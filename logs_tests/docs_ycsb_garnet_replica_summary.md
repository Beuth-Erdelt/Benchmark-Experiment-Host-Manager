## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 431s 
* Code: 1793814254
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
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
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* garnet-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:850500
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:605854
    * datadisk:895
    * volume_size:1.8T
    * volume_used:592G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:609635
    * datadisk:1019
    * volume_size:879G
    * volume_used:596G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:515784
    * datadisk:894
    * volume_size:1.8T
    * volume_used:504G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 3
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:252570
    * datadisk:894
    * volume_size:550G
    * volume_used:247G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 4
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:147241
    * datadisk:895
    * volume_size:219G
    * volume_used:144G
    * cpu_list:0-95
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 5
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:247817
    * datadisk:1019
    * volume_size:439G
    * volume_used:243G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-1-1793814254.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 24.25 CPU, 384.5 GiB RAM requested in 7 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 6 x, 24.0 CPU, 384.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793814254
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793814254-68dd5889b7-b8nnr: 0
* bx-w-garnet-1-1793814254-0: 0
* bx-w-garnet-1-1793814254-1: 0
* bx-w-garnet-1-1793814254-2: 0
* bx-w-garnet-1-1793814254-3: 0
* bx-w-garnet-1-1793814254-4: 0
* bx-w-garnet-1-1793814254-5: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13020.83 |                 9600.00 |            125000.00 |                              2049.00 | 1.00 |              375.00 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13354.70 |                 9360.00 |            125000.00 |                              1931.00 | 1.00 |              384.62 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13337.60 |                 9372.00 |            125000.00 |                              2209.00 | 1.00 |              384.12 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13228.91 |                 9449.00 |            125000.00 |                              2167.00 | 1.00 |              380.99 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12960.08 |                 9645.00 |            125000.00 |                              2055.00 | 1.00 |              373.25 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13313.45 |                 9389.00 |            125000.00 |                              2051.00 | 1.00 |              383.43 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13302.12 |                 9397.00 |            125000.00 |                              2049.00 | 1.00 |              383.10 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13094.49 |                 9546.00 |            125000.00 |                              2101.00 | 1.00 |              377.12 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              373.25 |                       105612.19 |                 9645.00 |           1000000.00 |                              2076.50 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        49735.65 |               201063.00 |            4997532 |                             292.00 |              5002468 |                               281.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        49735.65 |               201063.00 |            4997532 |                             292.00 |              5002468 |                               281.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         6.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       297.38 |      8.58 |           6.40 |                  6.40 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |      1142.18 |      8.46 |           8.35 |                  9.49 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       749.72 |      4.90 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

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
* TEST skipped: Monitoring metrics missing (phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
