## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 861s 
* Code: 1783171774
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['1M', '4M', '16M'].
  * Queue depth(s) swept: [4, 16].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:812496
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:809437
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811103
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:813340
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:804670
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805103
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783171774

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783171774-8565b6d56b-snrzb: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     78.22 |                           0.00 |                          101.19 |                           0.00 |                          166.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    250.15 |                           0.00 |                          139.46 |                           0.00 |                          217.06 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     51.99 |                           0.00 |                          128.45 |                           0.00 |                          208.67 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         63 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    153.99 |                           0.00 |                          221.25 |                           0.00 |                          438.30 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         62 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                      3.34 |                           0.00 |                         1199.57 |                           0.00 |                         1551.89 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1 | Hardware-1-1-6 | Hardware-1-1-6-1 |                1 |        6 |               1 |       1 |         63 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                      3.08 |                           0.00 |                         5737.81 |                           0.00 |                         6006.24 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     78.22 |                           0.00 |                          101.19 |                           0.00 |                          166.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    250.15 |                           0.00 |                          139.46 |                           0.00 |                          217.06 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     51.99 |                           0.00 |                          128.45 |                           0.00 |                          208.67 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         63 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    153.99 |                           0.00 |                          221.25 |                           0.00 |                          438.30 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         62 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      3.34 |                           0.00 |                         1199.57 |                           0.00 |                         1551.89 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 |         63 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      3.08 |                           0.00 |                         5737.81 |                           0.00 |                         6006.24 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        62.07 |      1.80 |           0.03 |                  0.03 |
| Hardware-1-1-2-1 |        67.44 |      3.67 |           0.04 |                  0.04 |
| Hardware-1-1-3-1 |        60.81 |      1.90 |           0.04 |                  0.04 |
| Hardware-1-1-4-1 |        69.60 |      1.90 |           0.08 |                  0.08 |
| Hardware-1-1-5-1 |        67.19 |      2.02 |           0.08 |                  0.08 |
| Hardware-1-1-6-1 |        75.37 |      2.12 |           0.27 |                  0.27 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.52 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.49 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.53 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1 |         0.53 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
