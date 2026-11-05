## Show Summary

### Workload
YCSB SF=3
* Type: ycsb
* Duration: 744s 
* Code: 1793813426
* YCSB driver runs the experiment.
* This experiment compares run time and resource consumption of YCSB queries.
  * Workload is 'A'.
  * Number of rows to insert is 3000000.
  * Ordering of inserts is hashed.
  * Number of operations is 10000000.
  * Batch size is ''.
  * Target is based on multiples of '16384'.
  * Factors for loading are [12].
  * Factors for benchmarking are [4]. A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round.
  * Status is logged every 10s.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.12.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Garnet'].
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
  * Distributed DBMS uses 3 worker nodes, 0 replicas and 0 shards per node.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.

### Connections
* garnet-1-1-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:903953
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:604784
    * datadisk:1402
    * volume_size:49G
    * volume_used:1.4G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607495
    * datadisk:1774
    * volume_size:49G
    * volume_used:1.8G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:540597891072
    * CPU:Intel(R) Xeon(R) 6767P
    * Cores:256
    * host:6.8.0-137-generic
    * node:cl-worker39
    * disk:244977
    * datadisk:1404
    * volume_size:49G
    * volume_used:1.4G
    * cpu_list:0-255
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793813426
    * BEXHOMA_WORKERS:3
* garnet-1-2-1-1 uses docker image valkey/valkey:9.1.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:903957
  * datadisk:1
  * cpu_list:0-223
  * args:['--maxclients', '10000', '--io-threads', '64']
  * requests_cpu:4
  * requests_memory:64Gi
  * limits_memory:64Gi
  * worker 0
    * RAM:1081742753792
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-146-generic
    * node:cl-worker29
    * disk:604783
    * datadisk:1681
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 1
    * RAM:1081853952000
    * CPU:Intel(R) Xeon(R) Gold 6438Y+
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker37
    * disk:607497
    * datadisk:2067
    * volume_size:49G
    * volume_used:2.1G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * worker 2
    * RAM:540579299328
    * CPU:AMD EPYC 7502 32-Core Processor
    * Cores:128
    * host:6.8.0-137-generic
    * node:cl-worker22
    * disk:253305
    * datadisk:1690
    * volume_size:49G
    * volume_used:1.7G
    * cpu_list:0-127
    * args:['--port', '6379', '--cluster', '--cluster-preferred-endpoint-type', 'hostname', '--cluster-announce-hostname', '$(POD_NAME).bx-w-garnet-nvme-ycsb-3.$(POD_NAMESPACE).svc.cluster.local', '--checkpointdir', '/data/checkpoints', '--aof', '--aof-commit-freq', '1000', '--recover']
  * resources_total: 12.25 CPU, 192.5 GiB RAM requested in 4 pods
    * sut: 1 x, 0.25 CPU, 0.5 GiB RAM
    * worker: 3 x, 12.0 CPU, 192.0 GiB RAM
  * load_durability: relaxed
  * eval_parameters
    * code:1793813426
    * BEXHOMA_WORKERS:3

### Inherited Loading
* loading skipped, loading times copied from an earlier repetition: Garnet-1-2

### Data Parameters of Reused Volumes
* Garnet-1: loading values of the volume: script=Schema, indexing=Checks, insert_order=hashed

### Init Scripts Not in Folder
* Garnet-1: skipped checkschema-ycsb.sql, initschema-ycsb.sql

### SUT Container Restarts
* bexhoma-sut-garnet-1-1793813426-78956b9f65-xqbx6: 0
* bx-w-garnet-nvme-ycsb-3-0: 0
* bx-w-garnet-nvme-ycsb-3-1: 0
* bx-w-garnet-nvme-ycsb-3-2: 0
* bexhoma-sut-garnet-1-1793813426-665c6c7f4d-2jb7f: 0

### Workflow

#### Actual

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

#### Planned

* DBMS Garnet-1 - Experiment 1 Client 1: ycsb (1 pods)
* DBMS Garnet-1 - Experiment 2 Client 1: ycsb (1 pods)

### Loading

#### Per Connection

