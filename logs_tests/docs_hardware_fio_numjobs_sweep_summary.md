## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1698s 
* Code: 1783161637
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [64].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 80Gi. Persistent storage is removed at experiment start.
  * Benchmarking is tested with [1, 2, 4, 8, 16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:839207
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:842199
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840328
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:836171
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840991
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:839254
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:838123
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840521
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:837586
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:838925
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783161637

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783161637-7b45c4c4cb-w7fxr: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 7: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 8: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 9: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 10: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 7: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 8: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 9: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 10: hardware (1 pods)

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2924.99 |                      0.00 |                          72.88 |                            0.00 |                         267.39 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                  4335.98 |                      0.00 |                          74.97 |                            0.00 |                         608.17 |                            0.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                  4110.61 |                      0.00 |                          94.90 |                            0.00 |                        2231.37 |                            0.00 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                  4074.11 |                      0.00 |                         196.08 |                            0.00 |                        4798.28 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                  3891.85 |                      0.00 |                        1216.35 |                            0.00 |                        7012.88 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1218.91 |                           0.00 |                          181.40 |                           0.00 |                          463.47 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                     0.00 |                   2653.30 |                           0.00 |                          183.50 |                           0.00 |                          367.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                     0.00 |                   3844.71 |                           0.00 |                          221.25 |                           0.00 |                          767.56 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                     0.00 |                   3365.52 |                           0.00 |                          329.25 |                           0.00 |                         3741.32 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\hardware.py:183: FutureWarning: Downcasting 
behavior in `replace` is deprecated and will be removed in a future version. To retain the old behavior, explicitly call 
`result.infer_objects(copy=False)`. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  for key in _KEYS_RESULTS:
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                     0.00 |                   3642.50 |                           0.00 |                          918.55 |                           0.00 |                         7147.09 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  2924.99 |                      0.00 |                          72.88 |                            0.00 |                         267.39 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4335.98 |                      0.00 |                          74.97 |                            0.00 |                         608.17 |                            0.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4110.61 |                      0.00 |                          94.90 |                            0.00 |                        2231.37 |                            0.00 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4074.11 |                      0.00 |                         196.08 |                            0.00 |                        4798.28 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3891.85 |                      0.00 |                        1216.35 |                            0.00 |                        7012.88 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1218.91 |                           0.00 |                          181.40 |                           0.00 |                          463.47 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2653.30 |                           0.00 |                          183.50 |                           0.00 |                          367.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3844.71 |                           0.00 |                          221.25 |                           0.00 |                          767.56 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3365.52 |                           0.00 |                          329.25 |                           0.00 |                         3741.32 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3642.50 |                           0.00 |                          918.55 |                           0.00 |                         7147.09 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        77.99 |      2.08 |           0.02 |                  4.02 |
| Hardware-1-1-2-1  |        75.09 |      4.12 |           0.03 |                  3.39 |
| Hardware-1-1-3-1  |        75.55 |      1.59 |           0.03 |                  4.03 |
| Hardware-1-1-4-1  |        88.91 |      1.75 |           0.03 |                  4.03 |
| Hardware-1-1-5-1  |       113.52 |      2.50 |           0.03 |                  4.03 |
| Hardware-1-1-6-1  |        57.56 |      1.51 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        69.32 |      2.18 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        75.81 |      2.87 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        69.41 |      1.94 |           0.03 |                  0.03 |
| Hardware-1-1-10-1 |        68.37 |      1.76 |           0.03 |                  0.03 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.43 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.43 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.56 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.03 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.56 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.55 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.54 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.55 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.55 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.54 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
