## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2192s 
* Code: 1783810612
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k', '8k', '16k', '64k', '128k', '256k', '1M'].
  * Queue depth(s) swept: [64].
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
  * disk:1083063
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062796
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062797
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062806
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062806
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1063004
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1084145
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062668
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062778
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062989
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062793
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062793
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062794
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062794
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783810612

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783810612-5464b4f559-6hknc: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         77 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4659.59 |                      0.00 |                          36.44 |                            0.00 |                         114.82 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         73 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4459.42 |                      0.00 |                          43.25 |                            0.00 |                         149.95 |                            0.00 |                  1 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         70 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5402.64 |                      0.00 |                          45.88 |                            0.00 |                         143.65 |                            0.00 |                  1 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         70 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  6325.46 |                      0.00 |                          37.49 |                            0.00 |                         158.33 |                            0.00 |                  1 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         75 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  6693.54 |                      0.00 |                          35.91 |                            0.00 |                         179.31 |                            0.00 |                  1 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         71 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5271.82 |                      0.00 |                          36.44 |                            0.00 |                         217.06 |                            0.00 |                  1 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         74 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                   719.93 |                      0.00 |                         287.31 |                            0.00 |                        2634.02 |                            0.00 |                  1 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1991.36 |                           0.00 |                          130.55 |                           0.00 |                          252.71 |                  1 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         65 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2249.65 |                           0.00 |                          117.96 |                           0.00 |                          212.86 |                  1 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2279.52 |                           0.00 |                          110.62 |                           0.00 |                          202.38 |                  1 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1386.34 |                           0.00 |                          125.30 |                           0.00 |                          450.89 |                  1 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1714.02 |                           0.00 |                          108.53 |                           0.00 |                          185.60 |                  1 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1456.53 |                           0.00 |                          122.16 |                           0.00 |                          181.40 |                  1 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         64 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    827.48 |                           0.00 |                          210.76 |                           0.00 |                          400.56 |                  1 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         77 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4659.59 |                      0.00 |                          36.44 |                            0.00 |                         114.82 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         73 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4459.42 |                      0.00 |                          43.25 |                            0.00 |                         149.95 |                            0.00 |                  1 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         70 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  5402.64 |                      0.00 |                          45.88 |                            0.00 |                         143.65 |                            0.00 |                  1 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         70 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  6325.46 |                      0.00 |                          37.49 |                            0.00 |                         158.33 |                            0.00 |                  1 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         75 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  6693.54 |                      0.00 |                          35.91 |                            0.00 |                         179.31 |                            0.00 |                  1 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         71 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  5271.82 |                      0.00 |                          36.44 |                            0.00 |                         217.06 |                            0.00 |                  1 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         74 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                   719.93 |                      0.00 |                         287.31 |                            0.00 |                        2634.02 |                            0.00 |                  1 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1991.36 |                           0.00 |                          130.55 |                           0.00 |                          252.71 |                  1 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         65 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2249.65 |                           0.00 |                          117.96 |                           0.00 |                          212.86 |                  1 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2279.52 |                           0.00 |                          110.62 |                           0.00 |                          202.38 |                  1 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1386.34 |                           0.00 |                          125.30 |                           0.00 |                          450.89 |                  1 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1714.02 |                           0.00 |                          108.53 |                           0.00 |                          185.60 |                  1 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1456.53 |                           0.00 |                          122.16 |                           0.00 |                          181.40 |                  1 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         64 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    827.48 |                           0.00 |                          210.76 |                           0.00 |                          400.56 |                  1 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        71.35 |      2.52 |           0.23 |                  0.23 |
| Hardware-1-1-2-1  |        68.45 |      1.53 |           0.23 |                  0.23 |
| Hardware-1-1-3-1  |        58.73 |      2.35 |           0.23 |                  0.23 |
| Hardware-1-1-4-1  |        65.37 |      1.96 |           0.24 |                  4.24 |
| Hardware-1-1-5-1  |        61.75 |      1.66 |           0.24 |                  0.24 |
| Hardware-1-1-6-1  |        72.54 |      2.29 |           0.24 |                  4.24 |
| Hardware-1-1-7-1  |        70.75 |      2.25 |           0.29 |                  0.29 |
| Hardware-1-1-8-1  |        57.45 |      1.62 |           0.23 |                  0.23 |
| Hardware-1-1-9-1  |        64.65 |      1.69 |           0.23 |                  0.23 |
| Hardware-1-1-10-1 |        63.64 |      4.56 |           0.23 |                  0.23 |
| Hardware-1-1-11-1 |        68.79 |      1.96 |           0.23 |                  0.23 |
| Hardware-1-1-12-1 |        68.67 |      2.60 |           0.24 |                  0.24 |
| Hardware-1-1-13-1 |        60.95 |      1.67 |           0.24 |                  0.24 |
| Hardware-1-1-14-1 |        70.00 |      1.61 |           0.29 |                  0.29 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.75 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.86 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.08 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.86 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.88 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.88 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.88 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.84 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.82 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.79 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.85 |      0.07 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.83 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.86 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         1.01 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
