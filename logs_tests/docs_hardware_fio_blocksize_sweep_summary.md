## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2048s 
* Code: 1783163363
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
  * disk:840609
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840127
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:837843
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:841996
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:839548
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:845793
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840610
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:840008
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:841756
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:838663
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:839711
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:835488
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:836614
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:836027
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783163363

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783163363-7dfdcfbf5b-lgl7t: 0

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
bexhoma : C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\hardware.py:193: FutureWarning: 
Downcasting behavior in `replace` is deprecated and will be removed in a future version. To retain the old behavior, explicitly 
call `result.infer_objects(copy=False)`. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
In Zeile:1 Zeichen:1
+ bexhoma hardware `
+ ~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (C:\Users\Patric...asting', True)`:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  df[numeric_columns] = df[numeric_columns].replace('', 0).infer_objects(copy=False)
* DBMS Hardware-1 - Experiment 1 Client 13: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 14: hardware (1 pods)

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         73 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2857.47 |                      0.00 |                          46.40 |                            0.00 |                         233.83 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         72 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3177.27 |                      0.00 |                          54.26 |                            0.00 |                         254.80 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         70 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3284.07 |                      0.00 |                          62.65 |                            0.00 |                         299.89 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         72 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2287.97 |                      0.00 |                          45.35 |                            0.00 |                         434.11 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         70 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5591.46 |                      0.00 |                          23.99 |                            0.00 |                         112.72 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         71 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4061.62 |                      0.00 |                          41.16 |                            0.00 |                         217.06 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         73 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                   680.97 |                      0.00 |                         123.21 |                            0.00 |                        3204.45 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    730.28 |                           0.00 |                          263.19 |                           0.00 |                         1266.68 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         64 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1072.28 |                           0.00 |                          183.50 |                           0.00 |                          708.84 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         83 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    138.22 |                           0.00 |                          526.39 |                           0.00 |                        17112.76 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    546.36 |                           0.00 |                          333.45 |                           0.00 |                         1132.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         67 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    931.52 |                           0.00 |                          156.24 |                           0.00 |                          658.51 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    985.44 |                           0.00 |                          162.53 |                           0.00 |                          459.28 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
C:\Users\Patrick\eclipse-workspace\Benchmark-Experiment-Host-Manager\bexhoma\evaluators\hardware.py:193: FutureWarning: Downcasting 
behavior in `replace` is deprecated and will be removed in a future version. To retain the old behavior, explicitly call 
`result.infer_objects(copy=False)`. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  df[numeric_columns] = df[numeric_columns].replace('', 0).infer_objects(copy=False)
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         64 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    587.87 |                           0.00 |                          295.70 |                           0.00 |                         1266.68 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         73 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  2857.47 |                      0.00 |                          46.40 |                            0.00 |                         233.83 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         72 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3177.27 |                      0.00 |                          54.26 |                            0.00 |                         254.80 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         70 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  3284.07 |                      0.00 |                          62.65 |                            0.00 |                         299.89 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         72 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  2287.97 |                      0.00 |                          45.35 |                            0.00 |                         434.11 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         70 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  5591.46 |                      0.00 |                          23.99 |                            0.00 |                         112.72 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         71 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  4061.62 |                      0.00 |                          41.16 |                            0.00 |                         217.06 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         73 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                   680.97 |                      0.00 |                         123.21 |                            0.00 |                        3204.45 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    730.28 |                           0.00 |                          263.19 |                           0.00 |                         1266.68 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         64 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1072.28 |                           0.00 |                          183.50 |                           0.00 |                          708.84 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         83 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    138.22 |                           0.00 |                          526.39 |                           0.00 |                        17112.76 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    546.36 |                           0.00 |                          333.45 |                           0.00 |                         1132.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         67 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    931.52 |                           0.00 |                          156.24 |                           0.00 |                          658.51 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    985.44 |                           0.00 |                          162.53 |                           0.00 |                          459.28 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         64 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    587.87 |                           0.00 |                          295.70 |                           0.00 |                         1266.68 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        65.44 |      1.73 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        71.34 |      2.08 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        64.07 |      1.53 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        61.86 |      3.12 |           0.03 |                  0.03 |
| Hardware-1-1-5-1  |        70.68 |      2.17 |           0.03 |                  0.03 |
| Hardware-1-1-6-1  |        64.87 |      2.07 |           0.04 |                  0.04 |
| Hardware-1-1-7-1  |        67.52 |      1.89 |           0.08 |                  0.08 |
| Hardware-1-1-8-1  |        60.84 |      3.02 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        70.70 |      2.42 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        64.70 |      2.06 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        72.15 |      1.52 |           0.03 |                  0.03 |
| Hardware-1-1-12-1 |        61.32 |      1.82 |           0.03 |                  0.03 |
| Hardware-1-1-13-1 |        61.64 |      1.40 |           0.04 |                  0.04 |
| Hardware-1-1-14-1 |        62.24 |      1.99 |           0.08 |                  0.08 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.43 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.52 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.52 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.60 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.50 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.60 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.45 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.56 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
