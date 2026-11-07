## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 415s 
* Code: 1794040924
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
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Dragonfly'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804836
  * datadisk:1
  * volume_size:1.8T
  * volume_used:786G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:206328
    * datadisk:356
    * volume_size:879G
    * volume_used:202G
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:717392
    * datadisk:377
    * volume_size:1.8T
    * volume_used:701G
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663359
    * datadisk:355
    * volume_size:1.8T
    * volume_used:648G
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040924
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794040924-665fd78dbd-wjc6k: 0
* bx-w-dragonflycluster-1-1794040924-0: 0
* bx-w-dragonflycluster-1-1794040924-1: 0
* bx-w-dragonflycluster-1-1794040924-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17700.37 |                 7062.00 |            125000.00 |                               774.00 | 1.00 |              509.77 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17864.80 |                 6997.00 |            125000.00 |                               763.00 | 1.00 |              514.51 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18910.74 |                 6610.00 |            125000.00 |                               631.00 | 1.00 |              544.63 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19180.60 |                 6517.00 |            125000.00 |                               652.00 | 1.00 |              552.40 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18808.31 |                 6646.00 |            125000.00 |                               696.00 | 1.00 |              541.68 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19549.58 |                 6394.00 |            125000.00 |                               633.00 | 1.00 |              563.03 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17775.88 |                 7032.00 |            125000.00 |                               763.00 | 1.00 |              511.95 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        19275.25 |                 6485.00 |            125000.00 |                               660.00 | 1.00 |              555.13 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              509.77 |                       149065.53 |                 7062.00 |           1000000.00 |                               696.50 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61335.39 |               163038.00 |            4999755 |                             267.00 |              5000245 |                               251.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        61335.39 |               163038.00 |            4999755 |                             267.00 |              5000245 |                               251.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        15.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       109.17 |      3.68 |           1.64 |                  1.64 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       554.43 |      3.77 |           1.68 |                  2.03 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       632.02 |      4.93 |           1.48 |                  1.48 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             2001602.00 |                 1.52 |                     10258.04 |                    7.23 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9179925.00 |                 1.52 |                     38832.80 |                    7.49 |                    0.00 |

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
* TEST failed: Monitoring metrics missing
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
