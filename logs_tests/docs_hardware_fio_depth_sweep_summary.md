## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2378s 
* Code: 1783808209
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [1, 2, 4, 8, 16, 32, 64, 128].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 50Gi. Persistent storage is removed at experiment start.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062890
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1064044
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1067056
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1080987
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1089789
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1096308
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1105708
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1112106
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1078458
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1083824
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1089477
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1094088
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1102727
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1107609
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1110018
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1087873
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783808209

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783808209-68d6cdb8d9-svkpk: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         74 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                    34.98 |                      0.00 |                          29.23 |                            0.00 |                         164.63 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         71 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                   175.70 |                      0.00 |                          26.08 |                            0.00 |                          73.92 |                            0.00 |                  1 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         72 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                   543.32 |                      0.00 |                          19.01 |                            0.00 |                          49.55 |                            0.00 |                  1 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         74 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                   223.79 |                      0.00 |                          26.08 |                            0.00 |                         583.01 |                            0.00 |                  1 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         72 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2285.93 |                      0.00 |                          18.22 |                            0.00 |                          51.12 |                            0.00 |                  1 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         71 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2910.83 |                      0.00 |                          25.30 |                            0.00 |                          92.80 |                            0.00 |                  1 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         70 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4836.11 |                      0.00 |                          49.02 |                            0.00 |                         166.72 |                            0.00 |                  1 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         70 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4806.34 |                      0.00 |                          53.22 |                            0.00 |                         851.44 |                            0.00 |                  1 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    110.26 |                           0.00 |                           34.34 |                           0.00 |                           67.63 |                  1 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    184.74 |                           0.00 |                           39.58 |                           0.00 |                           79.17 |                  1 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         66 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    311.82 |                           0.00 |                           42.21 |                           0.00 |                          114.82 |                  1 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         64 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    540.62 |                           0.00 |                           54.26 |                           0.00 |                          120.06 |                  1 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         64 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    887.06 |                           0.00 |                           68.68 |                           0.00 |                          162.53 |                  1 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         64 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1370.07 |                           0.00 |                           91.75 |                           0.00 |                          189.79 |                  1 |        0 |
| Hardware-1-1-15-1-1 | Hardware-1-1-15 | Hardware-1-1-15-1 |                1 |       15 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2202.25 |                           0.00 |                          123.21 |                           0.00 |                          229.64 |                  1 |        0 |
| Hardware-1-1-16-1-1 | Hardware-1-1-16 | Hardware-1-1-16-1 |                1 |       16 |               1 |       1 |         65 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   3389.16 |                           0.00 |                          156.24 |                           0.00 |                          248.51 |                  1 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         74 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    34.98 |                      0.00 |                          29.23 |                            0.00 |                         164.63 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         71 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   175.70 |                      0.00 |                          26.08 |                            0.00 |                          73.92 |                            0.00 |                  1 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         72 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   543.32 |                      0.00 |                          19.01 |                            0.00 |                          49.55 |                            0.00 |                  1 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         74 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                   223.79 |                      0.00 |                          26.08 |                            0.00 |                         583.01 |                            0.00 |                  1 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         72 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  2285.93 |                      0.00 |                          18.22 |                            0.00 |                          51.12 |                            0.00 |                  1 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         71 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  2910.83 |                      0.00 |                          25.30 |                            0.00 |                          92.80 |                            0.00 |                  1 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         70 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4836.11 |                      0.00 |                          49.02 |                            0.00 |                         166.72 |                            0.00 |                  1 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         70 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  4806.34 |                      0.00 |                          53.22 |                            0.00 |                         851.44 |                            0.00 |                  1 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    110.26 |                           0.00 |                           34.34 |                           0.00 |                           67.63 |                  1 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    184.74 |                           0.00 |                           39.58 |                           0.00 |                           79.17 |                  1 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         66 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    311.82 |                           0.00 |                           42.21 |                           0.00 |                          114.82 |                  1 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         64 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    540.62 |                           0.00 |                           54.26 |                           0.00 |                          120.06 |                  1 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         64 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    887.06 |                           0.00 |                           68.68 |                           0.00 |                          162.53 |                  1 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         64 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1370.07 |                           0.00 |                           91.75 |                           0.00 |                          189.79 |                  1 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2202.25 |                           0.00 |                          123.21 |                           0.00 |                          229.64 |                  1 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 |         65 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3389.16 |                           0.00 |                          156.24 |                           0.00 |                          248.51 |                  1 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        76.61 |      1.68 |           0.23 |                  0.23 |
| Hardware-1-1-2-1  |        55.91 |      1.77 |           0.23 |                  0.23 |
| Hardware-1-1-3-1  |        49.77 |      1.30 |           0.24 |                  4.12 |
| Hardware-1-1-4-1  |        56.39 |      1.75 |           0.23 |                  0.23 |
| Hardware-1-1-5-1  |        57.03 |      1.69 |           0.23 |                  0.23 |
| Hardware-1-1-6-1  |        64.30 |      1.85 |           0.23 |                  0.23 |
| Hardware-1-1-7-1  |        58.75 |      1.73 |           0.23 |                  0.23 |
| Hardware-1-1-8-1  |        59.79 |      1.93 |           0.23 |                  0.23 |
| Hardware-1-1-9-1  |        61.60 |      3.07 |           0.23 |                  0.23 |
| Hardware-1-1-10-1 |        69.99 |      2.30 |           0.23 |                  0.23 |
| Hardware-1-1-11-1 |        55.14 |      1.99 |           0.23 |                  0.23 |
| Hardware-1-1-12-1 |        56.14 |      1.86 |           0.23 |                  0.23 |
| Hardware-1-1-13-1 |        62.29 |      1.61 |           0.23 |                  0.23 |
| Hardware-1-1-14-1 |        53.77 |      1.35 |           0.23 |                  0.23 |
| Hardware-1-1-15-1 |        59.86 |      1.85 |           0.23 |                  0.23 |
| Hardware-1-1-16-1 |        56.96 |      2.37 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.74 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.85 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         1.17 |      0.07 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.98 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         1.17 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         1.04 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         1.11 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.74 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         1.11 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.93 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         1.12 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         1.19 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         1.14 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         1.07 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-15-1 |         1.04 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-16-1 |         1.12 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
