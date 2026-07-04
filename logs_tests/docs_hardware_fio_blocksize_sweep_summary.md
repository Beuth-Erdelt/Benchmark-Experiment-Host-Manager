## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1915s 
* Code: 1783116687
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k', '8k', '16k', '64k', '128k', '256k', '1M'].
  * Queue depth(s) swept: [64].
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
  * disk:823225
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806079
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806079
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806079
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806079
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:815794
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:814135
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820221
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823757
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822747
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822879
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:815726
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824532
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:806078
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783116687

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783116687-6c968f8dd4-gf9j2: 0

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

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3351.79 |                      0.00 |                          43.78 |                            0.00 |                         152.04 |                            0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3020.85 |                      0.00 |                          45.88 |                            0.00 |                         181.40 |                            0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3394.22 |                      0.00 |                          57.41 |                            0.00 |                         240.12 |                            0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  7386.03 |                      0.00 |                          33.82 |                            0.00 |                         120.06 |                            0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  8507.16 |                      0.00 |                          30.80 |                            0.00 |                         107.48 |                            0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4715.52 |                      0.00 |                          61.60 |                            0.00 |                         223.35 |                            0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2304.79 |                      0.00 |                         117.96 |                            0.00 |                         518.00 |                            0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2080.16 |                           0.00 |                          141.56 |                           0.00 |                          287.31 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2536.05 |                           0.00 |                          101.19 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2361.70 |                           0.00 |                          106.43 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1827.37 |                           0.00 |                          104.33 |                           0.00 |                          219.15 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1657.47 |                           0.00 |                          107.48 |                           0.00 |                          252.71 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1435.64 |                           0.00 |                          124.26 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    865.35 |                           0.00 |                          198.18 |                           0.00 |                          320.86 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3351.79 |                      0.00 |                          43.78 |                            0.00 |                         152.04 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3020.85 |                      0.00 |                          45.88 |                            0.00 |                         181.40 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  3394.22 |                      0.00 |                          57.41 |                            0.00 |                         240.12 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  7386.03 |                      0.00 |                          33.82 |                            0.00 |                         120.06 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  8507.16 |                      0.00 |                          30.80 |                            0.00 |                         107.48 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  4715.52 |                      0.00 |                          61.60 |                            0.00 |                         223.35 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                  2304.79 |                      0.00 |                         117.96 |                            0.00 |                         518.00 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2080.16 |                           0.00 |                          141.56 |                           0.00 |                          287.31 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2536.05 |                           0.00 |                          101.19 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2361.70 |                           0.00 |                          106.43 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1827.37 |                           0.00 |                          104.33 |                           0.00 |                          219.15 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1657.47 |                           0.00 |                          107.48 |                           0.00 |                          252.71 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1435.64 |                           0.00 |                          124.26 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    865.35 |                           0.00 |                          198.18 |                           0.00 |                          320.86 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        57.38 |      2.30 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        65.35 |      3.28 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        71.42 |      2.29 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        57.70 |      1.63 |           0.03 |                  0.03 |
| Hardware-1-1-5-1  |        70.98 |      2.23 |           0.03 |                  0.03 |
| Hardware-1-1-6-1  |        67.17 |      1.74 |           0.04 |                  0.04 |
| Hardware-1-1-7-1  |        66.86 |      2.22 |           0.09 |                  0.09 |
| Hardware-1-1-8-1  |        66.69 |      1.96 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        70.02 |      1.55 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        79.40 |      2.04 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        71.30 |      1.61 |           0.03 |                  0.03 |
| Hardware-1-1-12-1 |        77.81 |      2.10 |           0.03 |                  0.03 |
| Hardware-1-1-13-1 |        65.62 |      3.31 |           0.04 |                  0.04 |
| Hardware-1-1-14-1 |        76.96 |      2.39 |           0.09 |                  0.09 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.50 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.46 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.45 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.57 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.59 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.57 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.46 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.47 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.50 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
