## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 687s 
* Code: 1794818068
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 5000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Application metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Cassandra'].
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
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandra-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1085959
  * datadisk:1090
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818068
* cassandra-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1087773
  * datadisk:1268
  * volume_size:49G
  * volume_used:1.3G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794818068

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Cassandra-1-2

### Data Parameters of Reused Volumes
* Cassandra-1: DDL values of the volume: num_worker_replicas=1
* Cassandra-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Ingestion
* Cassandra-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1794818068-6f994f468b-k644q: 0
* bexhoma-sut-cassandra-1-1794818068-6d99b95d69-qmt8m: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9923.00 |                12597.00 |            125000.00 |                              1905.00 | 1.00 |              285.78 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8301.24 |                15058.00 |            125000.00 |                              1867.00 | 1.00 |              239.08 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9368.21 |                13343.00 |            125000.00 |                              1808.00 | 1.00 |              269.80 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8822.08 |                14169.00 |            125000.00 |                              1994.00 | 1.00 |              254.08 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8787.96 |                14224.00 |            125000.00 |                              1933.00 | 1.00 |              253.09 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9842.52 |                12700.00 |            125000.00 |                              1793.00 | 1.00 |              283.46 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9255.15 |                13506.00 |            125000.00 |                              1792.00 | 1.00 |              266.55 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9923.79 |                12596.00 |            125000.00 |                              1917.00 | 1.00 |              285.81 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              239.08 |                        74223.93 |                15058.00 |           1000000.00 |                              1876.12 |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        55881.53 |                89475.00 |            2500842 |                            4187.00 |              2499158 |                              4023.00 |
| cassandra-1-2-1-1-1 | cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |       1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499106 |                            4187.00 |              2500894 |                              3487.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        55881.53 |                89475.00 |            2500842 |                            4187.00 |              2499158 |                              4023.00 |
| cassandra-1-2-1 | cassandra-1-2-1 |                2 |        1 |               1 |           1 |       128 |    65536 |        0 |                        62985.78 |                79383.00 |            2499106 |                            4187.00 |              2500894 |                              3487.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |
| cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |         2.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       149.46 |      3.53 |           5.09 |                  5.99 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       318.32 |      4.58 |           5.35 |                  6.47 |
| cassandra-1-2-1-1 |       496.69 |      8.87 |           5.09 |                  6.40 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       397.33 |      7.86 |           1.42 |                  1.42 |
| cassandra-1-2-1-1 |       355.45 |      8.17 |           1.44 |                  1.45 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage, Working Set [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Rx Total [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Network Tx Total [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-2-1-1 (bexhoma-metrics-cassandra-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                    0.87 |                 25359.90 |                                 14.24 |                                   4.77 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                51479.07 |                 51516.50 |                                  1.60 |                                   0.54 |                              0.00 |
| cassandra-1-2-1-1 |                47024.40 |                 47225.30 |                                 20.50 |                                   0.45 |                              0.00 |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
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
* TEST passed: Reset scripts ran without errors
