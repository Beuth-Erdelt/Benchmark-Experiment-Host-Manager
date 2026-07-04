## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2200s 
* Code: 1783120041
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [1, 2, 4, 8, 16, 32, 64, 128].
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
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831543
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:833940
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:835198
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831613
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:837717
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829800
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825681
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831750
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825177
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:827871
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831905
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821517
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826881
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829500
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830982
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829377
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783120041

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783120041-5bdbc98444-69sjg: 0

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
* DBMS Hardware-1 - Experiment 1 Client 11: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 12: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 13: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 14: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 15: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 16: hardware (1 pods)

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
* DBMS Hardware-1 - Experiment 1 Client 11: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 12: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 13: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 14: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 15: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 16: hardware (1 pods)

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                    61.41 |                      0.00 |                          35.91 |                            0.00 |                          94.90 |                            0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                   149.89 |                      0.00 |                          33.42 |                            0.00 |                          96.99 |                            0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                   374.10 |                      0.00 |                          28.97 |                            0.00 |                          85.46 |                            0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                   858.62 |                      0.00 |                          26.35 |                            0.00 |                          82.31 |                            0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                  1990.59 |                      0.00 |                          21.36 |                            0.00 |                          74.97 |                            0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randread          | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3202.98 |                      0.00 |                          31.85 |                            0.00 |                          99.09 |                            0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5124.44 |                      0.00 |                          47.45 |                            0.00 |                         170.92 |                            0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randread          | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  6655.83 |                      0.00 |                          63.18 |                            0.00 |                         463.47 |                            0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     91.12 |                           0.00 |                           40.11 |                           0.00 |                           93.85 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    164.24 |                           0.00 |                           45.35 |                           0.00 |                          102.24 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 | randwrite         | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    287.73 |                           0.00 |                           48.50 |                           0.00 |                          114.82 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 | randwrite         | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    515.01 |                           0.00 |                           54.26 |                           0.00 |                          120.06 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 | randwrite         | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    907.01 |                           0.00 |                           61.08 |                           0.00 |                          160.43 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 | randwrite         | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1419.89 |                           0.00 |                           80.22 |                           0.00 |                          214.96 |        0 |
| Hardware-1-1-15-1-1 | Hardware-1-1-15 | Hardware-1-1-15-1 |                1 |       15 |               1 |       1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2013.53 |                           0.00 |                          109.58 |                           0.00 |                          400.56 |        0 |
| Hardware-1-1-16-1-1 | Hardware-1-1-16 | Hardware-1-1-16-1 |                1 |       16 |               1 |       1 | randwrite         | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2267.28 |                           0.00 |                          135.27 |                           0.00 |                          851.44 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    61.41 |                      0.00 |                          35.91 |                            0.00 |                          94.90 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   149.89 |                      0.00 |                          33.42 |                            0.00 |                          96.99 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   374.10 |                      0.00 |                          28.97 |                            0.00 |                          85.46 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                   858.62 |                      0.00 |                          26.35 |                            0.00 |                          82.31 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  1990.59 |                      0.00 |                          21.36 |                            0.00 |                          74.97 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  3202.98 |                      0.00 |                          31.85 |                            0.00 |                          99.09 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5124.44 |                      0.00 |                          47.45 |                            0.00 |                         170.92 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randread          | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  6655.83 |                      0.00 |                          63.18 |                            0.00 |                         463.47 |                            0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     91.12 |                           0.00 |                           40.11 |                           0.00 |                           93.85 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    164.24 |                           0.00 |                           45.35 |                           0.00 |                          102.24 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    287.73 |                           0.00 |                           48.50 |                           0.00 |                          114.82 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    515.01 |                           0.00 |                           54.26 |                           0.00 |                          120.06 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    907.01 |                           0.00 |                           61.08 |                           0.00 |                          160.43 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1419.89 |                           0.00 |                           80.22 |                           0.00 |                          214.96 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2013.53 |                           0.00 |                          109.58 |                           0.00 |                          400.56 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 | randwrite         | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2267.28 |                           0.00 |                          135.27 |                           0.00 |                          851.44 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        66.93 |      2.18 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        64.94 |      2.07 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        60.99 |      1.91 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        68.91 |      2.65 |           0.02 |                  0.02 |
| Hardware-1-1-5-1  |        68.26 |      2.11 |           0.02 |                  0.02 |
| Hardware-1-1-6-1  |        74.69 |      1.77 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        70.78 |      2.27 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        69.30 |      1.79 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        68.83 |      3.05 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        62.91 |      2.07 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        68.81 |      2.52 |           0.02 |                  0.02 |
| Hardware-1-1-12-1 |        63.01 |      1.50 |           0.02 |                  0.02 |
| Hardware-1-1-13-1 |        63.59 |      2.22 |           0.03 |                  0.03 |
| Hardware-1-1-14-1 |        66.27 |      1.91 |           0.02 |                  0.02 |
| Hardware-1-1-15-1 |        71.84 |      2.40 |           0.02 |                  0.02 |
| Hardware-1-1-16-1 |        62.76 |      1.62 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.48 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.43 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.54 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.56 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.45 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.55 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-15-1 |         0.59 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-16-1 |         0.55 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
