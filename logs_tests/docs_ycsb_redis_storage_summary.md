## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 522s 
* Code: 1794004396
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
  * Experiment uses bexhoma version 0.11.13.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:870015
  * datadisk:1
  * volume_size:49G
  * volume_used:24K
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794004396
* redis-1-2-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:869269
  * datadisk:1
  * volume_size:49G
  * volume_used:24K
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794004396

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Redis-1-2

### Data Parameters of Reused Volumes
* Redis-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Init Scripts with Errors
* Redis-1: save-snapshot-ycsb.sh

### SUT Container Restarts
* bexhoma-sut-redis-1-1794004396-7fb69974dd-gdcs4: 0
* bexhoma-sut-redis-1-1794004396-74d8cf8858-pmn4f: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         8911.39 |                14027.00 |            125000.00 |                              1846.00 | 1.00 |              256.65 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10833.77 |                11538.00 |            125000.00 |                              1822.00 | 1.00 |              312.01 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9966.51 |                12542.00 |            125000.00 |                              1897.00 | 1.00 |              287.04 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9767.15 |                12798.00 |            125000.00 |                              1887.00 | 1.00 |              281.29 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10488.34 |                11918.00 |            125000.00 |                              1872.00 | 1.00 |              302.06 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9245.56 |                13520.00 |            125000.00 |                              1847.00 | 1.00 |              266.27 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                         9674.17 |                12921.00 |            125000.00 |                              1854.00 | 1.00 |              278.62 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        10642.83 |                11745.00 |            125000.00 |                              1848.00 | 1.00 |              306.51 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 1.00 |              256.65 |                        79529.72 |                14027.00 |           1000000.00 |                              1859.12 |

### Benchmarking

#### Per Connection

| DBMS            | phase       | job           | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |
|:----------------|:------------|:--------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 | Redis-1         |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                            0.00 |                  173.00 |
| redis-1-2-1-1-1 | redis-1-2-1 | redis-1-2-1-1 | Redis-1         |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                            0.00 |                    0.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |
|:------------|:------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                            0.00 |                  173.00 |
| redis-1-2-1 | redis-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                            0.00 |                    0.00 |

### Monitoring

### Loading phase: SUT deployment

| DBMS          |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|-------------:|----------:|---------------:|----------------------:|
| redis-1-1-1-1 |        67.03 |      1.62 |           1.53 |                  1.53 |

### Loading phase: component loader

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |         0 |           0.00 |                  0.00 |

### Benchmarking phase: SUT deployment

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |      0.03 |           1.53 |                  1.53 |
| redis-1-2-1-1 | n/a          |      0.32 |           1.53 |                  1.53 |

### Benchmarking phase: component benchmarker

| DBMS          | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:--------------|:-------------|----------:|---------------:|----------------------:|
| redis-1-1-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |
| redis-1-2-1-1 | n/a          |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* Memory Usage incl. Page Cache [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU System Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Tx Total [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-1-1-1 (bexhoma-metrics-redis-1-1-1-1-loading.log, expected: series exists only while non-zero)
* Memory Usage, Working Set [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization [CPUs] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Memory Usage incl. Page Cache [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Utilization Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU System Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* CPU User Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Network Rx Total [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* Network Tx Total [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: phase shorter than scrape interval)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection redis-1-2-1-1 (bexhoma-metrics-redis-1-2-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST failed: Init scripts without errors (failed: Redis-1: save-snapshot-ycsb.sh)
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component loader contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: SUT deployment contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Benchmarking phase: component benchmarker contains 0 or NaN in CPU [CPUs] (phase shorter than monitoring scrape interval)
* TEST skipped: Monitoring metrics missing (job pods ran shorter than scrape interval; phase shorter than scrape interval; series exists only while non-zero)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST failed: Execution Phase: [OVERALL].Throughput(ops/sec) contains 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
