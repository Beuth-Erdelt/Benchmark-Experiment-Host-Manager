## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 238s 
* Code: 1783815862
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
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062832
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783815862

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783815862-65cbdfb4fb-ldwn6: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         61 |                  1 | tcp                         |                             8758.24 |                              0.11 |                              0.09 |                              0.26 |                              0.38 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         61 |                  1 | tcp                         |                             8758.24 |                              0.11 |                              0.08 |                              0.26 |                              0.38 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         7.71 |      0.17 |           0.20 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        11.43 |      0.31 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
