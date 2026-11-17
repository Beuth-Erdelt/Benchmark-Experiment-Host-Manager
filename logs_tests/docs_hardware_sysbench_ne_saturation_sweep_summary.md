## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 461s 
* Code: 1794941297
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4, 8] times the number of benchmarking pods.
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
  * disk:1058099
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941297
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058099
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941297
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058100
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941297
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058103
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941297

### SUT Container Restarts
* bexhoma-sut-hardware-1-1794941297-84c4c64d97-rbb8z: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |         2 |                                2242.93 |                                60.00 |                               1.27 |                             6164096.72 |                                     6019.63 |                                  0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         67 |         2 |                                1153.71 |                                60.03 |                               1.32 |                             2181080.82 |                                     2129.96 |                                  0.00 |        0 |
| hardware-1-1-2-1-2 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |         2 |                                1147.15 |                                60.00 |                               1.32 |                             2720159.00 |                                     2656.41 |                                  0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         78 |         2 |                                 564.68 |                                60.02 |                              20.00 |                              763422.13 |                                      745.53 |                                  0.00 |        0 |
| hardware-1-1-3-1-2 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         79 |         2 |                                 551.78 |                                60.00 |                              20.00 |                              739409.71 |                                      722.08 |                                  0.00 |        0 |
| hardware-1-1-3-1-3 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         76 |         2 |                                 542.62 |                                60.00 |                              20.00 |                              790123.46 |                                      771.60 |                                  0.00 |        0 |
| hardware-1-1-3-1-4 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         76 |         2 |                                 564.15 |                                60.00 |                              20.00 |                              710498.17 |                                      693.85 |                                  0.00 |        0 |
| hardware-1-1-4-1-1 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         85 |         2 |                                 274.11 |                                60.00 |                              58.92 |                              617805.92 |                                      603.33 |                                  0.00 |        0 |
| hardware-1-1-4-1-2 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         84 |         2 |                                 283.01 |                                60.00 |                              58.92 |                              608567.75 |                                      594.30 |                                  0.00 |        0 |
| hardware-1-1-4-1-3 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         80 |         2 |                                 279.81 |                                60.00 |                              58.92 |                              770844.32 |                                      752.78 |                                  0.00 |        0 |
| hardware-1-1-4-1-4 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         81 |         2 |                                 271.91 |                                60.00 |                              58.92 |                              666235.96 |                                      650.62 |                                  0.00 |        0 |
| hardware-1-1-4-1-5 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         81 |         2 |                                 276.73 |                                60.05 |                              58.92 |                              629754.26 |                                      614.99 |                                  0.00 |        0 |
| hardware-1-1-4-1-6 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         81 |         2 |                                 277.06 |                                60.00 |                              58.92 |                              641577.54 |                                      626.54 |                                  0.00 |        0 |
| hardware-1-1-4-1-7 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         77 |         2 |                                 280.69 |                                60.00 |                              58.92 |                              776317.86 |                                      758.12 |                                  0.00 |        0 |
| hardware-1-1-4-1-8 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         78 |         2 |                                 281.37 |                                60.02 |                              58.92 |                              679390.81 |                                      663.47 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |         2 |                                2242.93 |                                60.00 |                               1.27 |                             6164096.72 |                                     6019.63 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         67 |         4 |                                2300.86 |                                60.03 |                               1.32 |                             4901239.82 |                                     4786.37 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         79 |         8 |                                2223.23 |                                60.02 |                              20.00 |                             3003453.47 |                                     2933.06 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         85 |        16 |                                2224.69 |                                60.05 |                              58.92 |                             5390494.42 |                                     5264.15 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        90.25 |      1.99 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |        84.12 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        98.11 |      2.00 |           0.22 |                  0.22 |
| hardware-1-1-4-1 |       117.74 |      2.00 |           0.23 |                  0.23 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.61 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         1.23 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |         3.13 |      0.04 |           0.00 |                  0.00 |
| hardware-1-1-4-1 |         5.68 |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)

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
