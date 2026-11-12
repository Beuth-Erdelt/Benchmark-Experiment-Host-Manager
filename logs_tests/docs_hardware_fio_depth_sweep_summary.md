## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1707s 
* Code: 1794474107
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
  * Overwrite (prefilled test file) swept: ['0'].
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
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
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902245
  * volume_size:48.9G
  * volume_used:24.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902249
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902250
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902250
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902251
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902251
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902251
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902252
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902245
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902245
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902246
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902246
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902247
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902247
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902248
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107
* hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.11.17
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:902248
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1794474107

### SUT Container Restarts
* bexhoma-sut-hardware-1-1794474107-b4dff8d5c-trjfv: 0

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

### Benchmarking

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| hardware-1-1-1-1-1  | hardware-1-1-1  | hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         67 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  1674.12 |                      0.00 |                           0.75 |                            0.00 |                           0.82 |                            0.00 |                  1 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2  | hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         66 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  3354.56 |                      0.00 |                           0.77 |                            0.00 |                           0.86 |                            0.00 |                  1 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3  | hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         67 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  6898.02 |                      0.00 |                           0.81 |                            0.00 |                           0.91 |                            0.00 |                  1 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4  | hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         67 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 14019.85 |                      0.00 |                           0.82 |                            0.00 |                           0.94 |                            0.00 |                  1 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5  | hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         67 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 31453.11 |                      0.00 |                           0.82 |                            0.00 |                           1.01 |                            0.00 |                  1 |        0 |
| hardware-1-1-6-1-1  | hardware-1-1-6  | hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         67 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 54655.36 |                      0.00 |                           0.91 |                            0.00 |                           1.12 |                            0.00 |                  1 |        0 |
| hardware-1-1-7-1-1  | hardware-1-1-7  | hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 86339.34 |                      0.00 |                           1.11 |                            0.00 |                           1.34 |                            0.00 |                  1 |        0 |
| hardware-1-1-8-1-1  | hardware-1-1-8  | hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         67 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                121579.87 |                      0.00 |                           1.63 |                            0.00 |                           2.61 |                            0.00 |                  1 |        0 |
| hardware-1-1-9-1-1  | hardware-1-1-9  | hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   1124.80 |                           0.00 |                            1.14 |                           0.00 |                            2.11 |                  1 |        0 |
| hardware-1-1-10-1-1 | hardware-1-1-10 | hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   2490.66 |                           0.00 |                            1.09 |                           0.00 |                            1.78 |                  1 |        0 |
| hardware-1-1-11-1-1 | hardware-1-1-11 | hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         64 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   5847.22 |                           0.00 |                            0.98 |                           0.00 |                            1.55 |                  1 |        0 |
| hardware-1-1-12-1-1 | hardware-1-1-12 | hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         64 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  11879.99 |                           0.00 |                            0.94 |                           0.00 |                            1.71 |                  1 |        0 |
| hardware-1-1-13-1-1 | hardware-1-1-13 | hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         63 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  21687.46 |                           0.00 |                            1.03 |                           0.00 |                            1.58 |                  1 |        0 |
| hardware-1-1-14-1-1 | hardware-1-1-14 | hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         64 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  35709.47 |                           0.00 |                            1.32 |                           0.00 |                            1.88 |                  1 |        0 |
| hardware-1-1-15-1-1 | hardware-1-1-15 | hardware-1-1-15-1 |                1 |       15 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  54223.28 |                           0.00 |                            1.91 |                           0.00 |                            2.77 |                  1 |        0 |
| hardware-1-1-16-1-1 | hardware-1-1-16 | hardware-1-1-16-1 |                1 |       16 |               1 |       1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  67055.06 |                           0.00 |                            3.52 |                           0.00 |                            5.34 |                  1 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors | hardware_type   |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|:----------------|
| hardware-1-1-1  | hardware-1-1-1  |                1 |        1 |               1 |           1 |         67 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                  1674.12 |                      0.00 |                           0.75 |                            0.00 |                           0.82 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-2  | hardware-1-1-2  |                1 |        2 |               1 |           1 |         66 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                  3354.56 |                      0.00 |                           0.77 |                            0.00 |                           0.86 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-3  | hardware-1-1-3  |                1 |        3 |               1 |           1 |         67 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                  6898.02 |                      0.00 |                           0.81 |                            0.00 |                           0.91 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-4  | hardware-1-1-4  |                1 |        4 |               1 |           1 |         67 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                 14019.85 |                      0.00 |                           0.82 |                            0.00 |                           0.94 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-5  | hardware-1-1-5  |                1 |        5 |               1 |           1 |         67 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                 31453.11 |                      0.00 |                           0.82 |                            0.00 |                           1.01 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-6  | hardware-1-1-6  |                1 |        6 |               1 |           1 |         67 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                 54655.36 |                      0.00 |                           0.91 |                            0.00 |                           1.12 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-7  | hardware-1-1-7  |                1 |        7 |               1 |           1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 86339.34 |                      0.00 |                           1.11 |                            0.00 |                           1.34 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-8  | hardware-1-1-8  |                1 |        8 |               1 |           1 |         67 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                121579.87 |                      0.00 |                           1.63 |                            0.00 |                           2.61 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-9  | hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   1124.80 |                           0.00 |                            1.14 |                           0.00 |                            2.11 |                  1 |        0 | fio             |
| hardware-1-1-10 | hardware-1-1-10 |                1 |       10 |               1 |           1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   2490.66 |                           0.00 |                            1.09 |                           0.00 |                            1.78 |                  1 |        0 | fio             |
| hardware-1-1-11 | hardware-1-1-11 |                1 |       11 |               1 |           1 |         64 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   5847.22 |                           0.00 |                            0.98 |                           0.00 |                            1.55 |                  1 |        0 | fio             |
| hardware-1-1-12 | hardware-1-1-12 |                1 |       12 |               1 |           1 |         64 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  11879.99 |                           0.00 |                            0.94 |                           0.00 |                            1.71 |                  1 |        0 | fio             |
| hardware-1-1-13 | hardware-1-1-13 |                1 |       13 |               1 |           1 |         63 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  21687.46 |                           0.00 |                            1.03 |                           0.00 |                            1.58 |                  1 |        0 | fio             |
| hardware-1-1-14 | hardware-1-1-14 |                1 |       14 |               1 |           1 |         64 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  35709.47 |                           0.00 |                            1.32 |                           0.00 |                            1.88 |                  1 |        0 | fio             |
| hardware-1-1-15 | hardware-1-1-15 |                1 |       15 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  54223.28 |                           0.00 |                            1.91 |                           0.00 |                            2.77 |                  1 |        0 | fio             |
| hardware-1-1-16 | hardware-1-1-16 |                1 |       16 |               1 |           1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  67055.06 |                           0.00 |                            3.52 |                           0.00 |                            5.34 |                  1 |        0 | fio             |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |        70.13 |      2.23 |           0.23 |                  0.23 |
| hardware-1-1-2-1  |        73.53 |      2.15 |           0.35 |                  4.35 |
| hardware-1-1-3-1  |        72.64 |      1.82 |           0.23 |                  0.23 |
| hardware-1-1-4-1  |        79.27 |      2.85 |           0.23 |                  0.23 |
| hardware-1-1-5-1  |        71.85 |      2.29 |           0.23 |                  0.23 |
| hardware-1-1-6-1  |        79.67 |      1.84 |           0.23 |                  0.23 |
| hardware-1-1-7-1  |        81.42 |      2.95 |           0.23 |                  0.23 |
| hardware-1-1-8-1  |        82.47 |      4.98 |           0.28 |                  1.99 |
| hardware-1-1-9-1  |        66.48 |      2.10 |           0.23 |                  0.23 |
| hardware-1-1-10-1 |        67.75 |      2.16 |           0.23 |                  0.23 |
| hardware-1-1-11-1 |        68.48 |      2.26 |           0.23 |                  0.24 |
| hardware-1-1-12-1 |        75.86 |      2.29 |           0.23 |                  0.25 |
| hardware-1-1-13-1 |        80.20 |      2.24 |           0.23 |                  0.25 |
| hardware-1-1-14-1 |        77.15 |      2.16 |           0.23 |                  0.26 |
| hardware-1-1-15-1 |        88.58 |      2.12 |           0.24 |                  0.27 |
| hardware-1-1-16-1 |        66.49 |      1.58 |           0.23 |                  0.27 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |         0.82 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-2-1  |         0.82 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-3-1  |         0.84 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-4-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-5-1  |         0.82 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-6-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-7-1  |         0.83 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-8-1  |         0.84 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-9-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-10-1 |         0.84 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-11-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-12-1 |         0.86 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-13-1 |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-14-1 |         0.85 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-15-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-16-1 |         0.83 |      0.03 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-10-1 (bexhoma-metrics-hardware-1-1-10-1-benchmarker.log, expected: series exists only while non-zero)
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
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
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
* CPU Throttling Rate [s/s] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-15-1 (bexhoma-metrics-hardware-1-1-15-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-16-1 (bexhoma-metrics-hardware-1-1-16-1-benchmarking.log, expected: series exists only while non-zero)
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
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-8-1 (bexhoma-metrics-hardware-1-1-8-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: Data parameters as requested
* TEST passed: Loading completed without failures
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
