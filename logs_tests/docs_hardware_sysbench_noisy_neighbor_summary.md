## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 162s 
* Code: 1794941785
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.18.
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
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058107
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941785
* hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058108
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941785
* hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058107
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941785
* hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.11.18
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:1058107
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794941785

### SUT Container Restarts
* bexhoma-sut-hardware-1-1794941785-774fb56df6-lxp96: 0
* bexhoma-sut-hardware-2-1794941785-7748b55bdb-qwx66: 0
* bexhoma-sut-hardware-3-1794941785-655b658568-vnzjb: 0
* bexhoma-sut-hardware-4-1794941785-7c6d578bb-xwk8g: 0

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
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |         2 |                                2335.44 |                                60.00 |                               1.25 |                             6573933.09 |                                     6419.86 |                                  0.00 |        0 |
| hardware-2-1-1-1-1 | hardware-2-1-1 | hardware-2-1-1-1 |                1 |        1 |               1 |       1 |         67 |         2 |                                2337.79 |                                60.00 |                               1.25 |                             4294760.69 |                                     4194.10 |                                  0.00 |        0 |
| hardware-3-1-1-1-1 | hardware-3-1-1 | hardware-3-1-1-1 |                1 |        1 |               1 |       1 |         66 |         2 |                                2342.31 |                                60.00 |                               1.25 |                             4435080.29 |                                     4331.13 |                                  0.00 |        0 |
| hardware-4-1-1-1-1 | hardware-4-1-1 | hardware-4-1-1-1 |                1 |        1 |               1 |       1 |         72 |         2 |                                2345.63 |                                60.00 |                               1.10 |                             1849724.60 |                                     1806.37 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration |   threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|----------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1-0 | hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |         65 |         2 |                                2335.44 |                                60.00 |                               1.25 |                             6573933.09 |                                     6419.86 |                                  0.00 |        0 | sysbench        |
| hardware-2-1-1-1 | hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |         67 |         2 |                                2337.79 |                                60.00 |                               1.25 |                             4294760.69 |                                     4194.10 |                                  0.00 |        0 | sysbench        |
| hardware-3-1-1-2 | hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |         66 |         2 |                                2342.31 |                                60.00 |                               1.25 |                             4435080.29 |                                     4331.13 |                                  0.00 |        0 | sysbench        |
| hardware-4-1-1-3 | hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |         72 |         2 |                                2345.63 |                                60.00 |                               1.10 |                             1849724.60 |                                     1806.37 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        50.26 |      1.73 |           0.21 |                  0.21 |
| hardware-2-1-1-1 |       119.11 |      2.00 |           0.21 |                  0.21 |
| hardware-3-1-1-1 |        48.37 |      2.00 |           0.21 |                  0.21 |
| hardware-4-1-1-1 |        71.61 |      2.00 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         3.20 |      0.00 |           0.01 |                  0.01 |
| hardware-2-1-1-1 |         3.39 |      0.00 |           0.01 |                  0.01 |
| hardware-3-1-1-1 |         3.37 |      0.00 |           0.01 |                  0.01 |
| hardware-4-1-1-1 |         3.80 |      0.00 |           0.01 |                  0.01 |

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
* TEST passed: Loading measured in this experiment
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
