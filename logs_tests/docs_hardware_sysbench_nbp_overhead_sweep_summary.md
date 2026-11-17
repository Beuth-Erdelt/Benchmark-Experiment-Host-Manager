## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 358s 
* Code: 1794940918
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058096
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794940918
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058097
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794940918
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058098
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794940918

### SUT Container Restarts
* bexhoma-sut-hardware-1-1794940918-5bb8d4bd6b-ldvhn: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |         4 |                                2225.01 |                                60.00 |                               1.30 |                             2792160.68 |                                     2726.72 |                                  0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |         2 |                                1144.08 |                                60.00 |                               1.32 |                             2754496.45 |                                     2689.94 |                                  0.00 |        0 |
| hardware-1-1-2-1-2 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |         2 |                                1118.96 |                                60.02 |                               1.32 |                             3010586.01 |                                     2940.03 |                                  0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |         1 |                                 574.07 |                                60.00 |                               1.32 |                             2956756.79 |                                     2887.46 |                                  0.00 |        0 |
| hardware-1-1-3-1-2 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |         1 |                                 571.88 |                                60.00 |                               1.32 |                             3047780.00 |                                     2976.35 |                                  0.00 |        0 |
| hardware-1-1-3-1-3 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |         1 |                                 571.94 |                                60.00 |                               1.32 |                             3056554.67 |                                     2984.92 |                                  0.00 |        0 |
| hardware-1-1-3-1-4 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |         1 |                                 575.77 |                                60.00 |                               1.32 |                             2941498.70 |                                     2872.56 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |         4 |                                2225.01 |                                60.00 |                               1.30 |                             2792160.68 |                                     2726.72 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |         4 |                                2263.04 |                                60.02 |                               1.32 |                             5765082.46 |                                     5629.97 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |         4 |                                2293.66 |                                60.00 |                               1.32 |                            12002590.16 |                                    11721.29 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        83.15 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |       112.97 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |       119.22 |      2.00 |           0.22 |                  0.22 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.61 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         1.29 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |         2.60 |      0.03 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
