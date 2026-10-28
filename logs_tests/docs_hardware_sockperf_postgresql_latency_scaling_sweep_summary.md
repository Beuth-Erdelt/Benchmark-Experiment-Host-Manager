## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 623s 
* Code: 1793245151
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
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
  * disk:363133
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363331
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363160
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363221
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363221
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793245151-7d87d85bd7-k8kn6: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

### Benchmarking

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1  | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.04 |                               0.23 |                                0.27 |                              6749.86 |                                0.00 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                              6359.14 |                                0.00 |        0 |
| hardware-1-1-2-1-2  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                              6219.71 |                                0.00 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.04 |                               0.24 |                                0.28 |                              7489.42 |                                0.00 |        0 |
| hardware-1-1-3-1-2  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.09 |                               0.04 |                               0.25 |                                0.28 |                              5792.98 |                                0.00 |        0 |
| hardware-1-1-3-1-3  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.04 |                               0.03 |                               0.17 |                                0.25 |                             13741.78 |                                0.00 |        0 |
| hardware-1-1-3-1-4  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.09 |                               0.04 |                               0.25 |                                0.29 |                              5776.89 |                                0.00 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.08 |                               0.04 |                               0.25 |                                0.29 |                              6597.88 |                                0.00 |        0 |
| hardware-1-1-4-1-2  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.05 |                               0.03 |                               0.23 |                                0.28 |                              9656.19 |                                0.00 |        0 |
| hardware-1-1-4-1-3  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.04 |                               0.03 |                               0.18 |                                0.24 |                             13907.59 |                                0.00 |        0 |
| hardware-1-1-4-1-4  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.07 |                               0.04 |                               0.25 |                                0.29 |                              7615.82 |                                0.00 |        0 |
| hardware-1-1-4-1-5  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.07 |                               0.04 |                               0.26 |                                0.29 |                              7217.13 |                                0.00 |        0 |
| hardware-1-1-4-1-6  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.04 |                               0.25 |                                0.29 |                              6848.92 |                                0.00 |        0 |
| hardware-1-1-4-1-7  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.06 |                               0.04 |                               0.24 |                                0.28 |                              8930.63 |                                0.00 |        0 |
| hardware-1-1-4-1-8  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.08 |                               0.04 |                               0.25 |                                0.29 |                              6366.92 |                                0.00 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         77 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.03 |                               0.27 |                                0.32 |                              8505.81 |                                0.00 |        0 |
| hardware-1-1-5-1-2  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.03 |                               0.27 |                                0.32 |                              8589.85 |                                0.00 |        0 |
| hardware-1-1-5-1-3  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.08 |                               0.04 |                               0.29 |                                0.33 |                              6106.05 |                                0.00 |        0 |
| hardware-1-1-5-1-4  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.05 |                               0.03 |                               0.27 |                                0.32 |                              9088.58 |                                0.00 |        0 |
| hardware-1-1-5-1-5  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.04 |                               0.03 |                               0.25 |                                0.31 |                             11387.69 |                                0.00 |        0 |
| hardware-1-1-5-1-6  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.10 |                               0.04 |                               0.29 |                                0.34 |                              5125.05 |                                0.00 |        0 |
| hardware-1-1-5-1-7  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.04 |                               0.29 |                                0.33 |                              6692.01 |                                0.00 |        0 |
| hardware-1-1-5-1-8  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.04 |                               0.27 |                                0.32 |                              6959.28 |                                0.00 |        0 |
| hardware-1-1-5-1-9  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.08 |                               0.04 |                               0.29 |                                0.34 |                              5892.48 |                                0.00 |        0 |
| hardware-1-1-5-1-10 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.11 |                               0.04 |                               0.30 |                                0.34 |                              4690.80 |                                0.00 |        0 |
| hardware-1-1-5-1-11 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.07 |                               0.04 |                               0.28 |                                0.33 |                              7290.48 |                                0.00 |        0 |
| hardware-1-1-5-1-12 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.05 |                               0.03 |                               0.25 |                                0.32 |                              9522.79 |                                0.00 |        0 |
| hardware-1-1-5-1-13 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.09 |                               0.04 |                               0.29 |                                0.34 |                              5453.67 |                                0.00 |        0 |
| hardware-1-1-5-1-14 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.08 |                               0.03 |                               0.29 |                                0.33 |                              6524.21 |                                0.00 |        0 |
| hardware-1-1-5-1-15 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.04 |                               0.03 |                               0.20 |                                0.28 |                             13186.28 |                                0.00 |        0 |
| hardware-1-1-5-1-16 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.07 |                               0.04 |                               0.28 |                                0.32 |                              7618.00 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.07 |                               0.04 |                               0.23 |                                0.27 |                              6749.86 |                                0.00 |        0 | sockperf        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                             12578.86 |                                0.00 |        0 | sockperf        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.09 |                               0.04 |                               0.25 |                                0.29 |                             32801.07 |                                0.00 |        0 | sockperf        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.04 |                               0.26 |                                0.29 |                             67141.07 |                                0.00 |        0 | sockperf        |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |          16 |         77 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.11 |                               0.04 |                               0.30 |                                0.34 |                            122633.02 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         6.07 |      0.15 |           0.20 |                  0.20 |
| hardware-1-1-2-1 |        13.42 |      0.26 |           0.20 |                  0.20 |
| hardware-1-1-3-1 |        31.05 |      0.56 |           0.20 |                  0.20 |
| hardware-1-1-4-1 |        58.87 |      1.15 |           0.20 |                  0.20 |
| hardware-1-1-5-1 |       101.34 |      1.99 |           0.20 |                  0.20 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        14.37 |      0.26 |           0.55 |                  0.55 |
| hardware-1-1-2-1 |        15.75 |      0.50 |           0.55 |                  0.55 |
| hardware-1-1-3-1 |        37.51 |      0.98 |           0.55 |                  0.55 |
| hardware-1-1-4-1 |        80.88 |      1.88 |           0.55 |                  0.55 |
| hardware-1-1-5-1 |       133.86 |      3.72 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
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
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
