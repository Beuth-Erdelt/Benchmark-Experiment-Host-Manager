## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 316s 
* Code: 1783172304
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:804616
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783172304
* Hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:804882
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783172304
* Hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806223
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783172304
* Hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806934
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783172304

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783172304-66bf9895-n7ntf: 0
* bexhoma-sut-hardware-2-1783172304-7597944db7-qdgwx: 0
* bexhoma-sut-hardware-3-1783172304-588d74db47-2ptfq: 0
* bexhoma-sut-hardware-4-1783172304-5f79499b7f-vrvvg: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |        140 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2447.43 |                                60.00 |                               0.83 |                             2914074.81 |                                     2845.78 |                                  0.00 |        0 |
| Hardware-2-1-1-1-1 | Hardware-2-1-1 | Hardware-2-1-1-1 |                1 |        1 |               1 |       1 |        118 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2445.07 |                                60.00 |                               0.83 |                             1730371.91 |                                     1689.82 |                                  0.00 |        0 |
| Hardware-3-1-1-1-1 | Hardware-3-1-1 | Hardware-3-1-1-1 |                1 |        1 |               1 |       1 |         88 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2445.52 |                                60.00 |                               0.83 |                             6204183.50 |                                     6058.77 |                                  0.00 |        0 |
| Hardware-4-1-1-1-1 | Hardware-4-1-1 | Hardware-4-1-1-1 |                1 |        1 |               1 |       1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2446.26 |                                60.00 |                               0.83 |                             2941059.14 |                                     2872.13 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-0 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |        140 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2447.43 |                                60.00 |                               0.83 |                             2914074.81 |                                     2845.78 |                                  0.00 |        0 |
| Hardware-2-1-1-1 | Hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |        118 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2445.07 |                                60.00 |                               0.83 |                             1730371.91 |                                     1689.82 |                                  0.00 |        0 |
| Hardware-3-1-1-2 | Hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |         88 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2445.52 |                                60.00 |                               0.83 |                             6204183.50 |                                     6058.77 |                                  0.00 |        0 |
| Hardware-4-1-1-3 | Hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2446.26 |                                60.00 |                               0.83 |                             2941059.14 |                                     2872.13 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       122.16 |      2.00 |           0.01 |                  0.01 |
| Hardware-2-1-1-1 |        71.80 |      2.00 |           0.01 |                  0.01 |
| Hardware-3-1-1-1 |        90.52 |      1.84 |           0.00 |                  0.00 |
| Hardware-4-1-1-1 |        72.28 |      2.00 |           0.01 |                  0.01 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.23 |      0.01 |           0.00 |                  0.00 |
| Hardware-2-1-1-1 |         0.41 |      0.01 |           0.00 |                  0.00 |
| Hardware-3-1-1-1 |         0.30 |      0.01 |           0.00 |                  0.00 |
| Hardware-4-1-1-1 |         0.25 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
