# Benchmark: Hardware

`Hardware` is not a DBMS benchmark — it runs [fio](https://fio.readthedocs.io/) (disk I/O),
[sysbench](https://github.com/akopytov/sysbench) (CPU/memory),
[sockperf](https://github.com/Mellanox/sockperf) (single-connection network latency/throughput), or
[netperf](https://github.com/HewlettPackard/netperf) (many-concurrent-connection request/response)
directly against a dedicated SUT container, bypassing any database engine entirely. There is no
data loading phase and no `-dbms` engine choice beyond the single `Hardware` target (see
[DBMS.md](DBMS.md#hardware)).

The purpose of these benchmarks is not to rank hardware, but to **calibrate DBMS configuration**
against the actual storage/network a cluster provides — for example finding the queue depth
[PostgreSQL](https://www.postgresql.org/)'s `effective_io_concurrency` should target, a realistic
`random_page_cost`, the raw fsync latency that bounds commit throughput under
`synchronous_commit=on`, or whether per-connection query latency holds steady as concurrent
connections grow (relevant to `max_connections`/PgBouncer pool sizing).

**The results are not official benchmark results.
Exact performance depends on a number of parameters, including the underlying storage class,
node hardware, and cluster load at the time of the run.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

Result tables below are real output from an actual cluster run of every command on this page. This
page shows the four tools bexhoma can drive through `hardware.py`, what each one is about, and a
handful of typical use cases per tool. These commands are a subset of the full sweeps in
[`scripts/test-docs-hardware.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.ps1) /
[`scripts/test-docs-hardware.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.sh);
see [TestCases.md](TestCases.md#hardware) for eight further fio sweeps (numjobs, PostgreSQL-page-size
depth sweep, `fdatasync`, WAL group-commit and record-size sweeps, checkpoint writeback bandwidth,
and the OLTP/WAL contention proxy) with real output from
[`scripts/test-docs-cases.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cases.ps1) /
[`scripts/test-docs-cases.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-cases.sh).

## Perform Benchmark

You will have to change the node selectors to names of nodes that exist in your cluster
(or leave the corresponding parameters out):
```bash
BEXHOMA_NODE_SUT="cl-worker36"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=1
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

Unlike every other entry script, `hardware.py` has no loader — there is nothing to import before
benchmarking, so every command below goes straight to `run`. Which tool runs is selected with
`-xht {fio,sysbench,sockperf,netperf}`; everything else about a command depends on that choice, as
covered tool by tool below.

---

## Fio

### What is fio

[fio](https://fio.readthedocs.io/) ("Flexible I/O Tester") is Jens Axboe's open-source disk I/O
workload generator. It synthesizes an I/O pattern — read/write mix, block size, queue depth, I/O
engine, sync behavior — against a file or block device and reports IOPS, throughput, and latency
percentiles. bexhoma drives it to characterize the storage a SUT container actually sees, so that
storage-related DBMS settings can be set from measured numbers instead of generic defaults.

References:
1. fio documentation: https://fio.readthedocs.io/en/latest/fio_doc.html
1. fio `--fsync` / `--fdatasync`: https://fio.readthedocs.io/en/latest/fio_doc.html#cmdoption-arg-fsync
1. PostgreSQL WAL configuration: https://www.postgresql.org/docs/current/wal-configuration.html
1. PostgreSQL `effective_io_concurrency`: https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY

### Using fio in bexhoma

Select it with `-xht fio`. `-xts`/`-xtd` set the test file size and the duration per round; the
workload is swept with `-xfrw` (read pattern), `-xfbs` (block size), `-xfid` (queue depth), `-xfe`
(I/O engine), `-xfsy`/`-xffd` (fsync/fdatasync interval), and `-xfmx` (read percentage for mixed
`randrw`) — each accepts a comma-separated list, and every combination across the lists runs as one
more sequential round against the same SUT, so a whole sweep is one invocation instead of one
process per value. Because fio writes real data, request and size a persistent volume with
`-rst`/`-rss`, and pass `-rsr` so each command starts from a freshly recreated, empty volume rather
than inheriting whatever an earlier command left behind. The PVC name is fixed and shared across
the whole page (not scoped by experiment code), so fio commands must never be run concurrently
against the same SUT.

### Examples

#### 1. Queue-depth sweep

For performing the experiment we can run the
[hardware file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/hardware.py).

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 1,2,4,8,16,32,64,128 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep.log
```

This
* loops over 8 queue depths (`-xfid`, doubling from 1 to 128) for both `randread` and `randwrite`
  (`-xfrw`) at a fixed 4k block size (`-xfbs`)
* runs each of the 16 combinations as one more sequential round against the same SUT (16 rounds
  × 60s ≈ 16 minutes)
* collects SUT resource metrics (`-m`)
* tests if results match workflow (`-tr`)
* shows a summary

Doubling the queue depth (rather than a linear step) is standard practice for this kind of sweep:
IOPS/latency behavior versus depth is fundamentally logarithmic, so evenly-spaced points on a log
scale reveal the curvature efficiently, and real systems mostly configure queue depth in powers
of 2 anyway (NVMe queues, io_uring, RAID controllers).

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_fio_depth_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_fio_depth_sweep.log</a></summary>

```markdown
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
```

</details>

The Per Phase table lists one row per queue depth, with IOPS and completion-latency percentiles
aggregated across all pods in that round.

---

#### 2. Block-size sweep at fixed queue depth (throughput curve)

Also fixes `-xfid 64`, but sweeps `-xfbs` instead of numjobs: finds the best block size at the
queue depth already identified as the elbow, and shows where the workload shifts from IOPS-bound
(small blocks) to bandwidth-bound (large blocks).

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k,8k,16k,64k,128k,256k,1M \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_blocksize_sweep.log
```

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_fio_blocksize_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_fio_blocksize_sweep.log</a></summary>

```markdown
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
```

</details>

The Per Phase table lists one row per block size, at the fixed queue depth set by `-xfid`.

---

#### 3. `random_page_cost` calibration

Sequential vs. random read at the same block size and depth. The latency/throughput ratio
between the two rounds gives a device-specific number to replace `random_page_cost`'s
spinning-disk-era default of 4.0 (relative to `seq_page_cost=1.0`) — often closer to 1.1-1.5 on
NVMe.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw read,randread \
  -xfbs 8k \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_random_page_cost.log
```

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_fio_random_page_cost_summary.md" target="_blank" rel="noopener">docs_hardware_fio_random_page_cost.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 385s 
* Code: 1783812824
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
  * disk:1062808
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783812824
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062809
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783812824

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783812824-5496875d9-56btw: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         71 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4892.99 |                      0.00 |                          32.11 |                            0.00 |                          96.99 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         72 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4340.16 |                      0.00 |                          50.07 |                            0.00 |                         175.11 |                            0.00 |                  1 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         71 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4892.99 |                      0.00 |                          32.11 |                            0.00 |                          96.99 |                            0.00 |                  1 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         72 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4340.16 |                      0.00 |                          50.07 |                            0.00 |                         175.11 |                            0.00 |                  1 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        70.33 |      1.67 |           0.23 |                  0.23 |
| Hardware-1-1-2-1 |        71.88 |      1.78 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.90 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.85 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

</details>

The Per Phase table has one row for `read` (sequential) and one for `randread`, both at the same
block size and queue depth.

---

#### 4. WAL sync-write latency (fsync)

Sequential 8k write + fsync after every write, depth 1, single thread — "how fast can one backend
commit with `synchronous_commit=on` and no batching" (max TPS ≈ 1/latency).
`wal_sync_method=fsync`.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 8k \
  -xfid 1 \
  -xfe libaio \
  -xfsy 1 \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fsync.log
```

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_fio_wal_sync_fsync_summary.md" target="_blank" rel="noopener">docs_hardware_fio_wal_sync_fsync.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 248s 
* Code: 1783813228
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [1].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [1].
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
  * disk:1062811
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783813228

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783813228-6f75bf6655-jv2gw: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     83.27 |                           0.00 |                           43.78 |                           0.00 |                          100.14 |                  1 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     83.27 |                           0.00 |                           43.78 |                           0.00 |                          100.14 |                  1 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        68.37 |      2.05 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.76 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

</details>

`hardware_fio_write_iops` and the write latency percentiles in the Per Phase table are the
relevant columns for this single-row result.

---

## Sysbench

### What is sysbench

[sysbench](https://github.com/akopytov/sysbench) is Alexey Kopytov's open-source multi-threaded
benchmark tool for CPU, memory, and file I/O/OLTP workloads. It is most often used as a MySQL/
PostgreSQL OLTP load generator, but its CPU and memory sub-benchmarks are also a standard generic
system stress test. bexhoma uses only those CPU/memory sub-benchmarks to check whether a
Kubernetes CPU limit on a SUT container actually **isolates** co-located workloads from each
other, independent of any database engine.

References:
1. sysbench: https://github.com/akopytov/sysbench
1. Kubernetes resource requests and limits: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### Using sysbench in bexhoma

Select it with `-xht sysbench`. `-xtd` sets the run duration; `-nbt`/`-nbp` control how many
sysbench threads run and how they are split across benchmarker pods, and `-ne` grows total demand
against the SUT instead of just re-partitioning the same thread count. Give the SUT container a
hard CPU quota with `-lc`/`-rc` (request equal to limit), and use `-mtn`/`-mtb container` to run
several independent SUT pods pinned to the same node for a noisy-neighbor comparison. Sysbench
does no disk I/O, so none of the fio-only flags (`-rst`/`-rss`/`-rsr`) apply.

### Examples

#### 1. CPU-quota calibration (thread sweep)

A single SUT pod, `-lc 2 -rc 2` (request equals limit, so the CPU quota is a hard ceiling, not a
burstable one), sweeping sysbench's own thread count (`-nbt`) at a fixed `-nbp 1`:

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 1,2,4,8 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_cpu_quota_calibration.log
```

The Per Phase table lists one row per thread count, with `hardware_sysbench_cpu_events_per_sec`
and the `-mc` CPU usage columns being the ones to compare across rows; the thread count is used as
a fixed parameter in commands 14-16.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sysbench_cpu_quota_calibration_summary.md" target="_blank" rel="noopener">docs_hardware_sysbench_cpu_quota_calibration.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 639s 
* Code: 1783813494
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [1, 2, 4, 8], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 2, 4, 8] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062812
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783813494
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062813
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783813494
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062814
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783813494
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062814
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783813494

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783813494-86f67f85d-nzmjg: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                  1 |                                1104.56 |                                60.00 |                               1.27 |                             6010368.62 |                                     5869.50 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         63 |                  2 |                                2256.32 |                                60.00 |                               1.25 |                             4996442.43 |                                     4879.34 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         65 |                  4 |                                2273.19 |                                60.01 |                               1.30 |                             2827840.15 |                                     2761.56 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         72 |                  8 |                                2391.41 |                                60.04 |                               1.27 |                              960992.27 |                                      938.47 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                  1 |                                1104.56 |                                60.00 |                               1.27 |                             6010368.62 |                                     5869.50 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         63 |                  2 |                                2256.32 |                                60.00 |                               1.25 |                             4996442.43 |                                     4879.34 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         65 |                  4 |                                2273.19 |                                60.01 |                               1.30 |                             2827840.15 |                                     2761.56 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         72 |                  8 |                                2391.41 |                                60.04 |                               1.27 |                              960992.27 |                                      938.47 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        37.88 |      1.00 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        58.17 |      1.57 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        80.89 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |       124.39 |      2.00 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.67 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.67 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.66 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

</details>


`hardware_sysbench_cpu_events_per_sec` in the Per Phase table together with the Monitoring
section's CPU columns is what to compare across the thread counts swept.

---
#### 2. Harness-overhead sweep (`-nbp`)

The same fixed total of 4 sysbench threads against the same `-lc 2` SUT, but re-partitioned
across a growing number of separate benchmarker pods/SSH sessions (`-nbp`) instead of more
`--threads` inside one pod:

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1,2,4 \
  -nbt 4 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_nbp_overhead_sweep.log
```

`hardware.py` computes `threads_per_pod = -nbt / -nbp`, so the *total* sysbench thread count stays
constant across all rounds in the Per Phase table — only the number of separate pods carrying
them (`pod_count`) changes.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sysbench_nbp_overhead_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_sysbench_nbp_overhead_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 524s 
* Code: 1783814154
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062816
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062816
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062817
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814154

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783814154-85d67d784b-wt68q: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         71 |                  4 |                                2367.08 |                                60.00 |                               1.23 |                             1113629.23 |                                     1087.53 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                  2 |                                1205.10 |                                60.00 |                               1.30 |                             3694051.70 |                                     3607.47 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                  2 |                                1197.35 |                                60.02 |                               1.30 |                             3227562.46 |                                     3151.92 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  1 |                                 592.62 |                                60.00 |                               1.12 |                             2863953.79 |                                     2796.83 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                  1 |                                 604.10 |                                60.00 |                               1.10 |                             2955954.36 |                                     2886.67 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                  1 |                                 590.65 |                                60.00 |                               1.27 |                             3203088.44 |                                     3128.02 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  1 |                                 587.68 |                                60.00 |                               1.27 |                             2854271.38 |                                     2787.37 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         71 |                  4 |                                2367.08 |                                60.00 |                               1.23 |                             1113629.23 |                                     1087.53 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         65 |                  4 |                                2402.45 |                                60.02 |                               1.30 |                             6921614.16 |                                     6759.39 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  4 |                                2375.05 |                                60.00 |                               1.27 |                            11877267.97 |                                    11598.89 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        91.84 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        64.13 |      1.97 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        52.28 |      2.00 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.63 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         1.18 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         2.41 |      0.11 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

</details>


`hardware_sysbench_cpu_events_per_sec` in the Per Phase table is what to compare across the
`-nbp` values swept; `pod_count` in the same table confirms how the fixed total thread count was
partitioned.

---
#### 3. Shared-SUT saturation sweep (`-ne`)

The same `-lc 2` SUT, but this time `-ne` actually grows total demand instead of just
re-partitioning it — each additional parallel client submits another full `-nbt`-threads pod
(`benchmarking_pods_scaled = num_executor * benchmarking_pods` in `hardware.py`):

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 2 \
  -ne 1,2,4,8 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_ne_saturation_sweep.log
```

At `-nbt 2 -nbp 1`, `-ne 1,2,4,8` pushes growing total sysbench thread counts against the same
fixed-size cgroup, all inside one shared SUT container. The Per Phase table lists one row per
`-ne` value; `hardware_sysbench_cpu_events_per_sec` and `hardware_sysbench_cpu_lat_p95_ms` are the
throughput and completion-latency columns, and this result is the baseline command 16 is compared
against.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sysbench_ne_saturation_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_sysbench_ne_saturation_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 730s 
* Code: 1783814697
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4, 8] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062818
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062819
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062820
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062820
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783814697

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783814697-69c476b458-24skd: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                  2 |                                2327.85 |                                60.00 |                               1.25 |                             4519198.20 |                                     4413.28 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  2 |                                1196.63 |                                60.00 |                               1.30 |                             3496153.84 |                                     3414.21 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         69 |                  2 |                                1182.24 |                                60.00 |                               1.30 |                             1574692.31 |                                     1537.79 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         72 |                  2 |                                 595.38 |                                60.00 |                               7.98 |                             1450708.98 |                                     1416.71 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         75 |                  2 |                                 610.61 |                                60.07 |                               7.98 |                              912273.03 |                                      890.89 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         72 |                  2 |                                 612.80 |                                60.00 |                               7.98 |                             1153357.27 |                                     1126.33 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         72 |                  2 |                                 604.80 |                                60.00 |                               7.98 |                             1024798.28 |                                     1000.78 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         78 |                  2 |                                 298.69 |                                60.01 |                              80.03 |                              852319.94 |                                      832.34 |                                  0.00 |        0 |
| Hardware-1-1-4-1-2 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         79 |                  2 |                                 272.38 |                                60.00 |                              81.48 |                              873092.49 |                                      852.63 |                                  0.00 |        0 |
| Hardware-1-1-4-1-3 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         79 |                  2 |                                 296.64 |                                60.00 |                              80.03 |                              760471.69 |                                      742.65 |                                  0.00 |        0 |
| Hardware-1-1-4-1-4 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         80 |                  2 |                                 296.62 |                                60.00 |                              80.03 |                              727100.88 |                                      710.06 |                                  0.00 |        0 |
| Hardware-1-1-4-1-5 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         78 |                  2 |                                 294.82 |                                60.01 |                              80.03 |                              765363.73 |                                      747.43 |                                  0.00 |        0 |
| Hardware-1-1-4-1-6 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         76 |                  2 |                                 299.66 |                                60.00 |                              80.03 |                              838578.28 |                                      818.92 |                                  0.00 |        0 |
| Hardware-1-1-4-1-7 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         78 |                  2 |                                 285.68 |                                60.00 |                              80.03 |                              747198.39 |                                      729.69 |                                  0.00 |        0 |
| Hardware-1-1-4-1-8 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         76 |                  2 |                                 284.80 |                                60.01 |                              80.03 |                              754763.63 |                                      737.07 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                  2 |                                2327.85 |                                60.00 |                               1.25 |                             4519198.20 |                                     4413.28 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         69 |                  4 |                                2378.87 |                                60.00 |                               1.30 |                             5070846.15 |                                     4952.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         75 |                  8 |                                2423.59 |                                60.07 |                               7.98 |                             4541137.56 |                                     4434.71 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         80 |                 16 |                                2329.29 |                                60.01 |                              81.48 |                             6318889.03 |                                     6170.79 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        79.99 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |       111.03 |      2.00 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       131.88 |      2.00 |           0.22 |                  0.22 |
| Hardware-1-1-4-1 |        99.31 |      2.00 |           0.23 |                  0.23 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         1.17 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         2.42 |      0.06 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         5.17 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

</details>


`hardware_sysbench_cpu_events_per_sec` and `hardware_sysbench_cpu_lat_p95_ms` in the Per Phase
table are the throughput and completion-latency columns to compare across the `-ne` values swept
— this is the single-tenant baseline the noisy-neighbor test below is compared against.

---
#### 4. Co-located noisy-neighbor test (`-mtn`/`-mtb container`)

The actual cross-tenant test. `-mtn 4 -mtb container` creates 4 independent `SutConfiguration`
objects — 4 separate SUT pods, 4 separate cgroups — each `-lc 2 -rc 2` like command 13, all
pinned to the same physical node via `-rnn`:

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sysbench \
  -xtd 60 \
  -nbp 1 \
  -nbt 2 \
  -ne 1 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -lc 2 \
  -rc 2 \
  -mtb container \
  -mtn 4 \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sysbench_noisy_neighbor.log
```

`BEXHOMA_TENANT_BY=container` makes every tenant's benchmarker pod wait on one shared
experiment-level Redis counter (`bexhoma-benchmarker-podcount-exp-<experiment>`, see
`images/hardware/benchmarker/benchmarker.sh`) before starting sysbench, so all four 2-thread runs
begin at the same synchronized instant instead of drifting apart with each pod's own scheduling
jitter — otherwise a pod that happens to start stressing the node a few seconds before another
would make the comparison meaningless. `get_summary_benchmark_per_phase_multitenant()` groups the
result by `(phase, tenant_id)`, giving one row per co-located SUT pod.

`hardware_sysbench_cpu_events_per_sec` per tenant can be compared against the single-pod baseline
from command 13 at the same thread count.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sysbench_noisy_neighbor_summary.md" target="_blank" rel="noopener">docs_hardware_sysbench_noisy_neighbor.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 394s 
* Code: 1783815447
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062832
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062823
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062831
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447
* Hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062831
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783815447

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783815447-64bcdf966b-f2j9m: 0
* bexhoma-sut-hardware-2-1783815447-78cd9757db-vfrvz: 0
* bexhoma-sut-hardware-3-1783815447-84fb77cb4b-z8kzj: 0
* bexhoma-sut-hardware-4-1783815447-64dbfd4554-hx2m7: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-2 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-3 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-4 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-2 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-3 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-4 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         69 |                  2 |                                2391.19 |                                60.00 |                               0.89 |                             1769850.89 |                                     1728.37 |                                  0.00 |        0 |
| Hardware-2-1-1-1-1 | Hardware-2-1-1 | Hardware-2-1-1-1 |                1 |        1 |               1 |       1 |        180 |                  2 |                                2401.49 |                                60.00 |                               0.86 |                             3856651.33 |                                     3766.26 |                                  0.00 |        0 |
| Hardware-3-1-1-1-1 | Hardware-3-1-1 | Hardware-3-1-1-1 |                1 |        1 |               1 |       1 |        153 |                  2 |                                2386.91 |                                60.00 |                               0.89 |                             3507132.96 |                                     3424.93 |                                  0.00 |        0 |
| Hardware-4-1-1-1-1 | Hardware-4-1-1 | Hardware-4-1-1-1 |                1 |        1 |               1 |       1 |        128 |                  2 |                                2393.81 |                                60.00 |                               0.89 |                             2671808.15 |                                     2609.19 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-0 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |         69 |                  2 |                                2391.19 |                                60.00 |                               0.89 |                             1769850.89 |                                     1728.37 |                                  0.00 |        0 |
| Hardware-2-1-1-1 | Hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |        180 |                  2 |                                2401.49 |                                60.00 |                               0.86 |                             3856651.33 |                                     3766.26 |                                  0.00 |        0 |
| Hardware-3-1-1-2 | Hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |        153 |                  2 |                                2386.91 |                                60.00 |                               0.89 |                             3507132.96 |                                     3424.93 |                                  0.00 |        0 |
| Hardware-4-1-1-3 | Hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |        128 |                  2 |                                2393.81 |                                60.00 |                               0.89 |                             2671808.15 |                                     2609.19 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       126.04 |      2.00 |           0.21 |                  0.21 |
| Hardware-2-1-1-1 |       123.29 |      2.00 |           0.21 |                  0.21 |
| Hardware-3-1-1-1 |        66.61 |      2.00 |           0.21 |                  0.21 |
| Hardware-4-1-1-1 |        65.04 |      1.93 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         4.00 |      0.15 |           0.01 |                  0.01 |
| Hardware-2-1-1-1 |         7.54 |      0.18 |           0.01 |                  0.01 |
| Hardware-3-1-1-1 |         1.82 |      0.17 |           0.01 |                  0.01 |
| Hardware-4-1-1-1 |         1.42 |      0.18 |           0.01 |                  0.01 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

</details>


The Per Phase table is grouped per tenant (one row per co-located SUT pod); compare each tenant's
`hardware_sysbench_cpu_events_per_sec` against the single-pod baseline from the CPU-quota
calibration example above at the same thread count.

---
## Netperf

### What is netperf

[netperf](https://github.com/HewlettPackard/netperf) is Hewlett Packard's open-source network
performance benchmark, most commonly run in `TCP_RR`/`UDP_RR` request/response mode against its
`netserver` companion daemon. `netserver` forks a child per incoming test session natively, so it
is well suited to measuring how round-trip latency and throughput behave as the number of
concurrent connections to a single server grows.

References:
1. netperf: https://github.com/HewlettPackard/netperf
1. netperf manual, "Care and Feeding of Netperf" (TCP_RR, concurrent instances): https://hewlettpackard.github.io/netperf/doc/netperf.html
1. PostgreSQL `max_connections`: https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS
1. PgBouncer pool sizing: https://www.pgbouncer.org/config.html#pool_size

### Using netperf in bexhoma

Select it with `-xht netperf`. `-xtd` sets the run duration and `-xnpp` picks the protocol
(`tcp`/`udp`, selecting `TCP_RR`/`UDP_RR`). `-nbt` sweeps concurrent connections from a single
benchmarker pod; `-nbp` instead sweeps how many benchmarker pods carry a fixed total connection
count. Each benchmarker pod connects directly to a single shared `netserver` instance on the SUT
over the Kubernetes Service rather than over SSH, so the fio/sysbench storage/SSH-related flags do
not apply.

### Examples

#### 1. Single-connection round-trip latency baseline (TCP_RR)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_query_latency.log
```

This runs a single `TCP_RR` connection between one benchmarking pod and the SUT, synchronous
request/reply with no think time, for 60 seconds — the baseline commands 18 and 19 build on.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_netperf_postgresql_query_latency_summary.md" target="_blank" rel="noopener">docs_hardware_netperf_postgresql_query_latency.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 238s 
* Code: 1783815862
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
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
  * disk:1062832
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783815862

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783815862-65cbdfb4fb-ldwn6: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         61 |                  1 | tcp                         |                             8758.24 |                              0.11 |                              0.09 |                              0.26 |                              0.38 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         61 |                  1 | tcp                         |                             8758.24 |                              0.11 |                              0.08 |                              0.26 |                              0.38 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         7.71 |      0.17 |           0.20 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        11.43 |      0.31 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

</details>

`hardware_netperf_transaction_rate` and the `hardware_netperf_latency_*_ms` columns report the
observed transaction rate and round-trip latency for this connection.


---
#### 2. Concurrent-connection scaling (TCP_RR, `-nbt` sweep)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1 \
  -nbt 1,8,16,32,64 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_connection_scaling_sweep.log
```

This runs 1, 8, 16, 32, and 64 concurrent `TCP_RR` connections from a single benchmarking pod, one
round per value.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_netperf_postgresql_connection_scaling_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_netperf_postgresql_connection_scaling_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 747s 
* Code: 1783816119
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 8, 16, 32, 64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062834
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062834
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062835
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062835
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062836
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816119

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783816119-654989dc44-2wsdf: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         60 |                  1 | tcp                         |                             8735.47 |                              0.11 |                              0.08 |                              0.27 |                              0.38 |                                0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                  8 | tcp                         |                            65369.99 |                              0.13 |                              0.10 |                              0.33 |                              0.46 |                                0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         62 |                 16 | tcp                         |                           117147.15 |                              0.16 |                              0.11 |                              0.37 |                              0.50 |                                0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         65 |                 32 | tcp                         |                           181885.25 |                              0.23 |                              0.17 |                              0.45 |                              0.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         69 |                 64 | tcp                         |                           251881.02 |                              0.36 |                              0.35 |                              0.76 |                              2.04 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         60 |                  1 | tcp                         |                             8735.47 |                              0.11 |                              0.08 |                              0.26 |                              0.38 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                  8 | tcp                         |                            65369.99 |                              0.13 |                              0.10 |                              0.33 |                              0.46 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         62 |                 16 | tcp                         |                           117147.15 |                              0.16 |                              0.11 |                              0.37 |                              0.50 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         65 |                 32 | tcp                         |                           181885.25 |                              0.23 |                              0.17 |                              0.45 |                              0.64 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         69 |                 64 | tcp                         |                           251881.02 |                              0.36 |                              0.35 |                              0.76 |                              2.04 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         5.39 |      0.15 |           0.20 |                  0.20 |
| Hardware-1-1-2-1 |        70.63 |      1.29 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       140.24 |      2.46 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |       235.34 |      4.18 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       315.17 |      5.41 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        13.05 |      0.29 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |        92.18 |      2.93 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |       266.56 |      8.53 |           0.01 |                  0.01 |
| Hardware-1-1-4-1 |       513.82 |     17.45 |           0.01 |                  0.01 |
| Hardware-1-1-5-1 |      1014.53 |     35.66 |           0.02 |                  0.02 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

</details>

Compare `hardware_netperf_transaction_rate` and `hardware_netperf_latency_*_ms` across the five
rows of the Per Phase table to see how they change as connection count grows.


---
#### 3. Pod-count scaling at fixed total concurrency (TCP_RR, `-nbp` sweep)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht netperf \
  -xtd 60 \
  -xnpp tcp \
  -nbp 1,2 \
  -nbt 64 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_netperf_postgresql_pod_scaling_sweep.log
```

This runs 64 concurrent `TCP_RR` connections split across 1 and then 2 benchmarking pods, keeping
the total connection count constant — the same shape as the pod-count comparisons used for other
benchmark types in this repo (e.g. [`Example-Benchbase.md`](Example-Benchbase.md)), but with no
database engine in the loop.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_netperf_postgresql_pod_scaling_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_netperf_postgresql_pod_scaling_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 376s 
* Code: 1783816891
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [64] threads, split into [1, 2] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062837
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816891
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062838
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783816891

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783816891-58dd6f5bd6-snj6p: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         69 |                 64 | tcp                         |                           252207.00 |                              0.46 |                              0.37 |                              0.98 |                              1.76 |                                0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                 32 | tcp                         |                           124343.22 |                              0.45 |                              0.27 |                              1.14 |                              2.27 |                                0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                 32 | tcp                         |                           122771.18 |                              0.44 |                              0.32 |                              1.12 |                              2.21 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         69 |                 64 | tcp                         |                           252207.00 |                              0.46 |                              0.37 |                              0.98 |                              1.76 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                 64 | tcp                         |                           247114.40 |                              0.45 |                              0.32 |                              1.14 |                              2.27 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       179.97 |      5.07 |           0.22 |                  0.22 |
| Hardware-1-1-2-1 |       280.65 |      5.46 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |      1106.01 |     18.06 |           0.02 |                  0.02 |
| Hardware-1-1-2-1 |       670.04 |     35.45 |           0.01 |                  0.01 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

</details>

Compare `hardware_netperf_transaction_rate` and `hardware_netperf_latency_*_ms` between the two
rows of the Per Phase table to see how they change when the same total connection count is split
across more pods.


---
## Sockperf

### What is sockperf

[sockperf](https://github.com/Mellanox/sockperf) is a network benchmarking utility (originally
from Mellanox/NVIDIA) for measuring TCP/UDP socket latency and throughput. Unlike netperf's
`TCP_RR`, it supports both a synchronous ping-pong mode and a continuous under-load streaming
mode, and reports full latency percentiles rather than just an average. bexhoma runs it against a
static pool of dedicated sockperf server processes on the SUT, so single-connection network
latency/throughput can be measured independent of concurrent-connection scaling effects.

References:
1. sockperf: https://github.com/Mellanox/sockperf

### Using sockperf in bexhoma

Select it with `-xht sockperf`. `-xtd` sets the run duration; `-xspm` picks ping-pong (`pp`) or
continuous-load (`ul`) mode, `-xspr` the send rate (a number or `max`), `-xsps` the message size in
bytes, and `-xspp` the protocol (`tcp`/`udp`). `-nbp` sweeps how many benchmarker pods connect
concurrently, each to its own dedicated sockperf server on the SUT over the Kubernetes Service
rather than over SSH, so the fio/sysbench storage/SSH-related flags do not apply.

### Examples

#### 1. Pod/client scaling sweep

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm ul \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1,2,4,8,16 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_pod_scaling_sweep.log
```

This sweeps `-nbp` from 1 to 16 pods under continuous max-rate load (`-xspm ul -xspr max`) with a
generic 64-byte message. Compare the summed `hardware_sockperf_msg_rate_per_sec` across the five
rows of the Per Phase table to see whether aggregate throughput scales linearly with pod count or
flattens out; the `-mc` CPU columns for the SUT deployment versus the benchmarker component show
which side (server or client) would be driving any flattening. Within a single round, compare
`hardware_sockperf_latency_avg_ms` across the Per Connection table's children (one row per pod) —
a uniform value means the shared server pool is handling concurrent pods evenly, an uneven spread
points to contention on specific servers.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sockperf_pod_scaling_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_sockperf_pod_scaling_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 920s 
* Code: 1783817286
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062847
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062847
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062848
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062849
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062850
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783817286

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783817286-99d9447cf-5cq8c: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

### Execution

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.21 |                               0.16 |                               0.81 |                                1.03 |                              5032.78 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.20 |                               0.14 |                               0.83 |                                1.69 |                              5095.58 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.15 |                               0.10 |                               0.60 |                                2.95 |                              4506.94 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.40 |                               0.34 |                               0.82 |                               20.44 |                              4343.30 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.16 |                               0.12 |                               0.63 |                                1.05 |                              4437.83 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.37 |                               0.34 |                               0.81 |                                1.16 |                              4243.78 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.20 |                               0.14 |                               0.72 |                                1.08 |                              4973.87 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.19 |                               0.14 |                               0.88 |                                6.12 |                              3747.07 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.19 |                               1.25 |                                7.79 |                              3557.04 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.16 |                               0.12 |                               0.74 |                                1.60 |                              3657.04 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.27 |                               0.18 |                               1.24 |                               14.63 |                              3505.14 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.24 |                               0.19 |                               0.98 |                                1.62 |                              4220.37 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.19 |                               0.13 |                               0.78 |                                8.84 |                              4222.38 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.16 |                               0.12 |                               0.72 |                                2.27 |                              3549.41 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.20 |                               0.14 |                               0.93 |                                3.23 |                              4112.23 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               4.80 |                               4.71 |                              10.89 |                               21.65 |                              3945.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.26 |                               0.13 |                               1.61 |                                2.73 |                              3756.69 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               4.66 |                               4.69 |                               8.23 |                               12.11 |                              4026.99 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.25 |                               0.14 |                               1.62 |                                2.88 |                              3708.51 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         73 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               4.66 |                               4.68 |                               7.68 |                                8.67 |                              5286.58 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.27 |                               0.16 |                               1.67 |                                3.22 |                              3743.20 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               4.81 |                               4.81 |                               8.78 |                               13.02 |                              4859.74 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.22 |                               0.13 |                               1.52 |                                2.42 |                              2141.28 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.23 |                               0.15 |                               1.53 |                                2.69 |                              2139.93 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               4.76 |                               4.77 |                               8.52 |                               10.31 |                              5324.48 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               4.67 |                               4.69 |                               7.81 |                                8.99 |                              5285.36 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               0.22 |                               0.13 |                               1.52 |                                2.51 |                              2313.22 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               0.22 |                               0.13 |                               1.51 |                                2.44 |                              2440.36 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.24 |                               0.13 |                               1.67 |                                3.84 |                              3520.78 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               4.86 |                               4.76 |                              10.83 |                               15.46 |                              3992.93 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.23 |                               0.12 |                               1.62 |                                2.95 |                              3646.20 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | ul                       | tcp                          |                          64 | max                     |                               0.21 |                               0.16 |                               0.81 |                                1.03 |                              5032.78 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         64 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.20 |                               0.14 |                               0.83 |                                2.95 |                              9602.53 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.40 |                               0.34 |                               0.82 |                               20.44 |                             17998.79 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.27 |                               0.19 |                               1.25 |                               14.63 |                             30570.69 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                               4.86 |                               4.81 |                              10.89 |                               21.65 |                             60131.90 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.54 |      0.19 |           0.20 |                  0.21 |
| Hardware-1-1-2-1 |        17.33 |      0.40 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |        25.27 |      0.62 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |        81.32 |      1.65 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |        89.43 |      2.31 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        43.42 |      1.04 |           0.10 |                  0.10 |
| Hardware-1-1-2-1 |        66.02 |      2.95 |           0.10 |                  0.10 |
| Hardware-1-1-3-1 |       158.98 |      6.11 |           0.10 |                  0.10 |
| Hardware-1-1-4-1 |       181.08 |     12.16 |           0.10 |                  0.10 |
| Hardware-1-1-5-1 |       462.59 |     22.90 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

</details>


The summed `hardware_sockperf_msg_rate_per_sec` across the Per Phase table's rows shows whether
aggregate throughput scales with pod count or flattens out; the `-mc` CPU columns for the SUT
deployment versus the benchmarker component show which side would be driving any flattening.

---
#### 2. PostgreSQL simple-query round-trip latency (ping-pong, TCP)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm pp \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_query_latency.log
```

`-xspm pp` mirrors PostgreSQL's synchronous simple-query protocol: one connection sends, blocks
for the reply, sends the next; `-xspr max` fires the next request the instant the previous reply
lands, giving the single-connection round-trip latency ceiling — the network-latency analogue of
the WAL fsync "single outstanding write" tests in the fio section above.
`hardware_sockperf_latency_avg_ms`/`_p50_ms`/`_p99_ms`/`_p999_ms` in the result table give this
floor, and `hardware_sockperf_msg_rate_per_sec` reports how many round trips per second that
translates to for a single connection — the baseline command 23 repeats at growing pod counts.

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sockperf_postgresql_query_latency_summary.md" target="_blank" rel="noopener">docs_hardware_sockperf_postgresql_query_latency.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 209s 
* Code: 1783818228
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
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
  * disk:1062851
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818228

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783818228-5456949c59-2dfcp: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.05 |                               0.04 |                               0.18 |                                0.23 |                              9302.15 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.05 |                               0.04 |                               0.18 |                                0.23 |                              9302.15 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         8.62 |      0.18 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        15.27 |      0.32 |           0.55 |                  0.55 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

</details>


`hardware_sockperf_latency_avg_ms`/`_p50_ms`/`_p99_ms`/`_p999_ms` in the result table give the
single-connection round-trip latency floor, and `hardware_sockperf_msg_rate_per_sec` reports how
many round trips per second that translates to.

---
#### 3. PostgreSQL streaming/bulk throughput (WAL sender/COPY, TCP, 8k)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm ul \
  -xspr max \
  -xsps 8192 \
  -xspp tcp \
  -nbp 1 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_streaming_throughput.log
```

`-xspm ul` (continuous one-way stream) models WAL streaming replication or a `COPY`/bulk result
transfer rather than a request/reply cycle. `-xsps 8192` is PostgreSQL's page size (`BLCKSZ`) in
bytes — the same 8k anchor already used throughout the fio section — so this becomes the
network-throughput counterpart to those page-sized fio numbers.
`hardware_sockperf_msg_rate_per_sec` multiplied by the message size gives an effective throughput
figure comparable to fio's IOPS-at-blocksize numbers; comparing this round's `_p99_ms`/`_p999_ms`
against command 21's narrower 64-byte percentiles shows how much of the tail latency here is
payload transfer time rather than queuing (there is only one stream, so no concurrent-pod
contention to separate out).

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sockperf_postgresql_streaming_throughput_summary.md" target="_blank" rel="noopener">docs_hardware_sockperf_postgresql_streaming_throughput.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 241s 
* Code: 1783818455
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [8192] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
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
  * disk:1062853
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818455

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783818455-7bd7fd455f-4g6qz: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                  1 | ul                       | tcp                          |                        8192 | max                     |                    20000 |                               0.33 |                               0.14 |                               4.60 |                                4.97 |                              1264.82 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                  1 | ul                       | tcp                          |                        8192 | max                     |                               0.33 |                               0.14 |                               4.60 |                                4.97 |                              1264.82 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        13.71 |      0.34 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        48.62 |      1.01 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

</details>


`hardware_sockperf_msg_rate_per_sec` multiplied by the message size gives an effective throughput
figure comparable to fio's IOPS-at-blocksize numbers.

---
#### 4. PostgreSQL query latency under concurrent connections (ping-pong, TCP, `-nbp` sweep)

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht sockperf \
  -xtd 60 \
  -xspm pp \
  -xspr max \
  -xsps 64 \
  -xspp tcp \
  -nbp 1,2,4,8,16 \
  -nbt 1 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_sockperf_postgresql_latency_scaling_sweep.log
```

Same shape as command 21 (ping-pong, tcp, 64-byte message — one synchronous request/reply loop
per pod), but sweeping `-nbp 1,2,4,8,16` like command 20 instead of fixing it at 1. Compare
`hardware_sockperf_latency_avg_ms` (and its percentiles) per pod across the five rounds to see
whether an individual connection's round-trip latency holds steady as concurrency grows or
degrades; compare the summed `hardware_sockperf_msg_rate_per_sec` in the Per Phase table against
command 20's to see whether this self-paced request/reply pattern scales differently than
continuous max-rate send. This is the pairing that answers the `max_connections`/PgBouncer
pool-size question directly: as concurrent connections grow, does throughput or does per-connection
latency degrade first?

##### Show results

<details>
<summary>Show <a href="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/logs_tests/docs_hardware_sockperf_postgresql_latency_scaling_sweep_summary.md" target="_blank" rel="noopener">docs_hardware_sockperf_postgresql_latency_scaling_sweep.log</a></summary>

```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 882s 
* Code: 1783818715
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Experiment uses bexhoma version 0.10.4.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062854
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062854
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062855
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062856
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:1062856
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783818715

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783818715-5dd5cb7499-qrc7t: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)
* DBMS Hardware-1 - Experiment 1 Client 4: hardware (8 pods)
* DBMS Hardware-1 - Experiment 1 Client 5: hardware (16 pods)

### Execution

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8981.58 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.19 |                                0.25 |                              9071.91 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.21 |                                0.26 |                              8224.08 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.18 |                                0.22 |                              7981.43 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.04 |                               0.18 |                                0.22 |                              8544.53 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                              8445.59 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                              8434.48 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7597.16 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.07 |                               0.05 |                               0.21 |                                0.26 |                              6950.45 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7328.68 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.07 |                               0.05 |                               0.20 |                                0.25 |                              7165.44 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.05 |                               0.04 |                               0.19 |                                0.24 |                              9416.81 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.05 |                               0.21 |                                0.26 |                              7036.94 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.05 |                               0.21 |                                0.27 |                              6861.70 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.05 |                               0.20 |                                0.26 |                              7278.15 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7155.87 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.05 |                               0.22 |                                0.27 |                              7992.73 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.07 |                               0.05 |                               0.23 |                                0.27 |                              7456.37 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         74 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                              6135.87 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6438.71 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              6656.89 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.05 |                               0.23 |                                0.28 |                              7364.32 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7100.54 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.07 |                               0.05 |                               0.24 |                                0.27 |                              7167.94 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.07 |                               0.05 |                               0.24 |                                0.28 |                              7216.14 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.08 |                               0.06 |                               0.24 |                                0.28 |                              6573.64 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.07 |                               0.05 |                               0.23 |                                0.28 |                              7646.65 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6317.09 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                              6334.91 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.06 |                               0.05 |                               0.23 |                                0.27 |                              7858.59 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6430.76 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8981.58 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.05 |                               0.21 |                                0.26 |                             17295.99 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.22 |                             33406.03 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.07 |                               0.05 |                               0.21 |                                0.27 |                             59635.33 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.06 |                               0.25 |                                0.28 |                            111847.01 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         9.17 |      0.18 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        10.52 |      0.34 |           0.20 |                  0.20 |
| Hardware-1-1-3-1 |        24.70 |      0.66 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |        73.96 |      1.36 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       140.80 |      2.58 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.72 |      0.31 |           0.55 |                  0.55 |
| Hardware-1-1-2-1 |        31.04 |      0.93 |           0.55 |                  0.55 |
| Hardware-1-1-3-1 |        54.38 |      1.81 |           0.55 |                  0.55 |
| Hardware-1-1-4-1 |        99.45 |      3.42 |           0.55 |                  0.55 |
| Hardware-1-1-5-1 |       224.61 |      7.37 |           0.55 |                  0.55 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

</details>


`hardware_sockperf_latency_avg_ms` (and its percentiles) per pod across the Per Phase table's rows
shows whether an individual connection's round-trip latency holds steady as concurrency grows, or
degrades — the pairing that answers the `max_connections`/PgBouncer pool-size question directly.

---
## Adjust Parameters

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s
(`deploymenttemplate-Hardware.yml`, `jobtemplate-benchmarking-hardware.yml`).

### Benchmarker script

The fio, sysbench, sockperf, and netperf invocations themselves live in
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_fio.sh ,
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_sysbench.sh ,
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_sockperf.sh ,
and https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_netperf.sh

### Command line

You maybe want to adjust some of the parameters that are set in the file: `python hardware.py -h`

```bash
usage: hardware.py [-h] [-aws] [-db] [-sl] [-ss] [-cx CONTEXT] [-e EXPERIMENT]
                   [-m] [-ma] [-mc] [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
                   [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER]
                   [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS]
                   [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS]
                   [-nbp NUM_BENCHMARKING_PODS]
                   [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
                   [-t TIMEOUT] [-lr LIMIT_RAM] [-lc LIMIT_CPU]
                   [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE]
                   [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
                   [-rst {None,,local-hdd,shared,ramdisk,cephcsi}]
                   [-rss REQUEST_STORAGE_SIZE] [-rsr]
                   [-rnn [REQUEST_NODE_NAME]] [-rnl [REQUEST_NODE_LOADING]]
                   [-rnb [REQUEST_NODE_BENCHMARKING]] [-mtn MULTI_TENANT_NUM]
                   [-mtb MULTI_TENANT_BY] [-mtv] [-tr] [--set SETS]
                   [-dbms [{Hardware} ...]]
                   [-xht {fio,sysbench,sockperf,netperf}] [-xts HARDWARE_SIZE]
                   [-xtd HARDWARE_DURATION] [-xfrw FIO_RW] [-xfbs FIO_BS]
                   [-xfid FIO_IODEPTH] [-xfe FIO_ENGINE] [-xfsy FIO_FSYNC]
                   [-xffd FIO_FDATASYNC] [-xfmx FIO_RWMIXREAD]
                   [-xspm SOCKPERF_MODE] [-xspr SOCKPERF_MPS]
                   [-xsps SOCKPERF_MSGSIZE] [-xspp SOCKPERF_PROTOCOL]
                   [-xnpp NETPERF_PROTOCOL]
                   {run,start,summary}

Run Hardware (fio/sysbench/sockperf/netperf) benchmarks against a SUT in
Kubernetes. Controls fio workload shape (read/write pattern, block size, queue
depth, engine), selects sysbench for CPU/memory benchmarking, sockperf for
single-connection network latency/throughput benchmarking under a controlled
send rate, or netperf for many-concurrent-connection request/response
(TCP_RR/UDP_RR) network benchmarking.

positional arguments:
  {run,start,summary}   experiment phase: start SUT only, run the benchmark,
                        or summarize results

options:
  -h, --help            show this help message and exit
  -aws, --aws           pin components to AWS EKS node groups
  -db, --debug          enable debug logging
  -sl, --skip-loading   skip data loading and start benchmarking immediately
  -ss, --skip-shutdown  keep SUT pods running after the experiment finishes
  -cx CONTEXT, --context CONTEXT
                        kubectl context to use (default: current context)
  -e EXPERIMENT, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -ms MAX_SUT, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse MAX_SUT_EXPERIMENT, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -nc NUM_CONFIG, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne NUM_QUERY_EXECUTORS, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw NUM_WORKER, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr NUM_WORKER_REPLICAS, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws NUM_WORKER_SHARDS, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -nlp NUM_LOADING_PODS, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt NUM_LOADING_THREADS, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp NUM_BENCHMARKING_PODS, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt NUM_BENCHMARKING_THREADS, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf SCALING_FACTOR, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t TIMEOUT, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr LIMIT_RAM, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit)
  -lc LIMIT_CPU, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit)
  -rr REQUEST_RAM, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi)
  -rc REQUEST_CPU, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4)
  -rct REQUEST_CPU_TYPE, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg REQUEST_GPU, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt REQUEST_GPU_TYPE, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst {None,,local-hdd,shared,ramdisk,cephcsi}, --request-storage-type {None,,local-hdd,shared,ramdisk,cephcsi}
                        storage class for the SUT persistent volume
  -rss REQUEST_STORAGE_SIZE, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rnn [REQUEST_NODE_NAME], --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl [REQUEST_NODE_LOADING], --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb [REQUEST_NODE_BENCHMARKING], --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -mtn MULTI_TENANT_NUM, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb MULTI_TENANT_BY, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -tr, --test-result    validate that results meet basic correctness
                        requirements
  --set SETS            override a deployment parameter, e.g. deployment[sut].
                        container[dbms].max_worker_processes=128
  -dbms [{Hardware} ...], --dbms [{Hardware} ...]
                        hardware target(s) to test
  -xht {fio,sysbench,sockperf,netperf}, --xhardware-type {fio,sysbench,sockperf,netperf}
                        benchmark tool: fio (disk I/O), sysbench (CPU/memory),
                        sockperf (single-connection network
                        latency/throughput), or netperf (many-concurrent-
                        connection request/response)
  -xts HARDWARE_SIZE, --xtest-size HARDWARE_SIZE
                        fio test file size (e.g. 1G, 64G)
  -xtd HARDWARE_DURATION, --xtest-duration HARDWARE_DURATION
                        fio/sysbench/sockperf run duration in seconds
  -xfrw FIO_RW, --xfio-rw FIO_RW
                        comma-separated fio I/O patterns to sweep, each in
                        {write, read, randwrite, randread, randrw}
  -xfbs FIO_BS, --xfio-blocksize FIO_BS
                        comma-separated fio block sizes to sweep (e.g.
                        4k,64k,1M)
  -xfid FIO_IODEPTH, --xfio-iodepth FIO_IODEPTH
                        comma-separated fio queue depths to sweep
  -xfe FIO_ENGINE, --xfio-engine FIO_ENGINE
                        comma-separated fio ioengines to sweep, each in {sync,
                        libaio, io_uring}
  -xfsy FIO_FSYNC, --xfio-fsync FIO_FSYNC
                        comma-separated fsync intervals to sweep (0 disables
                        fsync); use fsync xor fdatasync, not both
  -xffd FIO_FDATASYNC, --xfio-fdatasync FIO_FDATASYNC
                        comma-separated fdatasync intervals to sweep (0
                        disables fdatasync); use fsync xor fdatasync, not both
  -xfmx FIO_RWMIXREAD, --xfio-rwmixread FIO_RWMIXREAD
                        comma-separated read percentages to sweep when
                        -xfrw=randrw
  -xspm SOCKPERF_MODE, --xsockperf-mode SOCKPERF_MODE
                        comma-separated sockperf modes to sweep, each in {pp,
                        ul}
  -xspr SOCKPERF_MPS, --xsockperf-mps SOCKPERF_MPS
                        comma-separated message rates to sweep (messages/sec);
                        each value is a positive integer or the literal "max"
  -xsps SOCKPERF_MSGSIZE, --xsockperf-msgsize SOCKPERF_MSGSIZE
                        comma-separated message payload sizes in bytes to
                        sweep
  -xspp SOCKPERF_PROTOCOL, --xsockperf-protocol SOCKPERF_PROTOCOL
                        comma-separated sockperf protocols to sweep, each in
                        {tcp, udp}
  -xnpp NETPERF_PROTOCOL, --xnetperf-protocol NETPERF_PROTOCOL
                        comma-separated netperf protocols to sweep, each in
                        {tcp, udp} (selects TCP_RR/UDP_RR)
```
