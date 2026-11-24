## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 161s 
* Code: 1795436108
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.12.3.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.12.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:813944
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1795436108
* hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.12.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:813944
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1795436108
* hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.12.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:813944
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1795436108
* hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.12.3
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:813944
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1795436108

### Loading Skipped
* loading skipped by -sl, DBMS not managed by bexhoma, nothing loaded or measured: Hardware-1, Hardware-2, Hardware-3, Hardware-4

### SUT Container Restarts
* bexhoma-sut-hardware-1-1795436108-557475ddd7-nw4q8: 0
* bexhoma-sut-hardware-2-1795436108-f9c6dbb7-9rgsr: 0
* bexhoma-sut-hardware-3-1795436108-bdf4b7d7f-wtrhl: 0
* bexhoma-sut-hardware-4-1795436108-7755c47bf5-6nkxk: 0

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

### Benchmarking

#### Per Connection

| connection         | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |         2 |                                2283.30 |                                60.00 |                               1.25 |                             5430513.99 |                                     5303.24 |                                  0.00 |        0 |
| hardware-2-1-1-1-1 | hardware-2-1-1 | hardware-2-1-1-1 |                1 |        1 |               1 |       1 |         67 |         2 |                                2288.58 |                                60.00 |                               1.10 |                             6239803.24 |                                     6093.56 |                                  0.00 |        0 |
| hardware-3-1-1-1-1 | hardware-3-1-1 | hardware-3-1-1-1 |                1 |        1 |               1 |       1 |         66 |         2 |                                2250.21 |                                60.00 |                               1.30 |                             5962597.01 |                                     5822.85 |                                  0.00 |        0 |
| hardware-4-1-1-1-1 | hardware-4-1-1 | hardware-4-1-1-1 |                1 |        1 |               1 |       1 |         68 |         2 |                                2284.83 |                                60.00 |                               1.10 |                             4107345.33 |                                     4011.08 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1-0 | hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |         65 |         2 |                                2283.30 |                                60.00 |                               1.25 |                             5430513.99 |                                     5303.24 |                                  0.00 |        0 | sysbench        |
| hardware-2-1-1-1 | hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |         67 |         2 |                                2288.58 |                                60.00 |                               1.10 |                             6239803.24 |                                     6093.56 |                                  0.00 |        0 | sysbench        |
| hardware-3-1-1-2 | hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |         66 |         2 |                                2250.21 |                                60.00 |                               1.30 |                             5962597.01 |                                     5822.85 |                                  0.00 |        0 | sysbench        |
| hardware-4-1-1-3 | hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |         68 |         2 |                                2284.83 |                                60.00 |                               1.10 |                             4107345.33 |                                     4011.08 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       102.49 |      2.00 |           0.21 |                  0.21 |
| hardware-2-1-1-1 |        89.81 |      2.00 |           0.21 |                  0.21 |
| hardware-3-1-1-1 |       102.42 |      2.00 |           0.21 |                  0.21 |
| hardware-4-1-1-1 |        97.10 |      2.00 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         3.33 |      0.00 |           0.01 |                  0.01 |
| hardware-2-1-1-1 |         3.71 |      0.00 |           0.01 |                  0.01 |
| hardware-3-1-1-1 |         3.52 |      0.00 |           0.01 |                  0.01 |
| hardware-4-1-1-1 |         3.72 |      0.00 |           0.01 |                  0.01 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-2-1-1-1 (bexhoma-metrics-hardware-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-2-1-1-1 (bexhoma-metrics-hardware-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-3-1-1-1 (bexhoma-metrics-hardware-3-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-3-1-1-1 (bexhoma-metrics-hardware-3-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-4-1-1-1 (bexhoma-metrics-hardware-4-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-4-1-1-1 (bexhoma-metrics-hardware-4-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST skipped: Loading measured in this experiment (loading skipped by -sl, DBMS not managed by bexhoma: Hardware-1, Hardware-2, Hardware-3, Hardware-4)
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
