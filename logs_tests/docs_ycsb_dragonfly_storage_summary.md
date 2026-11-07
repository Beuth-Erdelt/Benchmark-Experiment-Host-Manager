## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 728s 
* Code: 1794040133
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
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* dragonfly-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804842
  * datadisk:1086
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040133
* dragonfly-1-2-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:804843
  * datadisk:1086
  * volume_size:49G
  * volume_used:1.1G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794040133

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Dragonfly-1-2

### Data Parameters of Reused Volumes
* Dragonfly-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Dragonfly-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-dragonfly-1-1794040133-546c48698f-vzdg5: 0
* bexhoma-sut-dragonfly-1-1794040133-567b5f5bbd-67xnl: 0

### Workflow

#### Actual

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Dragonfly-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Dragonfly-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonfly-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        23941.77 |                 5221.00 |            125000.00 |                               711.00 | 1.00 |              689.52 |
| dragonfly-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24304.88 |                 5143.00 |            125000.00 |                               586.00 | 1.00 |              699.98 |
| dragonfly-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24267.13 |                 5151.00 |            125000.00 |                               614.00 | 1.00 |              698.89 |
| dragonfly-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24281.27 |                 5148.00 |            125000.00 |                               878.00 | 1.00 |              699.30 |
| dragonfly-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24323.80 |                 5139.00 |            125000.00 |                               638.00 | 1.00 |              700.53 |
| dragonfly-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24267.13 |                 5151.00 |            125000.00 |                               652.00 | 1.00 |              698.89 |
| dragonfly-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24262.42 |                 5152.00 |            125000.00 |                               621.00 | 1.00 |              698.76 |
| dragonfly-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        24271.84 |                 5150.00 |            125000.00 |                               623.00 | 1.00 |              699.03 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Dragonfly-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              689.52 |                       193920.26 |                 5221.00 |           1000000.00 |                               665.38 |

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1-1-1 | dragonfly-1-1-1 | dragonfly-1-1-1-1 | Dragonfly-1     |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65481.45 |               152715.00 |            4996545 |                             781.00 |              5003455 |                               762.00 |
| dragonfly-1-2-1-1-1 | dragonfly-1-2-1 | dragonfly-1-2-1-1 | Dragonfly-1     |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        65448.88 |               152791.00 |            5000110 |                             793.00 |              4999890 |                               772.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonfly-1-1-1 | dragonfly-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        65481.45 |               152715.00 |            4996545 |                             781.00 |              5003455 |                               762.00 |
| dragonfly-1-2-1 | dragonfly-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        65448.88 |               152791.00 |            5000110 |                             793.00 |              4999890 |                               772.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonfly-1-1-1 | dragonfly-1-1-1-1 |                1 |        1 |               1 |        12.00 |                |
| dragonfly-1-2-1 | dragonfly-1-2-1-1 |                2 |        1 |               1 |        12.00 |                |

### Monitoring

### Loading phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |        63.88 |      1.72 |           1.65 |                  1.65 |

### Loading phase: component loader

| DBMS              | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|:-------------|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       457.38 |      3.03 |           1.60 |                  1.60 |
| dragonfly-1-2-1-1 |       426.73 |      3.97 |           1.69 |                  2.75 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| dragonfly-1-1-1-1 |       639.74 |      5.23 |           1.37 |                  1.37 |
| dragonfly-1-2-1-1 |       730.85 |      6.69 |           1.05 |                  1.05 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Utilization [CPUs] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU User Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU System Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-1-1-1 (bexhoma-metrics-dragonfly-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replica Lag [records] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Cluster Slot Moved Errors [count] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Replication Streaming Memory [GiB] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* Full Sync Replication Memory [GiB] for connection dragonfly-1-2-1-1 (bexhoma-metrics-dragonfly-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Application Metrics

#### Loading phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             2000000.00 |                 1.53 |                     13177.01 |                    8.32 |                    0.00 |

#### Benchmarking phase: SUT deployment

| DBMS              |   Replies Sent [count] |   Memory Usage [GiB] |   Processed Commands [ops/s] |   Network Input [MiB/s] |   Replica Lag [records] |
|:------------------|-----------------------:|---------------------:|-----------------------------:|------------------------:|------------------------:|
| dragonfly-1-1-1-1 |             8531554.00 |                 1.53 |                     37933.12 |                    7.65 |                    0.00 |
| dragonfly-1-2-1-1 |             8474139.00 |                 1.63 |                     31871.08 |                    3.22 |                    0.00 |

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
