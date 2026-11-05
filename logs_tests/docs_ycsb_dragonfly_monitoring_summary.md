## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 362s 
* Code: 1793823429
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
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
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:854201
  * datadisk:3256
  * volume_size:1.8T
  * volume_used:835G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793823429

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1793823429-685fff678b-k4rgm: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24487.40 |                15314.00 |            375000.00 |                               579.00 | 3.00 |              705.24 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24485.80 |                15315.00 |            375000.00 |                               540.00 | 3.00 |              705.19 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24458.65 |                15332.00 |            375000.00 |                               600.00 | 3.00 |              704.41 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24484.20 |                15316.00 |            375000.00 |                               547.00 | 3.00 |              705.14 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24477.81 |                15320.00 |            375000.00 |                               573.00 | 3.00 |              704.96 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24474.61 |                15322.00 |            375000.00 |                               572.00 | 3.00 |              704.87 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24474.61 |                15322.00 |            375000.00 |                               545.00 | 3.00 |              704.87 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24497.00 |                15308.00 |            375000.00 |                               560.00 | 3.00 |              705.51 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              704.41 |                       195840.07 |                15332.00 |           3000000.00 |                               564.50 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65492.17 |               152690.00 |            4999051 |                             724.00 |              5000949 |                               705.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65492.17 |               152690.00 |            4999051 |                             724.00 |              5000949 |                               705.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       187.33 |      5.36 |           4.68 |                  4.68 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 | n/a          |         0 |           0.53 |                  0.53 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       444.98 |      3.02 |           4.63 |                  4.63 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       608.10 |      4.96 |           1.02 |                  1.03 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             6000001.00 |                 4.54 |                     29995.33 |                   18.93 |                    0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             7864263.00 |                 4.54 |                     51989.37 |                   16.95 |                    0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
