## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 709s 
* Code: 1783787574
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
  * disk:1062552
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783787574
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062562
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783787574
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062569
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783787574
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062575
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783787574

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783787574-6b6b9879d6-gxtwf: 0

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
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                  2 |                                2295.14 |                                60.00 |                               1.27 |                             6462537.67 |                                     6311.07 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         69 |                  2 |                                 927.17 |                                60.00 |                               1.73 |                             1634261.79 |                                     1595.96 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         69 |                  2 |                                 919.71 |                                60.00 |                               1.58 |                             1527470.30 |                                     1491.67 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         73 |                  2 |                                 453.17 |                                60.00 |                              26.20 |                             1172392.97 |                                     1144.92 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         71 |                  2 |                                 458.42 |                                60.04 |                              26.20 |                             1322546.05 |                                     1291.55 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         72 |                  2 |                                 460.63 |                                60.00 |                              26.20 |                             1172366.98 |                                     1144.89 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         73 |                  2 |                                 453.64 |                                60.00 |                              26.20 |                              984569.59 |                                      961.49 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         86 |                  2 |                                 232.82 |                                60.00 |                              64.47 |                              559209.07 |                                      546.10 |                                  0.00 |        0 |
| Hardware-1-1-4-1-2 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         86 |                  2 |                                 228.02 |                                60.02 |                              64.47 |                              530002.05 |                                      517.58 |                                  0.00 |        0 |
| Hardware-1-1-4-1-3 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         83 |                  2 |                                 234.08 |                                60.02 |                              64.47 |                              596716.58 |                                      582.73 |                                  0.00 |        0 |
| Hardware-1-1-4-1-4 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         84 |                  2 |                                 221.57 |                                60.03 |                              64.47 |                              566711.38 |                                      553.43 |                                  0.00 |        0 |
| Hardware-1-1-4-1-5 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         82 |                  2 |                                 223.82 |                                60.06 |                              64.47 |                              598934.85 |                                      584.90 |                                  0.00 |        0 |
| Hardware-1-1-4-1-6 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         83 |                  2 |                                 224.39 |                                60.00 |                              64.47 |                              578922.70 |                                      565.35 |                                  0.00 |        0 |
| Hardware-1-1-4-1-7 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         82 |                  2 |                                 228.91 |                                60.02 |                              64.47 |                              554127.68 |                                      541.14 |                                  0.00 |        0 |
| Hardware-1-1-4-1-8 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         80 |                  2 |                                 231.41 |                                60.00 |                              64.47 |                              601754.31 |                                      587.65 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                  2 |                                2295.14 |                                60.00 |                               1.27 |                             6462537.67 |                                     6311.07 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         69 |                  4 |                                1846.88 |                                60.00 |                               1.73 |                             3161732.09 |                                     3087.63 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         73 |                  8 |                                1825.86 |                                60.04 |                              26.20 |                             4651875.59 |                                     4542.85 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         86 |                 16 |                                1825.02 |                                60.06 |                              64.47 |                             4586378.62 |                                     4478.88 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       121.43 |      1.98 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |       112.60 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       108.79 |      2.00 |           0.22 |                  0.22 |
| Hardware-1-1-4-1 |       138.35 |      2.00 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         1.12 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         2.35 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         5.34 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
