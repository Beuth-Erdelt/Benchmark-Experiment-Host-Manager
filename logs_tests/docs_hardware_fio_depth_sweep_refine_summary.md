## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1389s 
* Code: 1783118630
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [64, 80, 96, 112, 128].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:690186
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678197
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:689576
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:693661
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:693990
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:684116
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:682714
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678193
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678195
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678196
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783118630

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783118630-64695bc6cb-fzm9k: 0 0

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
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5098.45 |                      0.00 |                          33.42 |                            0.00 |                         143.65 |                            0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                      1 |                  8719.86 |                      0.00 |                          27.39 |                            0.00 |                         132.64 |                            0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                      1 |                  9583.97 |                      0.00 |                          39.06 |                            0.00 |                         173.02 |                            0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                      1 |                 11924.60 |                      0.00 |                          28.97 |                            0.00 |                         149.95 |                            0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  6462.60 |                      0.00 |                          52.69 |                            0.00 |                         522.19 |                            0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1729.36 |                           0.00 |                          141.56 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randwrite         | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2011.50 |                           0.00 |                          149.95 |                           0.00 |                          379.58 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randwrite         | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2260.57 |                           0.00 |                          166.72 |                           0.00 |                          497.03 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2607.39 |                           0.00 |                          170.92 |                           0.00 |                          574.62 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2481.92 |                           0.00 |                          185.60 |                           0.00 |                          708.84 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5098.45 |                      0.00 |                          33.42 |                            0.00 |                         143.65 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                  8719.86 |                      0.00 |                          27.39 |                            0.00 |                         132.64 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                  9583.97 |                      0.00 |                          39.06 |                            0.00 |                         173.02 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                 11924.60 |                      0.00 |                          28.97 |                            0.00 |                         149.95 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  6462.60 |                      0.00 |                          52.69 |                            0.00 |                         522.19 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1729.36 |                           0.00 |                          141.56 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randwrite         | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2011.50 |                           0.00 |                          149.95 |                           0.00 |                          379.58 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2260.57 |                           0.00 |                          166.72 |                           0.00 |                          497.03 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2607.39 |                           0.00 |                          170.92 |                           0.00 |                          574.62 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2481.92 |                           0.00 |                          185.60 |                           0.00 |                          708.84 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        19.46 |      0.46 |           0.01 |                  0.01 |
| Hardware-1-1-2-1  |        25.76 |      0.73 |           0.01 |                  0.01 |
| Hardware-1-1-3-1  |        21.41 |      0.38 |           0.01 |                  0.01 |
| Hardware-1-1-4-1  |        30.99 |      0.63 |           0.01 |                  0.01 |
| Hardware-1-1-5-1  |        29.19 |      0.76 |           0.01 |                  0.01 |
| Hardware-1-1-6-1  |        11.84 |      0.26 |           0.01 |                  0.01 |
| Hardware-1-1-7-1  |        23.45 |      0.81 |           0.01 |                  0.01 |
| Hardware-1-1-8-1  |        20.07 |      0.60 |           0.01 |                  0.01 |
| Hardware-1-1-9-1  |        24.55 |      0.62 |           0.01 |                  0.01 |
| Hardware-1-1-10-1 |        23.22 |      1.16 |           0.01 |                  0.01 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
