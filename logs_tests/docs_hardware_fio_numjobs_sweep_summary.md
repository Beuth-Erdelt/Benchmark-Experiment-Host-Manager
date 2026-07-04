## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1388s 
* Code: 1783115274
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1, 2, 4, 8, 16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:689973
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677111
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:682997
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:679360
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:677114
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783115274

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783115274-759d949c84-98tbb: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3926.64 |                      0.00 |                          29.49 |                            0.00 |                         101.19 |                            0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                  6279.35 |                      0.00 |                          57.41 |                            0.00 |                         354.42 |                            0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                  3984.66 |                      0.00 |                         108.53 |                            0.00 |                        2164.26 |                            0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                  4114.35 |                      0.00 |                         371.20 |                            0.00 |                        3472.88 |                            0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                  3826.61 |                      0.00 |                         734.00 |                            0.00 |                        5268.05 |                            0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1604.06 |                           0.00 |                          149.95 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                     0.00 |                   2170.72 |                           0.00 |                          206.57 |                           0.00 |                          901.78 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                     0.00 |                   1988.53 |                           0.00 |                          240.12 |                           0.00 |                         3036.68 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                     0.00 |                   2858.75 |                           0.00 |                          591.40 |                           0.00 |                         3707.76 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3926.64 |                      0.00 |                          29.49 |                            0.00 |                         101.19 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  6279.35 |                      0.00 |                          57.41 |                            0.00 |                         354.42 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3984.66 |                      0.00 |                         108.53 |                            0.00 |                        2164.26 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4114.35 |                      0.00 |                         371.20 |                            0.00 |                        3472.88 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3826.61 |                      0.00 |                         734.00 |                            0.00 |                        5268.05 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1604.06 |                           0.00 |                          149.95 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2170.72 |                           0.00 |                          206.57 |                           0.00 |                          901.78 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1988.53 |                           0.00 |                          240.12 |                           0.00 |                         3036.68 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2858.75 |                           0.00 |                          591.40 |                           0.00 |                         3707.76 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        16.92 |      0.52 |           0.01 |                  0.01 |
| Hardware-1-1-2-1  |        34.84 |      0.77 |           0.01 |                  0.01 |
| Hardware-1-1-3-1  |        27.09 |      0.66 |           0.01 |                  0.01 |
| Hardware-1-1-4-1  |        30.96 |      1.40 |           0.01 |                  0.01 |
| Hardware-1-1-5-1  |        27.22 |      0.47 |           0.02 |                  0.02 |
| Hardware-1-1-6-1  |        19.49 |      1.06 |           0.01 |                  0.01 |
| Hardware-1-1-7-1  |        19.02 |      0.35 |           0.01 |                  0.01 |
| Hardware-1-1-8-1  |        22.80 |      0.55 |           0.01 |                  0.01 |
| Hardware-1-1-9-1  |        30.96 |      0.66 |           0.01 |                  0.01 |
| Hardware-1-1-10-1 |        30.84 |      0.69 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.50 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.54 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.44 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.45 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.53 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
