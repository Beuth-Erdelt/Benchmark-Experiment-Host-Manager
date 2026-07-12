## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 394s 
* Code: 1783815447
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
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
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
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062823
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062831
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062831
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783815447-64bcdf966b-f2j9m: 0
* bexhoma-sut-hardware-2-1783815447-78cd9757db-vfrvz: 0
* bexhoma-sut-hardware-3-1783815447-84fb77cb4b-z8kzj: 0
* bexhoma-sut-hardware-4-1783815447-64dbfd4554-hx2m7: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-2 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-3 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-4 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-2 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-3 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-4 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         69 |                  2 |                                2391.19 |                                60.00 |                               0.89 |                             1769850.89 |                                     1728.37 |                                  0.00 |        0 |
| Hardware-2-1-1-1-1 | Hardware-2-1-1 | Hardware-2-1-1-1 |                1 |        1 |               1 |       1 |        180 |                  2 |                                2401.49 |                                60.00 |                               0.86 |                             3856651.33 |                                     3766.26 |                                  0.00 |        0 |
| Hardware-3-1-1-1-1 | Hardware-3-1-1 | Hardware-3-1-1-1 |                1 |        1 |               1 |       1 |        153 |                  2 |                                2386.91 |                                60.00 |                               0.89 |                             3507132.96 |                                     3424.93 |                                  0.00 |        0 |
| Hardware-4-1-1-1-1 | Hardware-4-1-1 | Hardware-4-1-1-1 |                1 |        1 |               1 |       1 |        128 |                  2 |                                2393.81 |                                60.00 |                               0.89 |                             2671808.15 |                                     2609.19 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-0 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |         69 |                  2 |                                2391.19 |                                60.00 |                               0.89 |                             1769850.89 |                                     1728.37 |                                  0.00 |        0 |
| Hardware-2-1-1-1 | Hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |        180 |                  2 |                                2401.49 |                                60.00 |                               0.86 |                             3856651.33 |                                     3766.26 |                                  0.00 |        0 |
| Hardware-3-1-1-2 | Hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |        153 |                  2 |                                2386.91 |                                60.00 |                               0.89 |                             3507132.96 |                                     3424.93 |                                  0.00 |        0 |
| Hardware-4-1-1-3 | Hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |        128 |                  2 |                                2393.81 |                                60.00 |                               0.89 |                             2671808.15 |                                     2609.19 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       126.04 |      2.00 |           0.21 |                  0.21 |
| Hardware-2-1-1-1 |       123.29 |      2.00 |           0.21 |                  0.21 |
| Hardware-3-1-1-1 |        66.61 |      2.00 |           0.21 |                  0.21 |
| Hardware-4-1-1-1 |        65.04 |      1.93 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         4.00 |      0.15 |           0.01 |                  0.01 |
| Hardware-2-1-1-1 |         7.54 |      0.18 |           0.01 |                  0.01 |
| Hardware-3-1-1-1 |         1.82 |      0.17 |           0.01 |                  0.01 |
| Hardware-4-1-1-1 |         1.42 |      0.18 |           0.01 |                  0.01 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