| connection       |   experiment_run |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |   sf |   Throughput [SF/h] |
|:-----------------|-----------------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|-----:|--------------------:|
| garnet-1-1-0-1-1 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13379.48 |                28028.00 |            375000.00 |                              1447.00 | 3.00 |              385.33 |
| garnet-1-1-0-1-2 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13386.64 |                28013.00 |            375000.00 |                              1425.00 | 3.00 |              385.54 |
| garnet-1-1-0-1-3 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13038.49 |                28761.00 |            375000.00 |                              1453.00 | 3.00 |              375.51 |
| garnet-1-1-0-1-4 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13337.60 |                28116.00 |            375000.00 |                              1431.00 | 3.00 |              384.12 |
| garnet-1-1-0-1-5 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        14131.21 |                26537.00 |            375000.00 |                              1459.00 | 3.00 |              406.98 |
| garnet-1-1-0-1-6 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13473.22 |                27833.00 |            375000.00 |                              1447.00 | 3.00 |              388.03 |
| garnet-1-1-0-1-7 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13750.37 |                27272.00 |            375000.00 |                              1447.00 | 3.00 |              396.01 |
| garnet-1-1-0-1-8 |             1.00 |      8.00 | 24576.00 |        8.00 |         0.00 |                        13606.18 |                27561.00 |            375000.00 |                              1466.00 | 3.00 |              391.86 |

#### Per Run

| DBMS       |   experiment_run |   threads |    target |   pod_count |   exceptions |   sf |   Throughput [SF/h] |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [INSERT].Return=OK |   [INSERT].99thPercentileLatency(us) |
|:-----------|-----------------:|----------:|----------:|------------:|-------------:|-----:|--------------------:|--------------------------------:|------------------------:|---------------------:|-------------------------------------:|
| Garnet-1-1 |             1.00 |     64.00 | 196608.00 |        8.00 |         0.00 | 3.00 |              375.51 |                       108103.19 |                28761.00 |           3000000.00 |                              1446.88 |

### Benchmarking

#### Per Connection

| DBMS             | phase        | job            | configuration   |   experiment_run |   client |   benchmark_run |   child |   threads |   target |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-----------------|:-------------|:---------------|:----------------|-----------------:|---------:|----------------:|--------:|----------:|---------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1-1-1 | garnet-1-1-1 | garnet-1-1-1-1 | Garnet-1        |                1 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        62398.21 |               160261.00 |            4998231 |                             857.00 |              5001769 |                               854.00 |
| garnet-1-2-1-1-1 | garnet-1-2-1 | garnet-1-2-1-1 | Garnet-1        |                2 |        1 |               1 |       1 |       128 |    65536 |           1 |            0 |                        61294.42 |               163147.00 |            5000499 |                             253.00 |              4999501 |                               247.00 |

#### Per Phase

| DBMS         | phase        |   experiment_run |   threads |   target |   benchmark_run |   pod_count |   exceptions |   [OVERALL].Throughput(ops/sec) |   [OVERALL].RunTime(ms) |   [READ].Return=OK |   [READ].99thPercentileLatency(us) |   [UPDATE].Return=OK |   [UPDATE].99thPercentileLatency(us) |
|:-------------|:-------------|-----------------:|----------:|---------:|----------------:|------------:|-------------:|--------------------------------:|------------------------:|-------------------:|-----------------------------------:|---------------------:|-------------------------------------:|
| garnet-1-1-1 | garnet-1-1-1 |                1 |       128 |    65536 |               1 |           1 |            0 |                        62398.21 |               160261.00 |            4998231 |                             857.00 |              5001769 |                               854.00 |
| garnet-1-2-1 | garnet-1-2-1 |                2 |       128 |    65536 |               1 |           1 |            0 |                        61294.42 |               163147.00 |            5000499 |                             253.00 |              4999501 |                               247.00 |

#### Reset

| phase        | job            |   experiment_run |   client |   benchmark_run |   time_reset | reset_failed   |
|:-------------|:---------------|-----------------:|---------:|----------------:|-------------:|:---------------|
| garnet-1-1-1 | garnet-1-1-1-1 |                1 |        1 |               1 |         8.00 |                |
| garnet-1-2-1 | garnet-1-2-1-1 |                2 |        1 |               1 |         8.00 |                |

### Monitoring

### Loading phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       815.72 |     22.38 |           9.49 |                  9.49 |

### Loading phase: component loader

| DBMS           | CPU [CPUs]   |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|:-------------|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 | n/a          |         0 |           1.04 |                  1.04 |

### Benchmarking phase: component worker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |      1079.19 |      7.85 |           9.70 |                  9.70 |
| garnet-1-2-1-1 |      1040.95 |      8.34 |           8.04 |                  8.05 |

### Benchmarking phase: component benchmarker

| DBMS           |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:---------------|-------------:|----------:|---------------:|----------------------:|
| garnet-1-1-1-1 |       766.39 |      5.25 |           1.49 |                  1.50 |
| garnet-1-2-1-1 |       736.43 |      4.93 |           1.50 |                  1.50 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Utilization [CPUs] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: job pods ran shorter than scrape interval)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-loader.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-1-1-1 (bexhoma-metrics-garnet-1-1-1-1-workerloading.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection garnet-1-2-1-1 (bexhoma-metrics-garnet-1-2-1-1-workerbenchmarking.log, expected: series exists only while non-zero)

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
