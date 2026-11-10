## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 815s 
* Code: 1794041379
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
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
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
  * disk:804839
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
    * disk:204333
    * datadisk:356
    * volume_size:49G
    * volume_used:356M
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716984
    * datadisk:377
    * volume_size:49G
    * volume_used:377M
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663004
    * datadisk:355
    * volume_size:49G
    * volume_used:355M
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794041379
    * BEXHOMA_WORKERS:3
* dragonflycluster-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804840
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
    * disk:204333
    * datadisk:356
    * volume_size:49G
    * volume_used:356M
    * cpu_list:0-127
  * worker 1
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:716985
    * datadisk:377
    * volume_size:49G
    * volume_used:377M
    * cpu_list:0-127
  * worker 2
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:663004
    * datadisk:355
    * volume_size:49G
    * volume_used:355M
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794041379
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: DragonflyCluster-1-2

### Data Parameters of Reused Volumes
* DragonflyCluster-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794041379-6b877b8495-9ktgn: 0
* bx-w-df-nvme-ycsb-1-0: 0
* bx-w-df-nvme-ycsb-1-1: 0
* bx-w-df-nvme-ycsb-1-2: 0
* bexhoma-sut-dragonflycluster-1-1794041379-7554fbf7d5-bgvf6: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20709.08 |                 6036.00 |            125000.00 |                               578.00 | 1.00 |              596.42 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18862.23 |                 6627.00 |            125000.00 |                               671.00 | 1.00 |              543.23 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20193.86 |                 6190.00 |            125000.00 |                               580.00 | 1.00 |              581.58 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18950.88 |                 6596.00 |            125000.00 |                               682.00 | 1.00 |              545.79 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20233.09 |                 6178.00 |            125000.00 |                               712.00 | 1.00 |              582.71 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        18976.77 |                 6587.00 |            125000.00 |                               681.00 | 1.00 |              546.53 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        20538.94 |                 6086.00 |            125000.00 |                               581.00 | 1.00 |              591.52 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        17977.85 |                 6953.00 |            125000.00 |                               721.00 | 1.00 |              517.76 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              517.76 |                       156442.70 |                 6953.00 |           1000000.00 |                               650.75 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62484.77 |               160039.00 |            5001142 |                             256.00 |              4998858 |                               241.00 |
| dragonflycluster-1-2-1-1-1 | dragonflycluster-1-2-1 | dragonflycluster-1-2-1-1 | DragonflyCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62119.52 |               160980.00 |            5002813 |                             259.00 |              4997187 |                               243.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62484.77 |               160039.00 |            5001142 |                             256.00 |              4998858 |                               241.00 |
| dragonflycluster-1-2-1 | dragonflycluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        62119.52 |               160980.00 |            5002813 |                             259.00 |              4997187 |                               243.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        16.00 |                |
| dragonflycluster-1-2-1 | dragonflycluster-1-2-1-1 |                2 |        1 |               1 |        16.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       124.69 |      3.82 |           1.65 |                  1.65 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       485.40 |      4.02 |           1.67 |                  1.67 |
| dragonflycluster-1-2-1-1 |       559.74 |      4.30 |           1.78 |                  2.48 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| dragonflycluster-1-1-1-1 |       729.02 |      4.95 |           1.49 |                  1.49 |
| dragonflycluster-1-2-1-1 |       639.78 |      5.19 |           1.48 |                  1.49 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU User Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-1-1-1 (bexhoma-metrics-dragonflycluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonflycluster-1-2-1-1 (bexhoma-metrics-dragonflycluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             2001631.00 |                 1.52 |                     12728.40 |                    7.70 |                    0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:-------------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonflycluster-1-1-1-1 |             9017601.00 |                 1.52 |                     33388.58 |                    6.95 |                    0.00 |
| dragonflycluster-1-2-1-1 |             9025007.00 |                 1.61 |                     32678.29 |                    3.30 |                    0.00 |

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
* TEST passed: Reset scripts ran without errors
