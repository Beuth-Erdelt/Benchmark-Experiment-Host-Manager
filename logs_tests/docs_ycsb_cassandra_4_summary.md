## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 738s 
* Code: 1793444325
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
  * Experiment uses bexhoma version 0.11.11.
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
  * disk:862510
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
    * code:1793444325
* cassandra-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:861708
  * datadisk:1267
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
    * code:1793444325

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Cassandra-1-2

### Data Parameters of Reused Volumes
* Cassandra-1: DDL values of the volume: num_worker_replicas=1
* Cassandra-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1793444325-5dfc894d9d-ckffq: 0
* bexhoma-sut-cassandra-1-1793444325-5f5f866b9c-wr87q: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Cassandra-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10608.50 |                11783.00 |            125000.00 |                              1480.00 | 1.00 |              305.52 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10235.00 |                12213.00 |            125000.00 |                              1492.00 | 1.00 |              294.77 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12345.68 |                10125.00 |            125000.00 |                              1479.00 | 1.00 |              355.56 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12051.68 |                10372.00 |            125000.00 |                              1545.00 | 1.00 |              347.09 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10068.47 |                12415.00 |            125000.00 |                              1641.00 | 1.00 |              289.97 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9788.57 |                12770.00 |            125000.00 |                              1626.00 | 1.00 |              281.91 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        12989.71 |                 9623.00 |            125000.00 |                              1223.00 | 1.00 |              374.10 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        11650.67 |                10729.00 |            125000.00 |                              1520.00 | 1.00 |              335.54 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              281.91 |                        89738.27 |                12770.00 |           1000000.00 |                              1500.75 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 | Cassandra-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        57827.54 |                86464.00 |            2502102 |                            4911.00 |              2497898 |                              4539.00 |
| cassandra-1-2-1-1-1 | cassandra-1-2-1 | cassandra-1-2-1-1 | Cassandra-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        60016.08 |                83311.00 |            2500420 |                            5291.00 |              2499580 |                              4319.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        57827.54 |                86464.00 |            2502102 |                            4911.00 |              2497898 |                              4539.00 |
| cassandra-1-2-1 | cassandra-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        60016.08 |                83311.00 |            2500420 |                            5291.00 |              2499580 |                              4319.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         3.00 |                |
| cassandra-1-2-1 | cassandra-1-2-1-1 |                2 |        1 |               1 |         3.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       150.57 |      4.35 |           5.10 |                  6.00 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       424.93 |      5.34 |           5.28 |                  6.49 |
| cassandra-1-2-1-1 |       386.67 |      6.53 |           5.06 |                  6.35 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| cassandra-1-1-1-1 |       415.21 |      7.27 |           1.42 |                  1.42 |
| cassandra-1-2-1-1 |       406.20 |      6.10 |           1.40 |                  1.40 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Memory Usage incl. Page Cache [MiB] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection cassandra-1-1-1-1 (bexhoma-metrics-cassandra-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
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
| cassandra-1-1-1-1 |                    0.87 |                 29730.10 |                                 14.24 |                                   5.72 |                              0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandra-1-1-1-1 |                47674.63 |                 47712.70 |                                  1.60 |                                   0.54 |                              0.00 |
| cassandra-1-2-1-1 |                24250.73 |                 24330.93 |                                  1.92 |                                   0.54 |                              0.00 |

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
* TEST passed: Reset scripts ran without errors
