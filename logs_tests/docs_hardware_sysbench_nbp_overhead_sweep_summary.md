## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 454s 
* Code: 1783171145
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783171145
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783171145
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805122
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783171145

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783171145-657f44847-8qzvl: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2441.75 |                                60.03 |                               0.83 |                             1229643.34 |                                     1200.82 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1223.59 |                                60.00 |                               0.83 |                             1586657.52 |                                     1549.47 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1232.63 |                                60.00 |                               0.83 |                             2205455.94 |                                     2153.77 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 614.07 |                                60.00 |                               0.83 |                             3849159.37 |                                     3758.94 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 616.75 |                                60.03 |                               0.83 |                             3981050.52 |                                     3887.74 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 608.15 |                                60.00 |                               0.83 |                             4019074.34 |                                     3924.88 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 614.35 |                                60.00 |                               0.83 |                             3869462.44 |                                     3778.77 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2441.75 |                                60.03 |                               0.83 |                             1229643.34 |                                     1200.82 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2456.22 |                                60.00 |                               0.83 |                             3792113.46 |                                     3703.24 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2453.32 |                                60.03 |                               0.83 |                            15718746.67 |                                    15350.33 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        93.31 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-2-1 |       126.84 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-3-1 |        82.60 |      2.00 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.24 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.53 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         1.07 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
