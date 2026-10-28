## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 593s 
* Code: 1793243217
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 8, 16, 32, 64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363122
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363123
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363123
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363124
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793243217-67bd87489d-7nrgd: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         60 |                  1 | tcp                         |                             6253.52 |                              0.16 |                              0.07 |                              0.39 |                              0.47 |                                0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                  8 | tcp                         |                            59160.06 |                              0.21 |                              0.09 |                              0.45 |                              0.53 |                                0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 |                 16 | tcp                         |                           129741.72 |                              0.20 |                              0.08 |                              0.46 |                              0.60 |                                0.00 |        0 |
| hardware-1-1-4-1-1 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         65 |                 32 | tcp                         |                           351120.10 |                              0.17 |                              0.08 |                              0.45 |                              0.55 |                                0.00 |        0 |
| hardware-1-1-5-1-1 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         68 |                 64 | tcp                         |                           776966.99 |                              0.13 |                              0.09 |                              0.38 |                              0.54 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         60 |                  1 | tcp                         |                             6253.52 |                              0.16 |                              0.07 |                              0.39 |                              0.47 |                                0.00 |        0 | netperf         |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                  8 | tcp                         |                            59160.06 |                              0.21 |                              0.09 |                              0.45 |                              0.53 |                                0.00 |        0 | netperf         |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 |                 16 | tcp                         |                           129741.72 |                              0.20 |                              0.08 |                              0.46 |                              0.60 |                                0.00 |        0 | netperf         |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           1 |         65 |                 32 | tcp                         |                           351120.10 |                              0.17 |                              0.08 |                              0.44 |                              0.55 |                                0.00 |        0 | netperf         |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |           1 |         68 |                 64 | tcp                         |                           776966.99 |                              0.13 |                              0.09 |                              0.38 |                              0.54 |                                0.00 |        0 | netperf         |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         6.52 |      0.13 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |        33.94 |      0.97 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        92.94 |      2.03 |           0.21 |                  0.21 |
| hardware-1-1-4-1 |       274.13 |      5.00 |           0.21 |                  0.21 |
| hardware-1-1-5-1 |       571.83 |     10.57 |           0.22 |                  0.22 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         8.48 |      0.25 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |        67.19 |      1.82 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |        93.40 |      3.52 |           0.01 |                  0.01 |
| hardware-1-1-4-1 |       235.79 |      6.15 |           0.01 |                  0.01 |
| hardware-1-1-5-1 |       438.66 |     13.06 |           0.02 |                  0.02 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
