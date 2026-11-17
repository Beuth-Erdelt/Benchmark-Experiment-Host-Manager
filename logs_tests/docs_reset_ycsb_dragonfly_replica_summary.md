## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 487s 
* Code: 1794822975
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
  * Experiment is limited to DBMS ['Dragonfly'].
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
  * Distributed DBMS uses 3 worker nodes, 1 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* dragonflycluster-1-1-1-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1160242
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1390286
    * datadisk:1086
    * volume_size:1.8T
    * volume_used:1.4T
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:908909
    * datadisk:1086
    * volume_size:1.8T
    * volume_used:888G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:644299
    * datadisk:1086
    * volume_size:879G
    * volume_used:630G
    * cpu_list:0-127
  * resources_total: 13.0 CPU, 49.0 GiB RAM requested in 4 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822975
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3
* dragonflycluster-1-1-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1160243
  * datadisk:1
  * volume_size:1.8T
  * volume_used:1.2T
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1390059
    * datadisk:1086
    * volume_size:1.8T
    * volume_used:1.4T
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:909286
    * datadisk:1086
    * volume_size:1.8T
    * volume_used:888G
    * cpu_list:0-255
  * worker 2
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:644299
    * datadisk:1086
    * volume_size:879G
    * volume_used:630G
    * cpu_list:0-127
  * resources_total: 13.0 CPU, 49.0 GiB RAM requested in 4 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794822975
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### Init Scripts Not in Folder
* DragonflyCluster-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### Ingestion
* DragonflyCluster-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1794822975-76df65654c-jsdkg: 0
* bx-w-dragonflycluster-1-1794822975-0: 0
* bx-w-dragonflycluster-1-1794822975-1: 0
* bx-w-dragonflycluster-1-1794822975-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 1 Client 2: ycsb (2 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 1 Client 2: ycsb (2 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8166.20 |                15307.00 |            125000.00 |                               937.00 | 1.00 |              235.19 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8165.67 |                15308.00 |            125000.00 |                               926.00 | 1.00 |              235.17 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8164.60 |                15310.00 |            125000.00 |                               948.00 | 1.00 |              235.14 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8167.27 |                15305.00 |            125000.00 |                               913.00 | 1.00 |              235.22 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8163.53 |                15312.00 |            125000.00 |                               924.00 | 1.00 |              235.11 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8162.47 |                15314.00 |            125000.00 |                               788.00 | 1.00 |              235.08 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8164.60 |                15310.00 |            125000.00 |                               893.00 | 1.00 |              235.14 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         8164.60 |                15310.00 |            125000.00 |                               990.00 | 1.00 |              235.14 |

#### Per Run

| DBMS                 |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |              235.08 |                        65318.92 |                15314.00 |           1000000.00 |                               914.88 |

### Benchmarking

#### Per Connection

| connection                 | phase                  | job                      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |       1 |       128 |    16384 |        0 |                        16354.83 |                61144.00 |             501109 |                             355.00 |               498891 |                               347.00 |
| dragonflycluster-1-1-2-1-1 | dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 |                1 |        2 |               1 |       1 |       128 |    16384 |        0 |                        16296.73 |                30681.00 |             249270 |                             319.00 |               250730 |                               289.00 |
| dragonflycluster-1-1-2-1-2 | dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 |                1 |        2 |               1 |       2 |       128 |    16384 |        0 |                        16320.14 |                30637.00 |             249643 |                             300.00 |               250357 |                               286.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |        1 |               1 |           1 |       128 |    16384 |        0 |                        16354.83 |                61144.00 |             501109 |                             355.00 |               498891 |                               347.00 |
| dragonflycluster-1-1-2 | dragonflycluster-1-1-2 |                1 |        2 |               1 |           2 |       256 |    32768 |        0 |                        32616.87 |                30681.00 |             498913 |                             319.00 |               501087 |                               289.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        19.00 |                |
| dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 |                1 |        2 |               1 |        19.00 |                |

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
