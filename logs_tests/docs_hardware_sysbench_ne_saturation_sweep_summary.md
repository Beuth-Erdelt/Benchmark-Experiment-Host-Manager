## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 730s 
* Code: 1783814697
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4, 8] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062818
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062819
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062820
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062820
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783814697-69c476b458-24skd: 0

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

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                  2 |                                2327.85 |                                60.00 |                               1.25 |                             4519198.20 |                                     4413.28 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  2 |                                1196.63 |                                60.00 |                               1.30 |                             3496153.84 |                                     3414.21 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         69 |                  2 |                                1182.24 |                                60.00 |                               1.30 |                             1574692.31 |                                     1537.79 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         72 |                  2 |                                 595.38 |                                60.00 |                               7.98 |                             1450708.98 |                                     1416.71 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         75 |                  2 |                                 610.61 |                                60.07 |                               7.98 |                              912273.03 |                                      890.89 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         72 |                  2 |                                 612.80 |                                60.00 |                               7.98 |                             1153357.27 |                                     1126.33 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         72 |                  2 |                                 604.80 |                                60.00 |                               7.98 |                             1024798.28 |                                     1000.78 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         78 |                  2 |                                 298.69 |                                60.01 |                              80.03 |                              852319.94 |                                      832.34 |                                  0.00 |        0 |
| Hardware-1-1-4-1-2 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         79 |                  2 |                                 272.38 |                                60.00 |                              81.48 |                              873092.49 |                                      852.63 |                                  0.00 |        0 |
| Hardware-1-1-4-1-3 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         79 |                  2 |                                 296.64 |                                60.00 |                              80.03 |                              760471.69 |                                      742.65 |                                  0.00 |        0 |
| Hardware-1-1-4-1-4 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         80 |                  2 |                                 296.62 |                                60.00 |                              80.03 |                              727100.88 |                                      710.06 |                                  0.00 |        0 |
| Hardware-1-1-4-1-5 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         78 |                  2 |                                 294.82 |                                60.01 |                              80.03 |                              765363.73 |                                      747.43 |                                  0.00 |        0 |
| Hardware-1-1-4-1-6 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         76 |                  2 |                                 299.66 |                                60.00 |                              80.03 |                              838578.28 |                                      818.92 |                                  0.00 |        0 |
| Hardware-1-1-4-1-7 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         78 |                  2 |                                 285.68 |                                60.00 |                              80.03 |                              747198.39 |                                      729.69 |                                  0.00 |        0 |
| Hardware-1-1-4-1-8 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         76 |                  2 |                                 284.80 |                                60.01 |                              80.03 |                              754763.63 |                                      737.07 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                  2 |                                2327.85 |                                60.00 |                               1.25 |                             4519198.20 |                                     4413.28 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         69 |                  4 |                                2378.87 |                                60.00 |                               1.30 |                             5070846.15 |                                     4952.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         75 |                  8 |                                2423.59 |                                60.07 |                               7.98 |                             4541137.56 |                                     4434.71 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         80 |                 16 |                                2329.29 |                                60.01 |                              81.48 |                             6318889.03 |                                     6170.79 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        79.99 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |       111.03 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       131.88 |      2.00 |           0.22 |                  0.22 |
| Hardware-1-1-4-1 |        99.31 |      2.00 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         1.17 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         2.42 |      0.06 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         5.17 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
