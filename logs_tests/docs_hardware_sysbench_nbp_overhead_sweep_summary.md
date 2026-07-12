## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 524s 
* Code: 1783814154
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062816
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062816
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062817
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783814154-85d67d784b-wt68q: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         71 |                  4 |                                2367.08 |                                60.00 |                               1.23 |                             1113629.23 |                                     1087.53 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                  2 |                                1205.10 |                                60.00 |                               1.30 |                             3694051.70 |                                     3607.47 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                  2 |                                1197.35 |                                60.02 |                               1.30 |                             3227562.46 |                                     3151.92 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  1 |                                 592.62 |                                60.00 |                               1.12 |                             2863953.79 |                                     2796.83 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                  1 |                                 604.10 |                                60.00 |                               1.10 |                             2955954.36 |                                     2886.67 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                  1 |                                 590.65 |                                60.00 |                               1.27 |                             3203088.44 |                                     3128.02 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  1 |                                 587.68 |                                60.00 |                               1.27 |                             2854271.38 |                                     2787.37 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         71 |                  4 |                                2367.08 |                                60.00 |                               1.23 |                             1113629.23 |                                     1087.53 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         65 |                  4 |                                2402.45 |                                60.02 |                               1.30 |                             6921614.16 |                                     6759.39 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  4 |                                2375.05 |                                60.00 |                               1.27 |                            11877267.97 |                                    11598.89 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        91.84 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        64.13 |      1.97 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        52.28 |      2.00 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.63 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         1.18 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         2.41 |      0.11 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
