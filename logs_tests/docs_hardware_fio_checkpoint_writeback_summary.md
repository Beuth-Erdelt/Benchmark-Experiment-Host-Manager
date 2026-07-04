## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 844s 
* Code: 1783124623
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['1M', '4M', '16M'].
  * Queue depth(s) swept: [4, 16].
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
  * disk:690104
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:688933
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:682958
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:679329
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678204
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * host:6.8.0-111-generic
  * node:cl-worker37
  * disk:678203
  * volume_size:50.0G
  * volume_used:48.6G
  * cpu_list:0-127
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783124623

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783124623-578c7d4496-8vbjn: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 6: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     49.09 |                           0.00 |                          238.03 |                           0.00 |                          484.44 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    123.78 |                           0.00 |                          379.58 |                           0.00 |                         1115.68 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     28.86 |                           0.00 |                          350.22 |                           0.00 |                         1061.16 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     91.54 |                           0.00 |                          371.20 |                           0.00 |                         2164.26 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     13.66 |                           0.00 |                          826.28 |                           0.00 |                         2499.81 |        0 |
| Hardware-1-1-6-1-1 | Hardware-1-1-6 | Hardware-1-1-6-1 |                1 |        6 |               1 |       1 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     20.85 |                           0.00 |                         1686.11 |                           0.00 |                        14831.06 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     49.09 |                           0.00 |                          238.03 |                           0.00 |                          484.44 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    123.78 |                           0.00 |                          379.58 |                           0.00 |                         1115.68 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     28.86 |                           0.00 |                          350.22 |                           0.00 |                         1061.16 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     91.54 |                           0.00 |                          371.20 |                           0.00 |                         2164.26 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     13.66 |                           0.00 |                          826.28 |                           0.00 |                         2499.81 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     20.85 |                           0.00 |                         1686.11 |                           0.00 |                        14831.06 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        11.73 |      0.42 |           0.01 |                  0.01 |
| Hardware-1-1-2-1 |        16.57 |      0.46 |           0.02 |                  0.02 |
| Hardware-1-1-3-1 |        15.54 |      0.49 |           0.02 |                  0.02 |
| Hardware-1-1-4-1 |        13.81 |      0.45 |           0.07 |                  0.07 |
| Hardware-1-1-5-1 |        15.85 |      0.49 |           0.07 |                  0.07 |
| Hardware-1-1-6-1 |        18.53 |      0.46 |           0.26 |                  0.26 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.43 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.48 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-6-1 |         0.48 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
