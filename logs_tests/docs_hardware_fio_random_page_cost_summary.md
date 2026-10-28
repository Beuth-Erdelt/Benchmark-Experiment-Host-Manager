## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 266s 
* Code: 1793240941
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['read', 'randread'].
  * Block size(s) swept: ['8k'].
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
  * disk:363109
  * volume_size:48.9G
  * volume_used:24.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793240941
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363110
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793240941

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793240941-7fbbbc4f6d-2j4gf: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         67 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  8659.23 |                      0.00 |                           9.90 |                            0.00 |                          11.08 |                            0.00 |                  1 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         67 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 76455.18 |                      0.00 |                           1.25 |                            0.00 |                           2.09 |                            0.00 |                  1 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         67 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                  8659.23 |                      0.00 |                           9.90 |                            0.00 |                          11.08 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           1 |         67 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 76455.18 |                      0.00 |                           1.25 |                            0.00 |                           2.09 |                            0.00 |                  1 |        0 | fio             |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        74.99 |      1.72 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |        54.90 |      1.39 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         0.84 |      0.02 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
