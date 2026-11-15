## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 513s 
* Code: 1794619306
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 1000000.
  * Ordering of inserts is hashed.
  * Number of operations is 1000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [1].
  * Factors for benchmarking are [1].
  * Status is logged every 10s.
  * TiDB uses 3 SUT replica(s) and 3 PD node(s).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * Experiment is limited to DBMS ['TiDB'].
  * Import is handled by 8 processes (pods).
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* tidb-1-1-1-1 uses docker image pingcap/tidb:v8.5.8
  * RAM:1077381263360
  * CPU:AMD EPYC 7742 64-Core Processor
  * Cores:256
  * host:6.8.0-137-generic
  * node:cl-worker27
  * disk:671783
  * cpu_list:0-255
  * requests_cpu:4
  * requests_memory:16Gi
  * sut 0
    * RAM:1077381263360
    * CPU:AMD EPYC 7742 64-Core Processor
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:671783
    * cpu_list:0-255
  * sut 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:653329
    * cpu_list:0-127
  * sut 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1323296
    * cpu_list:0-127
  * pd 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:653330
    * datadisk:123
    * cpu_list:0-127
  * pd 1
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:164758
    * datadisk:123
    * cpu_list:0-95
  * pd 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1323296
    * datadisk:123
    * cpu_list:0-127
  * tikv 0
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:653329
    * datadisk:12037
    * cpu_list:0-127
  * tikv 1
    * RAM:540590792704
    * CPU:AMD EPYC 7352 24-Core Processor
    * Cores:96
    * host:6.8.0-146-generic
    * node:cl-worker25
    * disk:164758
    * datadisk:5260
    * cpu_list:0-95
  * tikv 2
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:1323296
    * datadisk:21043
    * cpu_list:0-127
  * resources_total: 24.75 CPU, 97.5 GiB RAM requested in 9 pods
    * pd: 3 x, 0.75 CPU, 1.5 GiB RAM
    * tikv: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 3 x, 12.0 CPU, 48.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794619306
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* TiDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-tidb-1-1794619306-658546c4c7-dszsj: 0
* bexhoma-sut-tidb-1-1794619306-658546c4c7-pxrwg: 0
* bexhoma-sut-tidb-1-1794619306-658546c4c7-qdqqs: 0
* bx-pd-ti-1-1794619306-0: 0
* bx-pd-ti-1-1794619306-1: 0
* bx-pd-ti-1-1794619306-2: 0
* bx-tikv-ti-1-1794619306-0: 0
* bx-tikv-ti-1-1794619306-1: 0
* bx-tikv-ti-1-1794619306-2: 0

### Workflow

#### Actual

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

#### Planned

* DBMS TiDB-1 - Experiment 1 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection     |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:---------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| tidb-1-1-0-1-1 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1300.70 |                96102.00 |            125000.00 |                             23935.00 | 1.00 |               37.46 |
| tidb-1-1-0-1-2 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1301.35 |                96054.00 |            125000.00 |                             23999.00 | 1.00 |               37.48 |
| tidb-1-1-0-1-3 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1300.84 |                96092.00 |            125000.00 |                             24543.00 | 1.00 |               37.46 |
| tidb-1-1-0-1-4 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1303.94 |                95863.00 |            125000.00 |                             24207.00 | 1.00 |               37.55 |
| tidb-1-1-0-1-5 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1300.73 |                96100.00 |            125000.00 |                             24863.00 | 1.00 |               37.46 |
| tidb-1-1-0-1-6 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1301.66 |                96031.00 |            125000.00 |                             23679.00 | 1.00 |               37.49 |
| tidb-1-1-0-1-7 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1302.35 |                95980.00 |            125000.00 |                             24367.00 | 1.00 |               37.51 |
| tidb-1-1-0-1-8 |             1.00 |      8.00 |  2048.00 |        8.00 |     0.00 |                         1299.98 |                96155.00 |            125000.00 |                             24639.00 | 1.00 |               37.44 |

#### Per Run

| DBMS     |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:---------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| TiDB-1-1 |             1.00 |     64.00 | 16384.00 |        8.00 |     0.00 | 1.00 |               37.44 |                        10411.56 |                96155.00 |           1000000.00 |                             24279.00 |

### Benchmarking

#### Per Connection

| connection     | phase      | job          |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:---------------|:-----------|:-------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1-1-1 | tidb-1-1-1 | tidb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    16384 |        0 |                        11462.63 |                87240.00 |             500686 |                            3557.00 |               499314 |                            120575.00 |

#### Per Phase

| DBMS       | phase      |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------|:-----------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| tidb-1-1-1 | tidb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    16384 |        0 |                        11462.63 |                87240.00 |             500686 |                            3557.00 |               499314 |                            120575.00 |

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
