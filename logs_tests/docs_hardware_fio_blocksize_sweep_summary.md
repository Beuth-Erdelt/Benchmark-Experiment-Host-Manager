## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1627s 
* Code: 1793239271
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
  * Overwrite (prefilled test file) swept: ['0'].
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type nvme and size 50Gi. Persistent storage is removed at experiment start.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 16Gi RAM.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363120
  * volume_size:48.9G
  * volume_used:24.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363115
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363116
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363116
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363117
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363117
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363120
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363112
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363112
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363113
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363114
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271
* hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363114
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793239271

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793239271-745844f775-xckgr: 0

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

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| hardware-1-1-1-1-1  | hardware-1-1-1  | hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 82913.25 |                      0.00 |                           1.16 |                            0.00 |                           1.35 |                            0.00 |                  1 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2  | hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         66 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 81128.85 |                      0.00 |                           1.17 |                            0.00 |                           1.40 |                            0.00 |                  1 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3  | hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         66 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 77184.05 |                      0.00 |                           1.27 |                            0.00 |                           1.73 |                            0.00 |                  1 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4  | hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         68 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 42716.99 |                      0.00 |                           3.78 |                            0.00 |                           4.55 |                            0.00 |                  1 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5  | hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         66 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 21472.59 |                      0.00 |                          10.81 |                            0.00 |                          12.26 |                            0.00 |                  1 |        0 |
| hardware-1-1-6-1-1  | hardware-1-1-6  | hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         67 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 10801.71 |                      0.00 |                          23.72 |                            0.00 |                          27.13 |                            0.00 |                  1 |        0 |
| hardware-1-1-7-1-1  | hardware-1-1-7  | hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         68 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  2676.83 |                      0.00 |                         112.72 |                            0.00 |                         126.35 |                            0.00 |                  1 |        0 |
| hardware-1-1-8-1-1  | hardware-1-1-8  | hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  54025.48 |                           0.00 |                            1.88 |                           0.00 |                            2.61 |                  1 |        0 |
| hardware-1-1-9-1-1  | hardware-1-1-9  | hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  54932.42 |                           0.00 |                            1.79 |                           0.00 |                            2.41 |                  1 |        0 |
| hardware-1-1-10-1-1 | hardware-1-1-10 | hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  49611.42 |                           0.00 |                            1.96 |                           0.00 |                            2.74 |                  1 |        0 |
| hardware-1-1-11-1-1 | hardware-1-1-11 | hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         63 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  31357.87 |                           0.00 |                            3.78 |                           0.00 |                            5.60 |                  1 |        0 |
| hardware-1-1-12-1-1 | hardware-1-1-12 | hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  19829.26 |                           0.00 |                            6.32 |                           0.00 |                           10.29 |                  1 |        0 |
| hardware-1-1-13-1-1 | hardware-1-1-13 | hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         64 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  10874.71 |                           0.00 |                           10.29 |                           0.00 |                           14.75 |                  1 |        0 |
| hardware-1-1-14-1-1 | hardware-1-1-14 | hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         63 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   2732.33 |                           0.00 |                           90.70 |                           0.00 |                          106.43 |                  1 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors | hardware_type   |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|:----------------|
| hardware-1-1-1  | hardware-1-1-1  |                1 |        1 |               1 |           1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 82913.25 |                      0.00 |                           1.16 |                            0.00 |                           1.35 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-2  | hardware-1-1-2  |                1 |        2 |               1 |           1 |         66 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 81128.85 |                      0.00 |                           1.17 |                            0.00 |                           1.40 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-3  | hardware-1-1-3  |                1 |        3 |               1 |           1 |         66 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 77184.05 |                      0.00 |                           1.27 |                            0.00 |                           1.73 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-4  | hardware-1-1-4  |                1 |        4 |               1 |           1 |         68 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 42716.99 |                      0.00 |                           3.78 |                            0.00 |                           4.55 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-5  | hardware-1-1-5  |                1 |        5 |               1 |           1 |         66 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 21472.59 |                      0.00 |                          10.81 |                            0.00 |                          12.26 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-6  | hardware-1-1-6  |                1 |        6 |               1 |           1 |         67 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 10801.71 |                      0.00 |                          23.72 |                            0.00 |                          27.13 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-7  | hardware-1-1-7  |                1 |        7 |               1 |           1 |         68 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                  2676.83 |                      0.00 |                         112.72 |                            0.00 |                         126.35 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-8  | hardware-1-1-8  |                1 |        8 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  54025.48 |                           0.00 |                            1.88 |                           0.00 |                            2.61 |                  1 |        0 | fio             |
| hardware-1-1-9  | hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  54932.42 |                           0.00 |                            1.79 |                           0.00 |                            2.41 |                  1 |        0 | fio             |
| hardware-1-1-10 | hardware-1-1-10 |                1 |       10 |               1 |           1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  49611.42 |                           0.00 |                            1.96 |                           0.00 |                            2.74 |                  1 |        0 | fio             |
| hardware-1-1-11 | hardware-1-1-11 |                1 |       11 |               1 |           1 |         63 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  31357.87 |                           0.00 |                            3.78 |                           0.00 |                            5.60 |                  1 |        0 | fio             |
| hardware-1-1-12 | hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  19829.26 |                           0.00 |                            6.32 |                           0.00 |                           10.29 |                  1 |        0 | fio             |
| hardware-1-1-13 | hardware-1-1-13 |                1 |       13 |               1 |           1 |         64 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  10874.71 |                           0.00 |                           10.29 |                           0.00 |                           14.75 |                  1 |        0 | fio             |
| hardware-1-1-14 | hardware-1-1-14 |                1 |       14 |               1 |           1 |         63 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   2732.33 |                           0.00 |                           90.70 |                           0.00 |                          106.43 |                  1 |        0 | fio             |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |        79.51 |      1.93 |           0.21 |                  0.21 |
| hardware-1-1-2-1  |        79.53 |      2.71 |           0.30 |                  2.85 |
| hardware-1-1-3-1  |        82.18 |      2.72 |           0.21 |                  0.21 |
| hardware-1-1-4-1  |        63.92 |      1.71 |           0.22 |                  0.22 |
| hardware-1-1-5-1  |        80.16 |      2.98 |           0.22 |                  0.22 |
| hardware-1-1-6-1  |        74.21 |      2.46 |           0.23 |                  0.23 |
| hardware-1-1-7-1  |        69.39 |      1.57 |           0.28 |                  0.28 |
| hardware-1-1-8-1  |        78.23 |      2.24 |           0.21 |                  0.22 |
| hardware-1-1-9-1  |        80.66 |      2.24 |           0.21 |                  0.22 |
| hardware-1-1-10-1 |        77.51 |      2.51 |           0.21 |                  0.23 |
| hardware-1-1-11-1 |        69.23 |      2.28 |           0.22 |                  0.23 |
| hardware-1-1-12-1 |        74.14 |      1.82 |           0.22 |                  0.23 |
| hardware-1-1-13-1 |        79.05 |      2.33 |           0.23 |                  0.24 |
| hardware-1-1-14-1 |        70.59 |      1.85 |           0.28 |                  0.29 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |         0.83 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-2-1  |         0.82 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-3-1  |         0.85 |      0.05 |           0.00 |                  0.00 |
| hardware-1-1-4-1  |         0.86 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-5-1  |         0.84 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-6-1  |         0.86 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-7-1  |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-8-1  |         0.78 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-9-1  |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-10-1 |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-11-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-12-1 |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-13-1 |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-14-1 |         0.82 |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-11-1 (bexhoma-metrics-hardware-1-1-11-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-6-1 (bexhoma-metrics-hardware-1-1-6-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-7-1 (bexhoma-metrics-hardware-1-1-7-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-9-1 (bexhoma-metrics-hardware-1-1-9-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
