## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2187s 
* Code: 1783113058
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
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
  * disk:802447
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797376
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797377
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797377
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797377
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797377
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:797378
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:796407
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:809021
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816811
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:815808
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:810194
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:812127
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805115
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:805195
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:800977
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783113058

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783113058-c6d64548d-g28tz: 0

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
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                    77.07 |                      0.00 |                          27.13 |                            0.00 |                          61.08 |                            0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                   186.07 |                      0.00 |                          28.97 |                            0.00 |                          72.88 |                            0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                   441.31 |                      0.00 |                          25.03 |                            0.00 |                          69.73 |                            0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                  1091.08 |                      0.00 |                          21.36 |                            0.00 |                          64.23 |                            0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                  1828.46 |                      0.00 |                          17.96 |                            0.00 |                          68.68 |                            0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2835.13 |                      0.00 |                          17.69 |                            0.00 |                          70.78 |                            0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  6460.70 |                      0.00 |                          32.90 |                            0.00 |                         116.92 |                            0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  9383.59 |                      0.00 |                          31.85 |                            0.00 |                         383.78 |                            0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     94.16 |                           0.00 |                           32.90 |                           0.00 |                           80.22 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    174.48 |                           0.00 |                           36.44 |                           0.00 |                           82.31 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    284.95 |                           0.00 |                           42.21 |                           0.00 |                           93.85 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    480.65 |                           0.00 |                           49.55 |                           0.00 |                          132.64 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    912.67 |                           0.00 |                           62.13 |                           0.00 |                          181.40 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1088.46 |                           0.00 |                           74.97 |                           0.00 |                          217.06 |        0 |
| Hardware-1-1-15-1-1 | Hardware-1-1-15 | Hardware-1-1-15-1 |                1 |       15 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2009.98 |                           0.00 |                          109.58 |                           0.00 |                          246.42 |        0 |
| Hardware-1-1-16-1-1 | Hardware-1-1-16 | Hardware-1-1-16-1 |                1 |       16 |               1 |       1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   3300.47 |                           0.00 |                          158.33 |                           0.00 |                          304.09 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    77.07 |                      0.00 |                          27.13 |                            0.00 |                          61.08 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   186.07 |                      0.00 |                          28.97 |                            0.00 |                          72.88 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   441.31 |                      0.00 |                          25.03 |                            0.00 |                          69.73 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                  1091.08 |                      0.00 |                          21.36 |                            0.00 |                          64.23 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  1828.46 |                      0.00 |                          17.96 |                            0.00 |                          68.68 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  2835.13 |                      0.00 |                          17.69 |                            0.00 |                          70.78 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  6460.70 |                      0.00 |                          32.90 |                            0.00 |                         116.92 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  9383.59 |                      0.00 |                          31.85 |                            0.00 |                         383.78 |                            0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     94.16 |                           0.00 |                           32.90 |                           0.00 |                           80.22 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    174.48 |                           0.00 |                           36.44 |                           0.00 |                           82.31 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    284.95 |                           0.00 |                           42.21 |                           0.00 |                           93.85 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    480.65 |                           0.00 |                           49.55 |                           0.00 |                          132.64 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    912.67 |                           0.00 |                           62.13 |                           0.00 |                          181.40 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1088.46 |                           0.00 |                           74.97 |                           0.00 |                          217.06 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2009.98 |                           0.00 |                          109.58 |                           0.00 |                          246.42 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3300.47 |                           0.00 |                          158.33 |                           0.00 |                          304.09 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        72.25 |      2.30 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        64.37 |      2.18 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        61.87 |      2.10 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        66.73 |      2.15 |           0.02 |                  0.02 |
| Hardware-1-1-5-1  |        65.78 |      1.83 |           0.03 |                  0.03 |
| Hardware-1-1-6-1  |        68.90 |      2.94 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        71.12 |      2.02 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        68.25 |      3.43 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        63.88 |      1.88 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        64.08 |      3.26 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        61.51 |      2.36 |           0.02 |                  0.02 |
| Hardware-1-1-12-1 |        75.44 |      2.39 |           0.02 |                  0.02 |
| Hardware-1-1-13-1 |        67.70 |      2.13 |           0.03 |                  0.03 |
| Hardware-1-1-14-1 |        69.07 |      2.22 |           0.02 |                  0.02 |
| Hardware-1-1-15-1 |        72.10 |      2.41 |           0.02 |                  0.02 |
| Hardware-1-1-16-1 |        75.38 |      1.80 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.44 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.44 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.47 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.46 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.48 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-15-1 |         0.47 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-16-1 |         0.46 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
