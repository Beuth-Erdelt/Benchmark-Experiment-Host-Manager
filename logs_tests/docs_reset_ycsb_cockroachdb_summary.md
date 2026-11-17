## Show Summary

### Workload
YCSB SF=1
* Type: ycsb
* Duration: 700s 
* Code: 1794821216
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
  * Experiment is limited to DBMS ['CockroachDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Loading is tested with [64] threads, split into [8] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1, 2] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * Distributed DBMS uses 3 worker nodes, 3 replicas and 0 shards per node.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* cockroachdb-1-1-1-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053306
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:647383
    * datadisk:2647
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:907122
    * datadisk:2263
    * cpu_list:0-255
  * worker 2
    * RAM:540597886976
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:302225
    * datadisk:2263
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794821216
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3
* cockroachdb-1-1-2-1 uses docker image cockroachdb/cockroach:v24.2.4
  * RAM:2164173156352
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1053307
  * cpu_list:0-223
  * args:['-c', 'while true; do echo hello; sleep 10;done']
  * requests_cpu:4
  * requests_memory:16Gi
  * worker 0
    * RAM:1081853952000
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:647950
    * datadisk:2876
    * cpu_list:0-127
  * worker 1
    * RAM:1077381263360
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker27
    * disk:906729
    * datadisk:2665
    * cpu_list:0-255
  * worker 2
    * RAM:540597886976
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:302631
    * datadisk:2667
    * cpu_list:0-255
  * resources_total: 12.25 CPU, 48.5 GiB RAM requested in 4 pods
    * worker: 3 x, 12.0 CPU, 48.0 GiB RAM
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1794821216
    * BEXHOMA_REPLICAS:3
    * BEXHOMA_WORKERS:3

### Ingestion
* CockroachDB-1: 8 of 8 units ok

### SUT Container Restarts
* bexhoma-sut-cockroachdb-1-1794821216-5c8fd64998-gr699: 0
* bx-w-cr-1-1794821216-0: 0
* bx-w-cr-1-1794821216-1: 0
* bx-w-cr-1-1794821216-2: 0

### Workflow

#### Actual

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: ycsb (2 pods)

#### Planned

* DBMS CockroachDB-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS CockroachDB-1 - Experiment 1 Client 2: ycsb (2 pods)

### Loading

#### Per Connection

| connection            |   experiment_run |   threads |   target |   pod_count |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   SF |   Throughput [SF/h] |
|:----------------------|-----------------:|----------:|---------:|------------:|---------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| cockroachdb-1-1-0-1-1 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1434.19 |                87157.00 |            125000.00 |                             17423.00 | 1.00 |               41.30 |
| cockroachdb-1-1-0-1-2 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1429.13 |                87466.00 |            125000.00 |                             17615.00 | 1.00 |               41.16 |
| cockroachdb-1-1-0-1-3 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1421.67 |                87925.00 |            125000.00 |                             17775.00 | 1.00 |               40.94 |
| cockroachdb-1-1-0-1-4 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1419.58 |                88054.00 |            125000.00 |                             17519.00 | 1.00 |               40.88 |
| cockroachdb-1-1-0-1-5 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1426.76 |                87611.00 |            125000.00 |                             17391.00 | 1.00 |               41.09 |
| cockroachdb-1-1-0-1-6 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1422.10 |                87898.00 |            125000.00 |                             17535.00 | 1.00 |               40.96 |
| cockroachdb-1-1-0-1-7 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1422.41 |                87879.00 |            125000.00 |                             17743.00 | 1.00 |               40.97 |
| cockroachdb-1-1-0-1-8 |             1.00 |      8.00 |  8192.00 |        8.00 |     0.00 |                         1418.84 |                88100.00 |            125000.00 |                             17663.00 | 1.00 |               40.86 |

#### Per Run

| DBMS            |   experiment_run |   threads |   target |   pod_count |   errors |   SF |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:----------------|-----------------:|----------:|---------:|------------:|---------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| CockroachDB-1-1 |             1.00 |     64.00 | 65536.00 |        8.00 |     0.00 | 1.00 |               40.86 |                        11394.69 |                88100.00 |           1000000.00 |                             17583.00 |

### Benchmarking

#### Per Connection

| connection            | phase             | job                 |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:----------------------|:------------------|:--------------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1-1-1 | cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |       1 |        64 |    16384 |        0 |                         9852.22 |               101500.00 |             499936 |                            8903.00 |               500064 |                            184447.00 |
| cockroachdb-1-1-2-1-1 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       1 |        64 |    16384 |        0 |                         4208.29 |               118813.00 |             250394 |                            9583.00 |               249606 |                            695807.00 |
| cockroachdb-1-1-2-1-2 | cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |       2 |        64 |    16384 |        0 |                         4158.77 |               120228.00 |             249187 |                            9599.00 |               250813 |                            695807.00 |

#### Per Phase

| DBMS              | phase             |   experiment_run |   client |   benchmark_run |   pod_count |   threads |   target |   errors |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:------------------|:------------------|-----------------:|---------:|----------------:|------------:|----------:|---------:|---------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| cockroachdb-1-1-1 | cockroachdb-1-1-1 |                1 |        1 |               1 |           1 |        64 |    16384 |        0 |                         9852.22 |               101500.00 |             499936 |                            8903.00 |               500064 |                            184447.00 |
| cockroachdb-1-1-2 | cockroachdb-1-1-2 |                1 |        2 |               1 |           2 |       128 |    32768 |        0 |                         8367.06 |               120228.00 |             499581 |                            9599.00 |               500419 |                            695807.00 |

#### Reset

| phase             | job                 |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:------------------|:--------------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| cockroachdb-1-1-1 | cockroachdb-1-1-1-1 |                1 |        1 |               1 |         6.00 |                |
| cockroachdb-1-1-2 | cockroachdb-1-1-2-1 |                1 |        2 |               1 |         6.00 |                |

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
