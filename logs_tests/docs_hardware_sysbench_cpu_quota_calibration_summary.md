## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 676s 
* Code: 1783170443
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 2, 4, 8] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805118
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783170443
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806241
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783170443
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:808269
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783170443
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
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
    * code:1783170443

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783170443-78f5f8777f-6hmwz: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                1216.18 |                                60.00 |                               0.84 |                             6972320.05 |                                     6808.91 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2434.15 |                                60.00 |                               0.83 |                             5823734.56 |                                     5687.24 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         72 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2421.63 |                                60.00 |                               0.89 |                              918643.81 |                                      897.11 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                2446.70 |                                60.01 |                               0.83 |                             1046718.22 |                                     1022.19 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                1216.18 |                                60.00 |                               0.84 |                             6972320.05 |                                     6808.91 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2434.15 |                                60.00 |                               0.83 |                             5823734.56 |                                     5687.24 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         72 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2421.63 |                                60.00 |                               0.89 |                              918643.81 |                                      897.11 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                2446.70 |                                60.01 |                               0.83 |                             1046718.22 |                                     1022.19 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        58.65 |      1.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |       108.94 |      2.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |       131.29 |      1.98 |           0.01 |                  0.01 |
| Hardware-1-1-4-1 |       131.90 |      2.00 |           0.01 |                  0.01 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.24 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.25 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.25 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.27 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
