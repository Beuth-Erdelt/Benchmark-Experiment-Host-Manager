## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 184s 
* Code: 1794695478
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4].
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['Redis'].
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
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1046314
  * datadisk:1095
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * resources_total: 4.0 CPU, 64.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 64.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794695478

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794695478-659c4c95b9-xdqwz: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         8961.22 |                13949.00 |            125000.00 |                              2044.00 | 1.00 |              258.08 |
| redis-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9159.52 |                13647.00 |            125000.00 |                              2000.00 | 1.00 |              263.79 |
| redis-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9645.06 |                12960.00 |            125000.00 |                              2002.00 | 1.00 |              277.78 |
| redis-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9150.81 |                13660.00 |            125000.00 |                              2010.00 | 1.00 |              263.54 |
| redis-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9467.55 |                13203.00 |            125000.00 |                              1975.00 | 1.00 |              272.67 |
| redis-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                        10030.49 |                12462.00 |            125000.00 |                              1972.00 | 1.00 |              288.88 |
| redis-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9782.44 |                12778.00 |            125000.00 |                              1973.00 | 1.00 |              281.73 |
| redis-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |     0.00 |                         9654.75 |                12947.00 |            125000.00 |                              1971.00 | 1.00 |              278.06 |

#### Per Run

| DBMS      |   experiment_run |   threads |    target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|----------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |     0.00 | 1.00 |              258.08 |                        75851.83 |                13949.00 |           1000000.00 |                              1993.38 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    65536 |        0 |                        65082.98 |                15365.00 |             499904 |                            1120.00 |               500096 |                              1056.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    65536 |        0 |                        65082.98 |                15365.00 |             499904 |                            1120.00 |               500096 |                              1056.00 |

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
