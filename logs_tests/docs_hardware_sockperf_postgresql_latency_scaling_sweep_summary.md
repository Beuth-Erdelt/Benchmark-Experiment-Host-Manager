## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 882s 
* Code: 1783818715
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
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
  * disk:1062854
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062854
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062855
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062856
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062856
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783818715-5dd5cb7499-qrc7t: 0

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
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8981.58 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.19 |                                0.25 |                              9071.91 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.21 |                                0.26 |                              8224.08 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.18 |                                0.22 |                              7981.43 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.04 |                               0.18 |                                0.22 |                              8544.53 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                              8445.59 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                              8434.48 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7597.16 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.07 |                               0.05 |                               0.21 |                                0.26 |                              6950.45 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7328.68 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.07 |                               0.05 |                               0.20 |                                0.25 |                              7165.44 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.05 |                               0.04 |                               0.19 |                                0.24 |                              9416.81 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.05 |                               0.21 |                                0.26 |                              7036.94 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.05 |                               0.21 |                                0.27 |                              6861.70 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7278.15 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7155.87 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.22 |                                0.27 |                              7992.73 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.07 |                               0.05 |                               0.23 |                                0.27 |                              7456.37 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                              6135.87 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6438.71 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              6656.89 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.05 |                               0.23 |                                0.28 |                              7364.32 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7100.54 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.07 |                               0.05 |                               0.24 |                                0.27 |                              7167.94 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7216.14 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.08 |                               0.06 |                               0.24 |                                0.28 |                              6573.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.07 |                               0.05 |                               0.23 |                                0.28 |                              7646.65 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6317.09 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                              6334.91 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.06 |                               0.05 |                               0.23 |                                0.27 |                              7858.59 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6430.76 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8981.58 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.05 |                               0.21 |                                0.26 |                             17295.99 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                             33406.03 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.07 |                               0.05 |                               0.21 |                                0.27 |                             59635.33 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                            111847.01 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         9.17 |      0.18 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        10.52 |      0.34 |           0.20 |                  0.20 |
| Hardware-1-1-3-1 |        24.70 |      0.66 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |        73.96 |      1.36 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       140.80 |      2.58 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.72 |      0.31 |           0.55 |                  0.55 |
| Hardware-1-1-2-1 |        31.04 |      0.93 |           0.55 |                  0.55 |
| Hardware-1-1-3-1 |        54.38 |      1.81 |           0.55 |                  0.55 |
| Hardware-1-1-4-1 |        99.45 |      3.42 |           0.55 |                  0.55 |
| Hardware-1-1-5-1 |       224.61 |      7.37 |           0.55 |                  0.55 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
