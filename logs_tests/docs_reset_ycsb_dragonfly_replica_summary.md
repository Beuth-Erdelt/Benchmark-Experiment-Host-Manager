## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 672s 
* Code: 1792633563
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
  * Experiment uses bexhoma version 0.11.7.
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
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:907412
  * datadisk:1
  * volume_size:1.8T
  * volume_used:887G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:267933
    * datadisk:1087
    * volume_size:550G
    * volume_used:262G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:543732
    * datadisk:1087
    * volume_size:879G
    * volume_used:531G
    * cpu_list:0-127
  * worker 2
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:151684
    * datadisk:1086
    * volume_size:219G
    * volume_used:149G
    * cpu_list:0-95
  * resources_total: 13.0 CPU, 49.0 GiB RAM requested in 4 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792633563
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3
* dragonflycluster-1-1-2-1 uses docker image docker.dragonflydb.io/dragonflydb/dragonfly:v2.0.2
  * RAM:2164173172736
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-137-generic
  * node:cl-worker36
  * disk:907414
  * datadisk:1
  * volume_size:1.8T
  * volume_used:887G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:267291
    * datadisk:1087
    * volume_size:550G
    * volume_used:262G
    * cpu_list:0-127
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:543732
    * datadisk:1087
    * volume_size:879G
    * volume_used:531G
    * cpu_list:0-127
  * worker 2
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:151684
    * datadisk:1086
    * volume_size:219G
    * volume_used:149G
    * cpu_list:0-95
  * resources_total: 13.0 CPU, 49.0 GiB RAM requested in 4 pods
    * sut: 1 x, 1.0 CPU, 1.0 GiB RAM
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1792633563
    * BEXHOMA_REPLICAS:1
    * BEXHOMA_WORKERS:3

### SUT Container Restarts
* bexhoma-sut-dragonflycluster-1-1792633563-6875d94cb4-vhptg: 0
* bx-w-dragonfly-ycsb-1-0: 0
* bx-w-dragonfly-ycsb-1-1: 0
* bx-w-dragonfly-ycsb-1-2: 0

### Workflow

#### Actual

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 1 Client 2: ycsb (2 pods)

#### Planned

* DBMS DragonflyCluster-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS DragonflyCluster-1 - Experiment 1 Client 2: ycsb (2 pods)

### Loading

#### Per Connection

| connection                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:---------------------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| dragonflycluster-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8163.00 |                15313.00 |            125000.00 |                               992.00 | 1.00 |              235.09 |
| dragonflycluster-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8161.40 |                15316.00 |            125000.00 |                               925.00 | 1.00 |              235.05 |
| dragonflycluster-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8156.07 |                15326.00 |            125000.00 |                               946.00 | 1.00 |              234.89 |
| dragonflycluster-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8158.20 |                15322.00 |            125000.00 |                               956.00 | 1.00 |              234.96 |
| dragonflycluster-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8163.00 |                15313.00 |            125000.00 |                               995.00 | 1.00 |              235.09 |
| dragonflycluster-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8159.27 |                15320.00 |            125000.00 |                               906.00 | 1.00 |              234.99 |
| dragonflycluster-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8160.87 |                15317.00 |            125000.00 |                               937.00 | 1.00 |              235.03 |
| dragonflycluster-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |         0.00 |                         8161.93 |                15315.00 |            125000.00 |                               937.00 | 1.00 |              235.06 |

#### Per Run

| DBMS                 |   experiment_run |   threads |   target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------------------|-----------------:|----------:|---------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| DragonflyCluster-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |         0.00 | 1.00 |              234.89 |                        65283.74 |                15326.00 |           1000000.00 |                               949.25 |

### Benchmarking

#### Per Connection

| DBMS                       | phase                  | job                      | configuration      |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------------------|:-----------------------|:-------------------------|:-------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1-1-1 | dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 | DragonflyCluster-1 |                1 |        1 |               1 |       1 |       128 |    16384 |           1 |            0 |                        16340.40 |                61198.00 |             499641 |                             530.00 |               500359 |                               506.00 |
| dragonflycluster-1-1-2-1-1 | dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 | DragonflyCluster-1 |                1 |        2 |               1 |       1 |       128 |    16384 |           2 |            0 |                        16314.81 |                30647.00 |             249172 |                             420.00 |               250828 |                               382.00 |
| dragonflycluster-1-1-2-1-2 | dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 | DragonflyCluster-1 |                1 |        2 |               1 |       2 |       128 |    16384 |           2 |            0 |                        16307.89 |                30660.00 |             249973 |                             445.00 |               250027 |                               388.00 |

#### Per Phase

| DBMS                   | phase                  |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------------|:-----------------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1 |                1 |       128 |    16384 |               1 |           1 |            0 |                        16340.40 |                61198.00 |             499641 |                             530.00 |               500359 |                               506.00 |
| dragonflycluster-1-1-2 | dragonflycluster-1-1-2 |                1 |       256 |    32768 |               1 |           2 |            0 |                        32622.70 |                30660.00 |             499145 |                             445.00 |               500855 |                               388.00 |

#### Reset

| phase                  | job                      |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-----------------------|:-------------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| dragonflycluster-1-1-1 | dragonflycluster-1-1-1-1 |                1 |        1 |               1 |        88.00 |                |
| dragonflycluster-1-1-2 | dragonflycluster-1-1-2-1 |                1 |        2 |               1 |        99.00 |                |

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Loading Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Execution Phase: [OVERALL].Throughput(ops/sec) contains no 0 or NaN
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: contains no FAILED column
* TEST passed: Reset scripts ran without errors
