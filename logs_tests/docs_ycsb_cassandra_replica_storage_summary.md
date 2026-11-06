## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 1100s 
* Code: 1793446418
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
  * Workers are fixed to cl-worker36, cl-worker37, cl-worker29.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run 2 times.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandracluster-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1277015
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:861765
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539030
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574576
    * datadisk:1090
    * volume_size:49G
    * volume_used:1.1G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793446418
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cassandracluster-1-2-1-1 uses docker image cassandra:5.0.9
  * RAM:540590809088
  * CPU:AMD EPYC 7352 24-Core Processor
  * Cores:96
  * host:6.8.0-137-generic
  * node:cl-worker23
  * disk:1277184
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.3T
  * cpu_list:0-95
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * worker 0
    * RAM:2164173156352
    * CPU:INTEL(R) XEON(R) PLATINUM 8570
    * Cores:224
    * host:6.8.0-147-generic
    * node:cl-worker36
    * disk:861766
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-223
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:539029
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * worker 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:574574
    * datadisk:1268
    * volume_size:49G
    * volume_used:1.3G
    * cpu_list:0-127
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793446418
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
    * ddl_num_worker_replicas:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: CassandraCluster-1-2

### Data Parameters of Reused Volumes
* CassandraCluster-1: DDL values of the volume: num_worker_replicas=3
* CassandraCluster-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### SUT Container Restarts
* bexhoma-sut-cassandracluster-1-1793446418-6c9fd645fc-5rddd: 0
* bx-w-ca-nvme-ycsb-1-0: 0
* bx-w-ca-nvme-ycsb-1-1: 0
* bx-w-ca-nvme-ycsb-1-2: 0
* bexhoma-sut-cassandracluster-1-1793446418-9f9967867-l62dh: 0

### Workflow

#### Actual

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS CassandraCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CassandraCluster-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandracluster-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7925.44 |                15772.00 |            125000.00 |                              2303.00 | 1.00 |              228.25 |
| cassandracluster-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7987.22 |                15650.00 |            125000.00 |                              1915.00 | 1.00 |              230.03 |
| cassandracluster-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7706.06 |                16221.00 |            125000.00 |                              2093.00 | 1.00 |              221.93 |
| cassandracluster-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         7682.38 |                16271.00 |            125000.00 |                              2093.00 | 1.00 |              221.25 |
| cassandracluster-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8234.52 |                15180.00 |            125000.00 |                              2157.00 | 1.00 |              237.15 |
| cassandracluster-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8476.30 |                14747.00 |            125000.00 |                              2169.00 | 1.00 |              244.12 |
| cassandracluster-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8629.62 |                14485.00 |            125000.00 |                              2137.00 | 1.00 |              248.53 |
| cassandracluster-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8469.41 |                14759.00 |            125000.00 |                              2187.00 | 1.00 |              243.92 |

#### Per Run

| DBMS                 |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CassandraCluster-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              221.25 |                        65110.94 |                16271.00 |           1000000.00 |                              2131.75 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1-1-1 | cassandracluster-1-1-1 | cassandracluster-1-1-1-1 | CassandraCluster-1 |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        63099.44 |                79240.00 |            2500077 |                            3851.00 |              2499923 |                              2727.00 |
| cassandracluster-1-2-1-1-1 | cassandracluster-1-2-1 | cassandracluster-1-2-1-1 | CassandraCluster-1 |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62576.66 |                79902.00 |            2500333 |                            6647.00 |              2499667 |                              3409.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandracluster-1-1-1 | cassandracluster-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        63099.44 |                79240.00 |            2500077 |                            3851.00 |              2499923 |                              2727.00 |
| cassandracluster-1-2-1 | cassandracluster-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        62576.66 |                79902.00 |            2500333 |                            6647.00 |              2499667 |                              3409.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandracluster-1-1-1 | cassandracluster-1-1-1-1 |                1 |        1 |               1 |        11.00 |                |
| cassandracluster-1-2-1 | cassandracluster-1-2-1-1 |                2 |        1 |               1 |        11.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       867.70 |     21.36 |          15.13 |                 17.80 |

### Loading phase: component loader

| DBMS                     | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|:-------------|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: component worker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |      1706.30 |     25.51 |          15.92 |                 19.39 |
| cassandracluster-1-2-1-1 |      1854.32 |     27.84 |          15.36 |                 18.34 |

### Benchmarking phase: component benchmarker

| DBMS                     |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-------------------------|-------------:|----------:|---------------:|----------------------:|
| cassandracluster-1-1-1-1 |       476.69 |      9.33 |           1.42 |                  1.43 |
| cassandracluster-1-2-1-1 |       592.20 |     10.01 |           1.47 |                  1.47 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-1-1-1 (bexhoma-metrics-cassandracluster-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection cassandracluster-1-2-1-1 (bexhoma-metrics-cassandracluster-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                    1.00 |                 29777.97 |                                 51.01 |                                   1.11 |                              0.00 |

#### Benchmarking phase: component worker

| DBMS                     |   Read Requests [ops/s] |   Write Requests [ops/s] |   Read Latency p99, Slowest Node [ms] |   Write Latency p99, Slowest Node [ms] |   Read and Write Timeouts [count] |
|:-------------------------|------------------------:|-------------------------:|--------------------------------------:|---------------------------------------:|----------------------------------:|
| cassandracluster-1-1-1-1 |                36726.70 |                 36713.17 |                                  4.77 |                                   1.11 |                              0.00 |
| cassandracluster-1-2-1-1 |                45201.10 |                 45422.17 |                                  5.72 |                                   0.77 |                              0.00 |

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
