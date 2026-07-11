## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 865s 
* Code: 1783791515
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
  * disk:1062741
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783791515
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062746
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783791515
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062751
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783791515
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062758
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783791515
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062764
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783791515

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783791515-696495dd79-njmcn: 0

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
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.05 |                               0.04 |                               0.20 |                                0.90 |                              9607.15 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.05 |                               0.22 |                                1.41 |                              8214.41 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.21 |                                1.34 |                              8256.71 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.05 |                               0.18 |                                1.52 |                              8565.91 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.22 |                                1.55 |                              8195.47 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.06 |                               0.05 |                               0.20 |                                1.06 |                              8849.52 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.05 |                               0.05 |                               0.19 |                                1.05 |                              9145.58 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.05 |                               0.21 |                                1.12 |                              8566.25 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.20 |                                1.36 |                              8878.46 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.06 |                               0.05 |                               0.19 |                                1.47 |                              8714.00 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.06 |                               0.05 |                               0.20 |                                1.28 |                              8622.70 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.06 |                               0.05 |                               0.21 |                                1.11 |                              8202.70 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.06 |                               0.05 |                               0.20 |                                1.53 |                              8068.83 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.06 |                               0.05 |                               0.20 |                                0.97 |                              8137.33 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.06 |                               0.05 |                               0.19 |                                1.46 |                              8187.10 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.24 |                                1.55 |                              7424.84 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.08 |                               0.06 |                               0.36 |                                1.48 |                              6300.17 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.08 |                               0.06 |                               0.35 |                                1.34 |                              5870.75 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.06 |                               0.06 |                               0.17 |                                1.17 |                              7744.01 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.07 |                               0.06 |                               0.25 |                                1.48 |                              6894.79 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.06 |                               0.05 |                               0.22 |                                1.41 |                              7943.16 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.08 |                               0.06 |                               0.37 |                                1.47 |                              5951.30 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.05 |                               0.25 |                                1.29 |                              7405.03 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.08 |                               0.06 |                               0.35 |                                1.45 |                              6161.08 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.07 |                               0.06 |                               0.25 |                                1.34 |                              7072.43 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.07 |                               0.06 |                               0.24 |                                1.36 |                              7193.84 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.07 |                               0.06 |                               0.23 |                                1.20 |                              6963.26 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.07 |                               0.06 |                               0.24 |                                1.23 |                              6885.86 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.09 |                               0.07 |                               0.37 |                                1.53 |                              5766.90 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.08 |                               0.06 |                               0.27 |                                1.34 |                              6562.75 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.08 |                               0.06 |                               0.37 |                                1.43 |                              6009.30 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.05 |                               0.04 |                               0.20 |                                0.90 |                              9607.15 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.05 |                               0.22 |                                1.41 |                             16471.12 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.05 |                               0.22 |                                1.55 |                             34756.47 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.05 |                               0.21 |                                1.53 |                             67377.38 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.09 |                               0.07 |                               0.37 |                                1.55 |                            108149.46 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         7.14 |      0.19 |           0.20 |                  0.20 |
| Hardware-1-1-2-1 |        13.44 |      0.31 |           0.20 |                  0.20 |
| Hardware-1-1-3-1 |        33.89 |      0.65 |           0.20 |                  0.20 |
| Hardware-1-1-4-1 |        43.01 |      1.35 |           0.20 |                  0.20 |
| Hardware-1-1-5-1 |        51.38 |      2.10 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        21.77 |      0.36 |           0.55 |                  0.55 |
| Hardware-1-1-2-1 |        22.22 |      1.09 |           0.55 |                  0.55 |
| Hardware-1-1-3-1 |        56.96 |      2.24 |           0.55 |                  0.55 |
| Hardware-1-1-4-1 |        74.68 |      4.23 |           0.55 |                  0.55 |
| Hardware-1-1-5-1 |       318.98 |      8.77 |           0.56 |                  0.56 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
