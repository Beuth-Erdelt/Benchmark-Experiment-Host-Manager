## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 623s 
* Code: 1793244151
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
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
  * disk:363127
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363128
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363128
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363129
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363327
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793244151-869c87cd7c-dqpvw: 0

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
| hardware-1-1-1-1-1  | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                  1 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.44 |                               0.42 |                               0.77 |                                1.91 |                              9252.41 |                                0.00 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.44 |                               0.36 |                               0.85 |                               27.21 |                             10830.26 |                                0.00 |        0 |
| hardware-1-1-2-1-2  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.45 |                               0.37 |                               2.14 |                               14.01 |                             10063.04 |                                0.00 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.40 |                               0.38 |                               0.95 |                                3.32 |                             10399.95 |                                0.00 |        0 |
| hardware-1-1-3-1-2  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.40 |                               0.37 |                               0.75 |                                9.28 |                              9912.96 |                                0.00 |        0 |
| hardware-1-1-3-1-3  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.50 |                               0.38 |                               4.94 |                               16.26 |                              9488.06 |                                0.00 |        0 |
| hardware-1-1-3-1-4  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.44 |                               0.43 |                               0.81 |                                2.30 |                              8417.20 |                                0.00 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.81 |                               0.41 |                              16.88 |                               43.07 |                              7782.85 |                                0.00 |        0 |
| hardware-1-1-4-1-2  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.45 |                               0.43 |                               0.89 |                                1.61 |                              8367.50 |                                0.00 |        0 |
| hardware-1-1-4-1-3  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.42 |                               0.41 |                               0.89 |                                1.72 |                              6935.79 |                                0.00 |        0 |
| hardware-1-1-4-1-4  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.45 |                               0.39 |                               1.00 |                               20.12 |                              6958.56 |                                0.00 |        0 |
| hardware-1-1-4-1-5  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.45 |                               0.39 |                               2.23 |                                6.46 |                              8387.32 |                                0.00 |        0 |
| hardware-1-1-4-1-6  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.71 |                               0.43 |                              12.90 |                               25.94 |                              7902.44 |                                0.00 |        0 |
| hardware-1-1-4-1-7  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.58 |                               0.41 |                               3.29 |                               30.59 |                              6955.55 |                                0.00 |        0 |
| hardware-1-1-4-1-8  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.40 |                               0.39 |                               0.79 |                                2.21 |                              8525.09 |                                0.00 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         76 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.48 |                               0.45 |                               1.02 |                                4.79 |                              6152.54 |                                0.00 |        0 |
| hardware-1-1-5-1-2  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.50 |                               0.41 |                               1.35 |                               21.84 |                              7303.27 |                                0.00 |        0 |
| hardware-1-1-5-1-3  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.50 |                               0.37 |                               2.68 |                               21.54 |                             10424.57 |                                0.00 |        0 |
| hardware-1-1-5-1-4  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.63 |                               0.27 |                               7.69 |                               28.30 |                              8436.13 |                                0.00 |        0 |
| hardware-1-1-5-1-5  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.52 |                               0.38 |                               2.68 |                               21.52 |                              7669.17 |                                0.00 |        0 |
| hardware-1-1-5-1-6  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.56 |                               0.45 |                               2.04 |                               20.07 |                              7540.68 |                                0.00 |        0 |
| hardware-1-1-5-1-7  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.90 |                               0.27 |                               9.64 |                               40.42 |                              6530.85 |                                0.00 |        0 |
| hardware-1-1-5-1-8  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               1.14 |                               0.28 |                              20.19 |                               23.92 |                              7639.16 |                                0.00 |        0 |
| hardware-1-1-5-1-9  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.43 |                               0.38 |                               1.13 |                               11.62 |                              6565.58 |                                0.00 |        0 |
| hardware-1-1-5-1-10 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               0.47 |                               0.40 |                               1.15 |                               14.60 |                              8829.54 |                                0.00 |        0 |
| hardware-1-1-5-1-11 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               0.45 |                               0.41 |                               0.97 |                               10.47 |                              7806.15 |                                0.00 |        0 |
| hardware-1-1-5-1-12 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               0.51 |                               0.38 |                               1.10 |                               24.92 |                              7255.52 |                                0.00 |        0 |
| hardware-1-1-5-1-13 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               0.35 |                               0.31 |                               0.78 |                                5.94 |                              8654.83 |                                0.00 |        0 |
| hardware-1-1-5-1-14 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.69 |                               0.30 |                               7.12 |                               22.81 |                              6340.31 |                                0.00 |        0 |
| hardware-1-1-5-1-15 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               0.97 |                               0.31 |                              21.86 |                               35.13 |                              5937.63 |                                0.00 |        0 |
| hardware-1-1-5-1-16 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.75 |                               0.27 |                               6.99 |                               22.26 |                              7085.74 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                  1 | ul                       | tcp                          |                          64 | max                     |                               0.44 |                               0.42 |                               0.77 |                                1.91 |                              9252.41 |                                0.00 |        0 | sockperf        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.45 |                               0.37 |                               2.14 |                               27.21 |                             20893.30 |                                0.00 |        0 | sockperf        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.50 |                               0.43 |                               4.94 |                               16.26 |                             38218.18 |                                0.00 |        0 | sockperf        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.81 |                               0.43 |                              16.88 |                               43.07 |                             61815.09 |                                0.00 |        0 | sockperf        |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |          16 |         76 |                  0 | ul                       | tcp                          |                          64 | max                     |                               1.14 |                               0.45 |                              21.86 |                               40.42 |                            120171.68 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         4.34 |      0.12 |           0.20 |                  0.20 |
| hardware-1-1-2-1 |        14.63 |      0.27 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        34.54 |      0.69 |           0.21 |                  0.21 |
| hardware-1-1-4-1 |        35.65 |      0.98 |           0.21 |                  0.21 |
| hardware-1-1-5-1 |       135.65 |      2.79 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        39.47 |      1.06 |           0.10 |                  0.10 |
| hardware-1-1-2-1 |        81.00 |      2.10 |           0.10 |                  0.10 |
| hardware-1-1-3-1 |       210.65 |      4.44 |           0.10 |                  0.10 |
| hardware-1-1-4-1 |       437.32 |      8.76 |           0.10 |                  0.10 |
| hardware-1-1-5-1 |       717.16 |     17.49 |           0.10 |                  0.10 |

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
