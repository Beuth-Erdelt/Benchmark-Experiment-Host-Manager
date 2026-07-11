## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 891s 
* Code: 1783790109
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
  * disk:1062671
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783790109
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062690
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783790109
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062695
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783790109
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062700
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783790109
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062707
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783790109

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783790109-7f994c455-9nlsj: 0

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
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.16 |                               0.10 |                               0.68 |                                1.09 |                              5168.09 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.15 |                               0.10 |                               0.67 |                                1.03 |                              4995.82 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.15 |                               1.01 |                                1.22 |                              5235.00 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.42 |                               0.40 |                               0.85 |                                1.11 |                              4388.16 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.18 |                               0.11 |                               0.89 |                                1.18 |                              4518.15 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.41 |                               0.39 |                               0.84 |                                1.08 |                              4402.50 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.19 |                               0.10 |                               0.83 |                                1.09 |                              5038.09 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.17 |                               0.12 |                               0.78 |                                1.48 |                              4178.37 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.19 |                               0.13 |                               0.93 |                                1.94 |                              4158.27 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.15 |                               0.10 |                               0.71 |                                1.39 |                              4125.47 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.14 |                               0.10 |                               0.68 |                                1.44 |                              3921.14 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.18 |                               0.12 |                               0.95 |                                2.47 |                              4012.24 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.17 |                               0.11 |                               0.83 |                                1.42 |                              4095.31 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.19 |                               0.13 |                               0.98 |                                2.40 |                              3678.49 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.18 |                               0.12 |                               0.89 |                                1.57 |                              4135.77 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.47 |                               0.40 |                               1.77 |                                3.47 |                              3758.02 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.17 |                               1.64 |                                3.64 |                              2711.89 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.27 |                               0.16 |                               1.59 |                                2.71 |                              3708.30 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         73 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.35 |                               0.22 |                               2.16 |                                4.66 |                              2561.67 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.30 |                               0.20 |                               1.69 |                                3.16 |                              3725.46 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.24 |                               0.14 |                               1.57 |                                2.80 |                              3346.77 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.46 |                               0.39 |                               1.74 |                                3.02 |                              2694.59 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.26 |                               0.17 |                               1.59 |                                2.77 |                              3490.86 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.54 |                               0.47 |                               1.80 |                                3.02 |                              3619.76 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               0.24 |                               0.15 |                               1.64 |                                3.38 |                              2510.28 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               0.24 |                               0.13 |                               1.67 |                                6.78 |                              2627.00 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               0.30 |                               0.20 |                               1.67 |                                3.17 |                              3721.61 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               0.23 |                               0.14 |                               1.57 |                                2.77 |                              2639.66 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.47 |                               0.40 |                               1.70 |                                3.70 |                              3624.96 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               0.23 |                               0.14 |                               1.55 |                                2.89 |                              3655.23 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.27 |                               0.18 |                               1.61 |                                3.17 |                              3720.24 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                               0.16 |                               0.10 |                               0.68 |                                1.09 |                              5168.09 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.26 |                               0.15 |                               1.01 |                                1.22 |                             10230.81 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.42 |                               0.40 |                               0.89 |                                1.18 |                             18346.90 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.19 |                               0.13 |                               0.98 |                                2.47 |                             32305.07 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.54 |                               0.47 |                               2.16 |                                6.78 |                             52116.30 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        15.38 |      0.28 |           0.20 |                  0.21 |
| Hardware-1-1-2-1 |        31.85 |      0.55 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        20.03 |      0.64 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |       104.17 |      1.76 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       147.62 |      2.76 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        38.82 |      1.05 |           0.10 |                  0.10 |
| Hardware-1-1-2-1 |        60.00 |      2.94 |           0.10 |                  0.10 |
| Hardware-1-1-3-1 |       114.21 |      6.57 |           0.10 |                  0.10 |
| Hardware-1-1-4-1 |       372.59 |     12.23 |           0.10 |                  0.10 |
| Hardware-1-1-5-1 |       764.53 |     25.39 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
