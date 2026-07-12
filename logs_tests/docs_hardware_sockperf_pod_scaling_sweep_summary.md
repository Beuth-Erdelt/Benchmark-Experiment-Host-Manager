## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 920s 
* Code: 1783817286
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062847
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062847
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062848
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062849
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062850
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783817286-99d9447cf-5cq8c: 0

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

### Execution

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.21 |                               0.16 |                               0.81 |                                1.03 |                              5032.78 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.20 |                               0.14 |                               0.83 |                                1.69 |                              5095.58 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.15 |                               0.10 |                               0.60 |                                2.95 |                              4506.94 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.40 |                               0.34 |                               0.82 |                               20.44 |                              4343.30 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.16 |                               0.12 |                               0.63 |                                1.05 |                              4437.83 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.37 |                               0.34 |                               0.81 |                                1.16 |                              4243.78 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.20 |                               0.14 |                               0.72 |                                1.08 |                              4973.87 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.19 |                               0.14 |                               0.88 |                                6.12 |                              3747.07 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.19 |                               1.25 |                                7.79 |                              3557.04 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.16 |                               0.12 |                               0.74 |                                1.60 |                              3657.04 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.27 |                               0.18 |                               1.24 |                               14.63 |                              3505.14 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.24 |                               0.19 |                               0.98 |                                1.62 |                              4220.37 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.19 |                               0.13 |                               0.78 |                                8.84 |                              4222.38 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.16 |                               0.12 |                               0.72 |                                2.27 |                              3549.41 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.20 |                               0.14 |                               0.93 |                                3.23 |                              4112.23 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               4.80 |                               4.71 |                              10.89 |                               21.65 |                              3945.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.13 |                               1.61 |                                2.73 |                              3756.69 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               4.66 |                               4.69 |                               8.23 |                               12.11 |                              4026.99 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.25 |                               0.14 |                               1.62 |                                2.88 |                              3708.51 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         73 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               4.66 |                               4.68 |                               7.68 |                                8.67 |                              5286.58 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.27 |                               0.16 |                               1.67 |                                3.22 |                              3743.20 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               4.81 |                               4.81 |                               8.78 |                               13.02 |                              4859.74 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.22 |                               0.13 |                               1.52 |                                2.42 |                              2141.28 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.23 |                               0.15 |                               1.53 |                                2.69 |                              2139.93 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               4.76 |                               4.77 |                               8.52 |                               10.31 |                              5324.48 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               4.67 |                               4.69 |                               7.81 |                                8.99 |                              5285.36 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               0.22 |                               0.13 |                               1.52 |                                2.51 |                              2313.22 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               0.22 |                               0.13 |                               1.51 |                                2.44 |                              2440.36 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.24 |                               0.13 |                               1.67 |                                3.84 |                              3520.78 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               4.86 |                               4.76 |                              10.83 |                               15.46 |                              3992.93 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.23 |                               0.12 |                               1.62 |                                2.95 |                              3646.20 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                               0.21 |                               0.16 |                               0.81 |                                1.03 |                              5032.78 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.20 |                               0.14 |                               0.83 |                                2.95 |                              9602.53 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.40 |                               0.34 |                               0.82 |                               20.44 |                             17998.79 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.27 |                               0.19 |                               1.25 |                               14.63 |                             30570.69 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                               4.86 |                               4.81 |                              10.89 |                               21.65 |                             60131.90 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.54 |      0.19 |           0.20 |                  0.21 |
| Hardware-1-1-2-1 |        17.33 |      0.40 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        25.27 |      0.62 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |        81.32 |      1.65 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |        89.43 |      2.31 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        43.42 |      1.04 |           0.10 |                  0.10 |
| Hardware-1-1-2-1 |        66.02 |      2.95 |           0.10 |                  0.10 |
| Hardware-1-1-3-1 |       158.98 |      6.11 |           0.10 |                  0.10 |
| Hardware-1-1-4-1 |       181.08 |     12.16 |           0.10 |                  0.10 |
| Hardware-1-1-5-1 |       462.59 |     22.90 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
