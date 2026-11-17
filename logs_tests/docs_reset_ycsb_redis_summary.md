## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 380s 
* Code: 1794823477
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [4].
  * Factors for benchmarking are [1]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * Experiment is limited to DBMS ['Redis'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [128] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* redis-1-1-1-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1161527
  * datadisk:1095
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794823477
* redis-1-1-2-1 uses docker image redis:8.10.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1161330
  * datadisk:1095
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794823477

### Init Scripts Not in Folder
* Redis-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* Redis-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-redis-1-1794823477-57dbdd9588-85sm5: 0

### Workflow

#### Actual

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 1 Client 2: ycsb (2 pods)

#### Planned

* DBMS Redis-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Redis-1 - Experiment 1 Client 2: ycsb (2 pods)

### Loading

#### Per Connection

| connection      |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| redis-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8136.43 |                15363.00 |            125000.00 |                              1755.00 | 1.00 |              234.33 |
| redis-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8163.53 |                15312.00 |            125000.00 |                              1832.00 | 1.00 |              235.11 |
| redis-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8167.80 |                15304.00 |            125000.00 |                              1856.00 | 1.00 |              235.23 |
| redis-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8163.53 |                15312.00 |            125000.00 |                              1771.00 | 1.00 |              235.11 |
| redis-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8165.67 |                15308.00 |            125000.00 |                              1845.00 | 1.00 |              235.17 |
| redis-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8165.67 |                15308.00 |            125000.00 |                              1717.00 | 1.00 |              235.17 |
| redis-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8163.53 |                15312.00 |            125000.00 |                              1853.00 | 1.00 |              235.11 |
| redis-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8166.73 |                15306.00 |            125000.00 |                              1885.00 | 1.00 |              235.20 |

#### Per Run

| DBMS      |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Redis-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              234.33 |                        65292.89 |                15363.00 |           1000000.00 |                              1814.25 |

### Benchmarking

#### Per Connection

| connection      | phase       | job           |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------|:------------|:--------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1-1-1 | redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    16384 |        0 |                        16331.86 |                61230.00 |             499754 |                             855.00 |               500246 |                               821.00 |
| redis-1-1-2-1-1 | redis-1-1-2 | redis-1-1-2-1 |                1 |        2 |               1 |       1 |       128 |    16384 |        0 |                        16314.81 |                30647.00 |             249812 |                             645.00 |               250188 |                               611.00 |
| redis-1-1-2-1-2 | redis-1-1-2 | redis-1-1-2-1 |                1 |        2 |               1 |       2 |       128 |    16384 |        0 |                        16321.73 |                30634.00 |             250218 |                             618.00 |               249782 |                               585.00 |

#### Per Phase

| DBMS        | phase       |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------|:------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| redis-1-1-1 | redis-1-1-1 |                1 |        1 |               1 |           1 |       128 |    16384 |        0 |                        16331.86 |                61230.00 |             499754 |                             855.00 |               500246 |                               821.00 |
| redis-1-1-2 | redis-1-1-2 |                1 |        2 |               1 |           2 |       256 |    32768 |        0 |                        32636.54 |                30647.00 |             500030 |                             645.00 |               499970 |                               611.00 |

#### Reset

| phase       | job           |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:------------|:--------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| redis-1-1-1 | redis-1-1-1-1 |                1 |        1 |               1 |         6.00 |                |
| redis-1-1-2 | redis-1-1-2-1 |                1 |        2 |               1 |         7.00 |                |

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
