## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 842s 
* Code: 1783123024
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [1].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [1].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1, 2, 4, 8, 16, 32] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:832168
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:839464
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829742
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831469
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817742
  * volume_size:50.0G
  * volume_used:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:814779
  * volume_size:50.0G
  * volume_used:48.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783123024

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783123024-6487c7645b-tjk74: 0

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
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                    120.28 |                           0.00 |                           38.54 |                           0.00 |                           81.26 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      2 |                     0.00 |                    153.31 |                           0.00 |                           54.79 |                           0.00 |                          139.46 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      4 |                     0.00 |                    408.90 |                           0.00 |                           48.50 |                           0.00 |                          106.43 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      8 |                     0.00 |                    752.88 |                           0.00 |                           50.07 |                           0.00 |                          107.48 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     16 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |
| Hardware-1-1-6-1-1 | Hardware-1-1-6 | Hardware-1-1-6-1 |                1 |        6 |               1 |       1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     32 |                     0.00 |                   2308.15 |                           0.00 |                           66.85 |                           0.00 |                          127.40 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    120.28 |                           0.00 |                           38.54 |                           0.00 |                           81.26 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    153.31 |                           0.00 |                           54.79 |                           0.00 |                          139.46 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    408.90 |                           0.00 |                           48.50 |                           0.00 |                          106.43 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    752.88 |                           0.00 |                           50.07 |                           0.00 |                          107.48 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                   2308.15 |                           0.00 |                           66.85 |                           0.00 |                          127.40 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        55.46 |      2.01 |           0.02 |                  0.02 |
| Hardware-1-1-2-1 |        65.05 |      2.08 |           0.02 |                  0.02 |
| Hardware-1-1-3-1 |        66.51 |      2.04 |           0.02 |                  0.02 |
| Hardware-1-1-4-1 |        74.18 |      1.76 |           0.02 |                  0.02 |
| Hardware-1-1-5-1 |        73.94 |      2.02 |           0.03 |                  0.03 |
| Hardware-1-1-6-1 |        76.56 |      1.81 |           0.04 |                  0.04 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.52 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.52 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.49 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-6-1 |         0.52 |      0.03 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
