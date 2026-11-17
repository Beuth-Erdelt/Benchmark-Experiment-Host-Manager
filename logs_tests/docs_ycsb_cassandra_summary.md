## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 297s 
* Code: 1794817263
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['Cassandra'].
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
  * SUT requests 4 CPU and 16Gi RAM. RAM limit is 16Gi.

### Connections
* cassandra-1-1-1-1 uses docker image cassandra:5.0.9
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1056542
  * datadisk:1090
  * volume_size:1.8T
  * volume_used:1.1T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * limits_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794817263

### Ingestion
* Cassandra-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cassandra-1-1794817263-858bcd889b-bvwj5: 0

### Workflow

#### Actual

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Cassandra-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection          |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:--------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cassandra-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10470.77 |                11938.00 |            125000.00 |                              1635.00 | 1.00 |              301.56 |
| cassandra-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10650.08 |                11737.00 |            125000.00 |                              1598.00 | 1.00 |              306.72 |
| cassandra-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10544.07 |                11855.00 |            125000.00 |                              1713.00 | 1.00 |              303.67 |
| cassandra-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10118.18 |                12354.00 |            125000.00 |                              1869.00 | 1.00 |              291.40 |
| cassandra-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10210.75 |                12242.00 |            125000.00 |                              1677.00 | 1.00 |              294.07 |
| cassandra-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10298.24 |                12138.00 |            125000.00 |                              1626.00 | 1.00 |              296.59 |
| cassandra-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10560.11 |                11837.00 |            125000.00 |                              1545.00 | 1.00 |              304.13 |
| cassandra-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        11428.05 |                10938.00 |            125000.00 |                              1484.00 | 1.00 |              329.13 |

#### Per Run

| DBMS          |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:--------------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Cassandra-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              291.40 |                        84280.25 |                12354.00 |           1000000.00 |                              1643.38 |

### Benchmarking

#### Per Connection

| connection          | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1-1-1 | cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        52416.40 |                19078.00 |             499969 |                            4847.00 |               500031 |                              4195.00 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cassandra-1-1-1 | cassandra-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        52416.40 |                19078.00 |             499969 |                            4847.00 |               500031 |                              4195.00 |

#### Reset

| phase           | job               |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:----------------|:------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cassandra-1-1-1 | cassandra-1-1-1-1 |                1 |        1 |               1 |         2.00 |                |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Init scripts without errors
* TEST passed: Loader pods without errors
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Loading Phase: all rows inserted
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
