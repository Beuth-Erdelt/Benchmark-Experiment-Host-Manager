## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 747s 
* Code: 1783816119
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 8, 16, 32, 64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062834
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062834
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062835
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062835
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062836
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783816119-654989dc44-2wsdf: 0

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

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         60 |                  1 | tcp                         |                             8735.47 |                              0.11 |                              0.08 |                              0.27 |                              0.38 |                                0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                  8 | tcp                         |                            65369.99 |                              0.13 |                              0.10 |                              0.33 |                              0.46 |                                0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         62 |                 16 | tcp                         |                           117147.15 |                              0.16 |                              0.11 |                              0.37 |                              0.50 |                                0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         65 |                 32 | tcp                         |                           181885.25 |                              0.23 |                              0.17 |                              0.45 |                              0.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         69 |                 64 | tcp                         |                           251881.02 |                              0.36 |                              0.35 |                              0.76 |                              2.04 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         60 |                  1 | tcp                         |                             8735.47 |                              0.11 |                              0.08 |                              0.26 |                              0.38 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                  8 | tcp                         |                            65369.99 |                              0.13 |                              0.10 |                              0.33 |                              0.46 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         62 |                 16 | tcp                         |                           117147.15 |                              0.16 |                              0.11 |                              0.37 |                              0.50 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         65 |                 32 | tcp                         |                           181885.25 |                              0.23 |                              0.17 |                              0.45 |                              0.64 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         69 |                 64 | tcp                         |                           251881.02 |                              0.36 |                              0.35 |                              0.76 |                              2.04 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         5.39 |      0.15 |           0.20 |                  0.20 |
| Hardware-1-1-2-1 |        70.63 |      1.29 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       140.24 |      2.46 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |       235.34 |      4.18 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       315.17 |      5.41 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        13.05 |      0.29 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |        92.18 |      2.93 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |       266.56 |      8.53 |           0.01 |                  0.01 |
| Hardware-1-1-4-1 |       513.82 |     17.45 |           0.01 |                  0.01 |
| Hardware-1-1-5-1 |      1014.53 |     35.66 |           0.02 |                  0.02 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
