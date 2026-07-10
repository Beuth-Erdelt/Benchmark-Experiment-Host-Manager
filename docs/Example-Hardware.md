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
connections grow (relevant to `max_connections`/PgBouncer pool sizing). This page walks through
the fio, sysbench, netperf, and sockperf sweeps in
[`scripts/test-docs-hardware.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.ps1) /
[`scripts/test-docs-hardware.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.sh)
and explains what each one is for.

**The results are not official benchmark results.
Exact performance depends on a number of parameters, including the underlying storage class,
node hardware, and cluster load at the time of the run.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

Result tables below are real output from an actual cluster run of every command on this page.

References:
1. fio documentation: https://fio.readthedocs.io/en/latest/fio_doc.html
1. fio `--fsync` / `--fdatasync`: https://fio.readthedocs.io/en/latest/fio_doc.html#cmdoption-arg-fsync
1. PostgreSQL WAL configuration: https://www.postgresql.org/docs/current/wal-configuration.html
1. PostgreSQL `effective_io_concurrency`: https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY
1. sockperf: https://github.com/Mellanox/sockperf
1. netperf: https://github.com/HewlettPackard/netperf
1. netperf manual, "Care and Feeding of Netperf" (TCP_RR, concurrent instances): https://hewlettpackard.github.io/netperf/doc/netperf.html
1. PostgreSQL `max_connections`: https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS
1. PgBouncer pool sizing: https://www.pgbouncer.org/config.html#pool_size

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

Unlike every other entry script, `hardware.py` has no loader — there is nothing to import
before benchmarking, so every command below goes straight to `run`. The page covers four groups
of commands: twelve `-xht fio` disk-I/O commands, four `-xht sysbench` CPU/memory commands, three
`-xht netperf` many-concurrent-connection request/response commands, and four `-xht sockperf`
single-connection network latency/throughput commands.

The twelve fio commands all share the same `Hardware-1` SUT/PVC and run **sequentially**; two
`hardware.py run` invocations must never overlap in time, because the PVC name is fixed
(`storage_label='hardware'`, not scoped by experiment code) and a second SUT pod would either
fail to attach the volume or silently write into the same test-file path as the first (see the
project notes on `-rsr` and PVC sharing). Each of them passes `-rsr` so it starts from a freshly
recreated, empty volume rather than inheriting whatever an earlier command left on the PVC — fio
creates one full `-xts`-sized file per `numjobs` thread with no cleanup between rounds by
default, so `-rss` is sized per command to the largest single round it will run (most stay at the
default `50Gi`; the numjobs and group-commit sweeps go up to `80Gi`/`150Gi` since they sweep
`numjobs` as high as 16/32).

The four sysbench commands (13-16), three netperf commands (17-19), and four sockperf commands
(20-23) are CPU/memory and network-only respectively — no disk I/O, so none of them use
`-rst`/`-rss`/`-rsr` and the PVC-sharing constraint above doesn't apply to them. netperf and
sockperf traffic also do not go over SSH the way fio/sysbench do — each benchmarker pod connects
directly to netserver/a dedicated sockperf server on the SUT over the Kubernetes Service instead of
executing commands on the SUT via SSH.

The fio workload flags (`-xfrw`, `-xfbs`, `-xfid`, `-xfe`, `-xfsy`, `-xffd`, `-xfmx`), the netperf
workload flag (`-xnpp`), and the sockperf workload flags (`-xspm`, `-xspr`, `-xsps`, `-xspp`) each
accept a comma-separated list. Every combination across the lists is run as one more sequential
round against the same SUT, so a parameter sweep is expressed as a single invocation instead of one
process per value — see `python hardware.py -h` at the bottom of this page.

---

## Fio disk benchmarks

The twelve commands below (`-xht fio`) cover raw disk I/O: queue-depth and block-size
characterization, PostgreSQL-page-size calibration, and WAL/durability/checkpoint simulation.

### 1. Queue-depth sweep

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

### Result

docs_hardware_fio_depth_sweep.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2294s 
* Code: 1783188404
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [1, 2, 4, 8, 16, 32, 64, 128].
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
  * disk:819565
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824021
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817879
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818006
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819794
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818889
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821465
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826315
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822628
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822032
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821880
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823130
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817718
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822412
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817960
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818215
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783188404

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783188404-77b66d7746-mcz5n: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         72 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                    67.09 |                      0.00 |                          36.44 |                            0.00 |                          86.51 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         70 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                   153.10 |                      0.00 |                          31.85 |                            0.00 |                          76.02 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         71 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                   303.88 |                      0.00 |                          36.44 |                            0.00 |                          98.04 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         71 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                   739.75 |                      0.00 |                          32.64 |                            0.00 |                          81.26 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         70 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                  1676.72 |                      0.00 |                          26.08 |                            0.00 |                          72.88 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         73 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2344.08 |                      0.00 |                          39.58 |                            0.00 |                         126.35 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4036.87 |                      0.00 |                          52.17 |                            0.00 |                         166.72 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         71 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5875.08 |                      0.00 |                          81.26 |                            0.00 |                         337.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     82.79 |                           0.00 |                           41.68 |                           0.00 |                           94.90 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         63 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    138.53 |                           0.00 |                           54.79 |                           0.00 |                          102.24 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         63 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    263.75 |                           0.00 |                           58.98 |                           0.00 |                          122.16 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    385.27 |                           0.00 |                           73.92 |                           0.00 |                          189.79 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         63 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    768.98 |                           0.00 |                           76.02 |                           0.00 |                          189.79 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         62 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1187.86 |                           0.00 |                          108.53 |                           0.00 |                          219.15 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-15-1-1 | Hardware-1-1-15 | Hardware-1-1-15-1 |                1 |       15 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1783.67 |                           0.00 |                          143.65 |                           0.00 |                          261.10 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-16-1-1 | Hardware-1-1-16 | Hardware-1-1-16-1 |                1 |       16 |               1 |       1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   3287.80 |                           0.00 |                          162.53 |                           0.00 |                          261.10 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         72 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    67.09 |                      0.00 |                          36.44 |                            0.00 |                          86.51 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         70 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   153.10 |                      0.00 |                          31.85 |                            0.00 |                          76.02 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         71 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   303.88 |                      0.00 |                          36.44 |                            0.00 |                          98.04 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         71 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                   739.75 |                      0.00 |                          32.64 |                            0.00 |                          81.26 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         70 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  1676.72 |                      0.00 |                          26.08 |                            0.00 |                          72.88 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         73 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  2344.08 |                      0.00 |                          39.58 |                            0.00 |                         126.35 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4036.87 |                      0.00 |                          52.17 |                            0.00 |                         166.72 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         71 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  5875.08 |                      0.00 |                          81.26 |                            0.00 |                         337.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     82.79 |                           0.00 |                           41.68 |                           0.00 |                           94.90 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         63 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    138.53 |                           0.00 |                           54.79 |                           0.00 |                          102.24 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         63 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    263.75 |                           0.00 |                           58.98 |                           0.00 |                          122.16 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    385.27 |                           0.00 |                           73.92 |                           0.00 |                          189.79 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         63 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    768.98 |                           0.00 |                           76.02 |                           0.00 |                          189.79 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         62 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1187.86 |                           0.00 |                          108.53 |                           0.00 |                          219.15 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1783.67 |                           0.00 |                          143.65 |                           0.00 |                          261.10 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3287.80 |                           0.00 |                          162.53 |                           0.00 |                          261.10 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        58.46 |      2.03 |           0.02 |                  4.02 |
| Hardware-1-1-2-1  |        59.58 |      2.00 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        61.58 |      1.67 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        62.67 |      2.12 |           0.03 |                  4.03 |
| Hardware-1-1-5-1  |        62.89 |      2.34 |           0.02 |                  0.02 |
| Hardware-1-1-6-1  |        64.63 |      1.60 |           0.03 |                  4.03 |
| Hardware-1-1-7-1  |        52.98 |      1.43 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        52.85 |      1.30 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        58.73 |      1.62 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        62.15 |      2.77 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        62.97 |      2.18 |           0.02 |                  0.02 |
| Hardware-1-1-12-1 |        62.34 |      1.46 |           0.03 |                  0.03 |
| Hardware-1-1-13-1 |        63.76 |      2.10 |           0.02 |                  0.02 |
| Hardware-1-1-14-1 |        65.04 |      1.83 |           0.02 |                  0.02 |
| Hardware-1-1-15-1 |        67.95 |      2.45 |           0.02 |                  0.02 |
| Hardware-1-1-16-1 |        71.27 |      2.43 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.52 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.54 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.52 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.44 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.51 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.49 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.51 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.45 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.51 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.44 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-15-1 |         0.46 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-16-1 |         0.52 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per queue depth, with IOPS and completion-latency percentiles
aggregated across all pods in that round.

---

### 2. Depth-sweep refinement around the elbow

The coarse sweep above only localizes the elbow to "somewhere between 64 and 128" — each doubling
step covers a wide range. This does a linear pass inside that bracket to pinpoint the actual knee
instead of just the bracket containing it.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 64,80,96,112,128 \
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
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_refine.log
```

10 rounds (2 patterns × 5 depths) ≈ 10 minutes.

### Result

docs_hardware_fio_depth_sweep_refine.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1436s 
* Code: 1783194420
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [64, 80, 96, 112, 128].
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
  * disk:822252
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830607
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825422
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:830646
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826119
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821292
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819472
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819602
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:817519
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:827330
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783194420

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783194420-65c8bf6b44-5bmdx: 0

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

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         72 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3313.16 |                      0.00 |                          50.59 |                            0.00 |                         175.11 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         71 | randread          | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4361.20 |                      0.00 |                          49.02 |                            0.00 |                         206.57 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         72 | randread          | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4002.56 |                      0.00 |                          65.27 |                            0.00 |                         396.36 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         72 | randread          | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4200.43 |                      0.00 |                          79.17 |                            0.00 |                         413.14 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         70 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5286.49 |                      0.00 |                          78.12 |                            0.00 |                         438.30 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         65 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1822.94 |                           0.00 |                          141.56 |                           0.00 |                          250.61 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         64 | randwrite         | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2241.12 |                           0.00 |                          152.04 |                           0.00 |                          250.61 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         63 | randwrite         | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2578.38 |                           0.00 |                          152.04 |                           0.00 |                          263.19 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2552.31 |                           0.00 |                          173.02 |                           0.00 |                          341.84 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         64 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   3076.56 |                           0.00 |                          168.82 |                           0.00 |                          291.50 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         72 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3313.16 |                      0.00 |                          50.59 |                            0.00 |                         175.11 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         71 | randread          | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                  4361.20 |                      0.00 |                          49.02 |                            0.00 |                         206.57 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         72 | randread          | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                  4002.56 |                      0.00 |                          65.27 |                            0.00 |                         396.36 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         72 | randread          | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                  4200.43 |                      0.00 |                          79.17 |                            0.00 |                         413.14 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         70 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  5286.49 |                      0.00 |                          78.12 |                            0.00 |                         438.30 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         65 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1822.94 |                           0.00 |                          141.56 |                           0.00 |                          250.61 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         64 | randwrite         | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2241.12 |                           0.00 |                          152.04 |                           0.00 |                          250.61 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         63 | randwrite         | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2578.38 |                           0.00 |                          152.04 |                           0.00 |                          263.19 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2552.31 |                           0.00 |                          173.02 |                           0.00 |                          341.84 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         64 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3076.56 |                           0.00 |                          168.82 |                           0.00 |                          291.50 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        67.31 |      2.51 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        75.69 |      4.20 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        75.00 |      3.93 |           0.03 |                  2.17 |
| Hardware-1-1-4-1  |        64.23 |      1.85 |           0.02 |                  0.02 |
| Hardware-1-1-5-1  |        72.15 |      2.09 |           0.03 |                  4.03 |
| Hardware-1-1-6-1  |        66.85 |      3.03 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        62.88 |      2.02 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        73.73 |      2.75 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        69.06 |      2.72 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        68.84 |      1.95 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.54 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.52 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.52 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.53 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.47 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.44 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.53 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.51 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

`-rnn` pins the SUT pod to a specific node; without it, the scheduler may place different commands
on different nodes, so results are only directly comparable across commands if `-rnn` is set
consistently.

---

### 3. Numjobs sweep at fixed queue depth (elbow check)

Fixes `-xfid 64` (the elbow found above) and sweeps `-nbt` (numjobs per pod) instead of depth: if
IOPS keep climbing with more threads at the same depth, 64 was a per-queue submission limit, not
a real device ceiling; if IOPS stay flat, 64 is the actual hardware limit.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 4k \
  -xfid 64 \
  -xfe libaio \
  -nbp 1 \
  -nbt 1,2,4,8,16 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 80Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_numjobs_sweep.log
```

### Result

docs_hardware_fio_numjobs_sweep.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1662s 
* Code: 1783190728
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [64].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [0].
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 80Gi. Persistent storage is removed at experiment start.
  * Benchmarking is tested with [1, 2, 4, 8, 16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823734
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:815983
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826418
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821858
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:828969
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821433
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818500
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:827363
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818057
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821903
  * volume_size:80.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783190728

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783190728-748c5bf8b6-6grqm: 0

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

### Execution

#### Per Connection

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4338.31 |                      0.00 |                          54.26 |                            0.00 |                         152.04 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         79 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                  4703.97 |                      0.00 |                          89.65 |                            0.00 |                         497.03 |                            0.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         94 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                  5166.99 |                      0.00 |                         113.77 |                            0.00 |                         952.11 |                            0.00 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |        122 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                  5773.17 |                      0.00 |                         196.08 |                            0.00 |                        1803.55 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |        187 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                  5295.18 |                      0.00 |                        1333.79 |                            0.00 |                        4731.17 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1878.38 |                           0.00 |                          141.56 |                           0.00 |                          256.90 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      2 |                     0.00 |                   3213.22 |                           0.00 |                          168.82 |                           0.00 |                          265.29 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      4 |                     0.00 |                   3792.92 |                           0.00 |                          214.96 |                           0.00 |                          750.78 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      8 |                     0.00 |                   4919.47 |                           0.00 |                          320.86 |                           0.00 |                         1484.78 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     16 |                     0.00 |                   6830.33 |                           0.00 |                          488.64 |                           0.00 |                         2768.24 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4338.31 |                      0.00 |                          54.26 |                            0.00 |                         152.04 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         79 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4703.97 |                      0.00 |                          89.65 |                            0.00 |                         497.03 |                            0.00 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         94 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5166.99 |                      0.00 |                         113.77 |                            0.00 |                         952.11 |                            0.00 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |        122 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5773.17 |                      0.00 |                         196.08 |                            0.00 |                        1803.55 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |        187 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5295.18 |                      0.00 |                        1333.79 |                            0.00 |                        4731.17 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1878.38 |                           0.00 |                          141.56 |                           0.00 |                          256.90 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3213.22 |                           0.00 |                          168.82 |                           0.00 |                          265.29 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   3792.92 |                           0.00 |                          214.96 |                           0.00 |                          750.78 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   4919.47 |                           0.00 |                          320.86 |                           0.00 |                         1484.78 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         64 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   6830.33 |                           0.00 |                          488.64 |                           0.00 |                         2768.24 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        70.17 |      2.29 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        70.96 |      1.99 |           0.03 |                  4.03 |
| Hardware-1-1-3-1  |        81.90 |      3.40 |           0.03 |                  4.03 |
| Hardware-1-1-4-1  |        91.72 |      1.83 |           0.03 |                  4.03 |
| Hardware-1-1-5-1  |       108.61 |      1.85 |           0.03 |                  4.03 |
| Hardware-1-1-6-1  |        68.42 |      2.56 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        73.46 |      2.33 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        71.69 |      4.00 |           0.03 |                  0.03 |
| Hardware-1-1-9-1  |        72.63 |      1.74 |           0.03 |                  0.03 |
| Hardware-1-1-10-1 |        61.99 |      1.61 |           0.03 |                  0.04 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.54 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.57 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.54 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.57 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.58 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.44 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.58 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.55 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.55 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.50 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per `-nbt` (numjobs) value, at the fixed queue depth set by
`-xfid`.

---

### 4. Block-size sweep at fixed queue depth (throughput curve)

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

### Result

docs_hardware_fio_blocksize_sweep.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1977s 
* Code: 1783192417
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
  * disk:824488
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821009
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825466
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821784
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819972
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820658
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821968
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816479
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818635
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820585
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821033
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820735
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825529
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821483
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783192417

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783192417-57659bf49b-grq8b: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4295.42 |                      0.00 |                          49.02 |                            0.00 |                         270.53 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         70 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  5709.68 |                      0.00 |                          37.49 |                            0.00 |                          94.90 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         72 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4000.58 |                      0.00 |                          46.40 |                            0.00 |                         259.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         71 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  8313.69 |                      0.00 |                          30.28 |                            0.00 |                         113.77 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         69 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  8716.04 |                      0.00 |                          25.82 |                            0.00 |                         130.55 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         69 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  3598.18 |                      0.00 |                          50.07 |                            0.00 |                         488.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         73 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2303.26 |                      0.00 |                          54.26 |                            0.00 |                         859.83 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2060.27 |                           0.00 |                          127.40 |                           0.00 |                          229.64 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2036.00 |                           0.00 |                          126.35 |                           0.00 |                          233.83 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2054.96 |                           0.00 |                          114.82 |                           0.00 |                          214.96 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1725.67 |                           0.00 |                          104.33 |                           0.00 |                          166.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1629.86 |                           0.00 |                          111.67 |                           0.00 |                          187.70 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1406.65 |                           0.00 |                          127.40 |                           0.00 |                          191.89 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         63 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    715.00 |                           0.00 |                          240.12 |                           0.00 |                          851.44 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         71 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4295.42 |                      0.00 |                          49.02 |                            0.00 |                         270.53 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         70 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5709.68 |                      0.00 |                          37.49 |                            0.00 |                          94.90 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         72 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  4000.58 |                      0.00 |                          46.40 |                            0.00 |                         259.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         71 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  8313.69 |                      0.00 |                          30.28 |                            0.00 |                         113.77 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         69 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  8716.04 |                      0.00 |                          25.82 |                            0.00 |                         130.55 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         69 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  3598.18 |                      0.00 |                          50.07 |                            0.00 |                         488.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         73 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                  2303.26 |                      0.00 |                          54.26 |                            0.00 |                         859.83 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2060.27 |                           0.00 |                          127.40 |                           0.00 |                          229.64 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2036.00 |                           0.00 |                          126.35 |                           0.00 |                          233.83 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         63 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2054.96 |                           0.00 |                          114.82 |                           0.00 |                          214.96 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         64 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1725.67 |                           0.00 |                          104.33 |                           0.00 |                          166.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1629.86 |                           0.00 |                          111.67 |                           0.00 |                          187.70 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         63 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1406.65 |                           0.00 |                          127.40 |                           0.00 |                          191.89 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         63 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    715.00 |                           0.00 |                          240.12 |                           0.00 |                          851.44 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        74.48 |      1.69 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        75.06 |      3.01 |           0.02 |                  0.02 |
| Hardware-1-1-3-1  |        69.96 |      2.06 |           0.03 |                  4.03 |
| Hardware-1-1-4-1  |        72.50 |      2.23 |           0.03 |                  0.03 |
| Hardware-1-1-5-1  |        77.29 |      1.78 |           0.03 |                  0.03 |
| Hardware-1-1-6-1  |        71.45 |      2.08 |           0.04 |                  0.04 |
| Hardware-1-1-7-1  |        76.74 |      2.35 |           0.09 |                  0.09 |
| Hardware-1-1-8-1  |        61.76 |      2.02 |           0.02 |                  0.02 |
| Hardware-1-1-9-1  |        71.84 |      2.23 |           0.03 |                  0.03 |
| Hardware-1-1-10-1 |        71.85 |      1.66 |           0.02 |                  0.02 |
| Hardware-1-1-11-1 |        62.57 |      1.72 |           0.03 |                  0.03 |
| Hardware-1-1-12-1 |        69.23 |      2.20 |           0.03 |                  0.03 |
| Hardware-1-1-13-1 |        72.29 |      2.25 |           0.04 |                  0.04 |
| Hardware-1-1-14-1 |        64.87 |      1.70 |           0.09 |                  0.09 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.55 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.44 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.49 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.54 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.46 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.45 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.50 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.47 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.45 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.53 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.53 |      0.03 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per block size, at the fixed queue depth set by `-xfid`.

---

### 5. Depth sweep at PostgreSQL's page size (8k)

The sweeps above use `bs=4k` as a generic device-IOPS probe. PostgreSQL always issues 8kB pages
(`BLCKSZ`), so this re-anchors the depth sweep at the actual unit of I/O Postgres uses — the
number that calibrates `effective_io_concurrency` / `maintenance_io_concurrency`, PostgreSQL's
own prefetch-depth knobs.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randread,randwrite \
  -xfbs 8k \
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
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_8k.log
```

### Result

docs_hardware_fio_depth_sweep_8k.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2212s 
* Code: 1783195883
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [1, 2, 4, 8, 16, 32, 64, 128].
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
  * disk:822044
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825002
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816640
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-12-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823446
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824851
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-14-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826533
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825407
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820455
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823479
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829372
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826037
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:829244
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825635
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-7-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823397
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819244
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883
* Hardware-1-1-9-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821267
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783195883

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783195883-97d957696-qdj82: 0

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

| DBMS                | phase           | job               |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:--------------------|:----------------|:------------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1  | Hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         70 | randread          | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                    61.98 |                      0.00 |                          36.44 |                            0.00 |                          90.70 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2  | Hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         69 | randread          | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                   167.54 |                      0.00 |                          32.11 |                            0.00 |                          76.02 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3  | Hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         70 | randread          | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                   403.22 |                      0.00 |                          26.35 |                            0.00 |                          66.32 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4  | Hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         72 | randread          | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                   546.25 |                      0.00 |                          35.39 |                            0.00 |                         117.96 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5  | Hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         70 | randread          | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                  1337.27 |                      0.00 |                          42.21 |                            0.00 |                         107.48 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1  | Hardware-1-1-6  | Hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         70 | randread          | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                  2537.31 |                      0.00 |                          31.33 |                            0.00 |                          91.75 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7-1-1  | Hardware-1-1-7  | Hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         71 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4781.67 |                      0.00 |                          43.25 |                            0.00 |                         127.40 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8-1-1  | Hardware-1-1-8  | Hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         71 | randread          | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4743.46 |                      0.00 |                          66.85 |                            0.00 |                         734.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9-1-1  | Hardware-1-1-9  | Hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         63 | randwrite         | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    100.86 |                           0.00 |                           38.01 |                           0.00 |                           71.83 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10-1-1 | Hardware-1-1-10 | Hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         63 | randwrite         | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    172.16 |                           0.00 |                           43.78 |                           0.00 |                           83.36 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11-1-1 | Hardware-1-1-11 | Hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         63 | randwrite         | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    279.84 |                           0.00 |                           50.59 |                           0.00 |                          112.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12-1-1 | Hardware-1-1-12 | Hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    490.15 |                           0.00 |                           55.84 |                           0.00 |                          149.95 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13-1-1 | Hardware-1-1-13 | Hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         65 | randwrite         | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    696.68 |                           0.00 |                           70.78 |                           0.00 |                          193.99 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14-1-1 | Hardware-1-1-14 | Hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         63 | randwrite         | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1175.87 |                           0.00 |                           88.60 |                           0.00 |                          223.35 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-15-1-1 | Hardware-1-1-15 | Hardware-1-1-15-1 |                1 |       15 |               1 |       1 |         64 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   1859.32 |                           0.00 |                          122.16 |                           0.00 |                          246.42 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-16-1-1 | Hardware-1-1-16 | Hardware-1-1-16-1 |                1 |       16 |               1 |       1 |         64 | randwrite         | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                   2449.04 |                           0.00 |                          162.53 |                           0.00 |                          434.11 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 |         70 | randread          | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    61.98 |                      0.00 |                          36.44 |                            0.00 |                          90.70 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 |         69 | randread          | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   167.54 |                      0.00 |                          32.11 |                            0.00 |                          76.02 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 |         70 | randread          | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   403.22 |                      0.00 |                          26.35 |                            0.00 |                          66.32 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 |         72 | randread          | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                   546.25 |                      0.00 |                          35.39 |                            0.00 |                         117.96 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 |         70 | randread          | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  1337.27 |                      0.00 |                          42.21 |                            0.00 |                         107.48 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 |         70 | randread          | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  2537.31 |                      0.00 |                          31.33 |                            0.00 |                          91.75 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 |         71 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4781.67 |                      0.00 |                          43.25 |                            0.00 |                         127.40 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 |         71 | randread          | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  4743.46 |                      0.00 |                          66.85 |                            0.00 |                         734.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 |         63 | randwrite         | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    100.86 |                           0.00 |                           38.01 |                           0.00 |                           71.83 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 |         63 | randwrite         | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    172.16 |                           0.00 |                           43.78 |                           0.00 |                           83.36 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 |         63 | randwrite         | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    279.84 |                           0.00 |                           50.59 |                           0.00 |                          112.72 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    490.15 |                           0.00 |                           55.84 |                           0.00 |                          149.95 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 |         65 | randwrite         | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    696.68 |                           0.00 |                           70.78 |                           0.00 |                          193.99 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 |         63 | randwrite         | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1175.87 |                           0.00 |                           88.60 |                           0.00 |                          223.35 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 |         64 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1859.32 |                           0.00 |                          122.16 |                           0.00 |                          246.42 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 |         64 | randwrite         | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2449.04 |                           0.00 |                          162.53 |                           0.00 |                          434.11 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |        73.15 |      2.30 |           0.02 |                  0.02 |
| Hardware-1-1-2-1  |        65.66 |      2.04 |           0.03 |                  4.03 |
| Hardware-1-1-3-1  |        73.03 |      2.69 |           0.02 |                  0.02 |
| Hardware-1-1-4-1  |        65.29 |      1.79 |           0.02 |                  0.02 |
| Hardware-1-1-5-1  |        71.24 |      1.98 |           0.02 |                  0.02 |
| Hardware-1-1-6-1  |        65.16 |      2.14 |           0.02 |                  0.02 |
| Hardware-1-1-7-1  |        72.52 |      4.75 |           0.02 |                  0.02 |
| Hardware-1-1-8-1  |        75.68 |      2.36 |           0.03 |                  2.44 |
| Hardware-1-1-9-1  |        65.55 |      2.49 |           0.02 |                  0.02 |
| Hardware-1-1-10-1 |        68.96 |      2.28 |           0.08 |                  0.08 |
| Hardware-1-1-11-1 |        66.96 |      1.66 |           0.02 |                  0.02 |
| Hardware-1-1-12-1 |        58.58 |      1.69 |           0.02 |                  0.02 |
| Hardware-1-1-13-1 |        65.96 |      1.79 |           0.02 |                  0.02 |
| Hardware-1-1-14-1 |        64.07 |      2.03 |           0.03 |                  0.03 |
| Hardware-1-1-15-1 |        67.91 |      1.47 |           0.02 |                  0.02 |
| Hardware-1-1-16-1 |        64.59 |      1.68 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1  |         0.49 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1  |         0.50 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1  |         0.52 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-4-1  |         0.54 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-5-1  |         0.52 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-6-1  |         0.48 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-7-1  |         0.55 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-8-1  |         0.43 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-9-1  |         0.58 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-10-1 |         0.51 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-11-1 |         0.54 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-12-1 |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-13-1 |         0.50 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-14-1 |         0.52 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-15-1 |         0.50 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-16-1 |         0.57 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per queue depth, at the 8k block size set by `-xfbs`.

---

### 6. `random_page_cost` calibration

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

### Result

docs_hardware_fio_random_page_cost.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 316s 
* Code: 1783198124
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['read', 'randread'].
  * Block size(s) swept: ['8k'].
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
  * disk:822444
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198124
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825522
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198124

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783198124-5d959fb658-s85rs: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         71 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4745.50 |                      0.00 |                          26.08 |                            0.00 |                          86.51 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         71 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                      1 |                  4090.29 |                      0.00 |                          45.88 |                            0.00 |                         229.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         71 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4745.50 |                      0.00 |                          26.08 |                            0.00 |                          86.51 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         71 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4090.29 |                      0.00 |                          45.88 |                            0.00 |                         229.64 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        70.73 |      1.84 |           0.02 |                  0.02 |
| Hardware-1-1-2-1 |        70.86 |      5.29 |           0.03 |                  4.03 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.44 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.49 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table has one row for `read` (sequential) and one for `randread`, both at the same
block size and queue depth.

---

### 7. WAL sync-write latency (fsync)

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

### Result

docs_hardware_fio_wal_sync_fsync.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 214s 
* Code: 1783198464
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
  * disk:820118
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198464

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783198464-779ccffd68-ldt2x: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     48.92 |                           0.00 |                           29.75 |                           0.00 |                          467.66 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     48.92 |                           0.00 |                           29.75 |                           0.00 |                          467.66 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        66.46 |      1.71 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.44 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

`hardware_fio_write_iops` and the write latency percentiles in the Per Phase table are the
relevant columns for this single-row result.

---

### 8. WAL sync-write latency (fdatasync)

Same as above but `fdatasync` instead of `fsync`. fdatasync skips the inode-metadata sync fsync
does, and is PostgreSQL's Linux default (`wal_sync_method=fdatasync`) — compare its latency
against the fsync run above to confirm it is actually cheaper on this storage.

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
  -xffd 1 \
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
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fdatasync.log
```

### Result

docs_hardware_fio_wal_sync_fdatasync.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 182s 
* Code: 1783198702
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [1].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
  * Fdatasync interval(s) swept: [1].
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
  * disk:825046
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198702

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783198702-85dd59cf54-f67jc: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    0 |                        1 |                       50 |                      1 |                     0.00 |                    177.61 |                           0.00 |                           25.03 |                           0.00 |                           58.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    0 |                        1 |                       50 |                     0.00 |                    177.61 |                           0.00 |                           25.03 |                           0.00 |                           58.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        64.00 |      2.58 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.50 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

`hardware_fio_write_iops` and the write latency percentiles are the relevant columns to compare
against command 7's `fsync` result.

---

### 9. WAL group-commit scaling

Same sync-write profile, sweeping concurrent committing backends (`-nbt`) instead of a single
one. If aggregate fsyncs/sec keeps climbing with more concurrent writers, the storage/controller
coalesces concurrent commits well; if it flattens immediately, tune `commit_delay` /
`commit_siblings` in Postgres to force batching in software instead.

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
  -nbt 1,2,4,8,16,32 \
  -ne 1 \
  -m \
  -ms $BEXHOMA_MS \
  -tr \
  -rsr \
  -rss 150Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_group_commit.log
```

### Result

docs_hardware_fio_wal_group_commit.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 856s 
* Code: 1783198907
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
  * SUT is fixed to cl-worker36.
  * Database is persisted to disk of type shared and size 150Gi. Persistent storage is removed at experiment start.
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
  * disk:826576
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824462
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824318
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818035
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823012
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824871
  * volume_size:150.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783198907

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783198907-565b848d8d-p7zpw: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     64.94 |                           0.00 |                           17.43 |                           0.00 |                          429.92 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      2 |                     0.00 |                    181.98 |                           0.00 |                           57.93 |                           0.00 |                          100.14 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      4 |                     0.00 |                    476.06 |                           0.00 |                           50.07 |                           0.00 |                           74.97 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      8 |                     0.00 |                    852.53 |                           0.00 |                           50.59 |                           0.00 |                          104.33 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     16 |                     0.00 |                   1396.17 |                           0.00 |                           50.07 |                           0.00 |                           91.75 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1 | Hardware-1-1-6 | Hardware-1-1-6-1 |                1 |        6 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     32 |                     0.00 |                   2593.54 |                           0.00 |                           58.46 |                           0.00 |                          115.87 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     64.94 |                           0.00 |                           17.43 |                           0.00 |                          429.92 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    181.98 |                           0.00 |                           57.93 |                           0.00 |                          100.14 |                  2 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    476.06 |                           0.00 |                           50.07 |                           0.00 |                           74.97 |                  4 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    852.53 |                           0.00 |                           50.59 |                           0.00 |                          104.33 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                   1396.17 |                           0.00 |                           50.07 |                           0.00 |                           91.75 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                   2593.54 |                           0.00 |                           58.46 |                           0.00 |                          115.87 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        64.08 |      2.65 |           0.02 |                  0.02 |
| Hardware-1-1-2-1 |        63.25 |      1.56 |           0.02 |                  0.02 |
| Hardware-1-1-3-1 |        60.88 |      1.96 |           0.02 |                  0.02 |
| Hardware-1-1-4-1 |        69.21 |      1.75 |           0.02 |                  0.02 |
| Hardware-1-1-5-1 |        69.16 |      2.91 |           0.03 |                  0.03 |
| Hardware-1-1-6-1 |        71.18 |      3.49 |           0.04 |                  0.04 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.56 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.57 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.49 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.57 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.62 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-6-1 |         0.52 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per concurrent-writer count set by `-nbt`.

---

### 10. WAL record-size sweep

Same sync-write profile, sweeping the WAL record size instead of backend count. Bigger
transactions (or post-checkpoint `full_page_writes` bursts) write more before fsync — this shows
how sync-write latency grows with record size.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 1k,8k,16k,32k,64k \
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
  run &>$LOG_DIR/docs_hardware_fio_wal_record_size.log
```

### Result

docs_hardware_fio_wal_record_size.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 723s 
* Code: 1783199789
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['write'].
  * Block size(s) swept: ['1k', '8k', '16k', '32k', '64k'].
  * Queue depth(s) swept: [1].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [1].
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
  * disk:823240
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783199789
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:831169
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783199789
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824028
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783199789
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:827995
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783199789
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:819882
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783199789

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783199789-d99d9b8c8-dmq44: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 | write             | 1k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     84.38 |                           0.00 |                           52.17 |                           0.00 |                           79.17 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                    145.23 |                           0.00 |                           33.42 |                           0.00 |                           63.70 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 | write             | 16k               |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     94.12 |                           0.00 |                           33.42 |                           0.00 |                           63.18 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         63 | write             | 32k               |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                    127.30 |                           0.00 |                           35.39 |                           0.00 |                           74.97 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         62 | write             | 64k               |                      1 | libaio                |                    1 |                        0 |                       50 |                      1 |                     0.00 |                     53.67 |                           0.00 |                           65.80 |                           0.00 |                           88.60 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 | write             | 1k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     84.38 |                           0.00 |                           52.17 |                           0.00 |                           79.17 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         63 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    145.23 |                           0.00 |                           33.42 |                           0.00 |                           63.70 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 | write             | 16k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     94.12 |                           0.00 |                           33.42 |                           0.00 |                           63.18 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         63 | write             | 32k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    127.30 |                           0.00 |                           35.39 |                           0.00 |                           74.97 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         62 | write             | 64k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     53.67 |                           0.00 |                           65.80 |                           0.00 |                           88.60 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        69.84 |      2.70 |           0.02 |                  0.02 |
| Hardware-1-1-2-1 |        63.40 |      1.72 |           0.02 |                  0.02 |
| Hardware-1-1-3-1 |        62.02 |      1.64 |           0.02 |                  0.02 |
| Hardware-1-1-4-1 |        69.61 |      1.90 |           0.02 |                  0.02 |
| Hardware-1-1-5-1 |        61.78 |      1.75 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.45 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.55 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.52 |      0.04 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.52 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per block size set by `-xfbs`, at fixed queue depth 1.

---

### 11. Checkpoint writeback bandwidth

Large-block sequential writes without a per-write fsync, approximating how fast
checkpointer/bgwriter can flush dirty pages during a checkpoint.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw write \
  -xfbs 1M,4M,16M \
  -xfid 4,16 \
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
  run &>$LOG_DIR/docs_hardware_fio_checkpoint_writeback.log
```

### Result

docs_hardware_fio_checkpoint_writeback.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 864s 
* Code: 1783200536
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
  * disk:831367
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820536
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:827659
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821051
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:825418
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536
* Hardware-1-1-6-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821889
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783200536

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783200536-f46bc844-kqq79: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     76.80 |                           0.00 |                          104.33 |                           0.00 |                          164.63 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         63 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    237.50 |                           0.00 |                          143.65 |                           0.00 |                          212.86 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                     49.68 |                           0.00 |                          139.46 |                           0.00 |                          206.57 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         63 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                    142.58 |                           0.00 |                          235.93 |                           0.00 |                          362.81 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         63 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                      3.11 |                           0.00 |                         1182.79 |                           0.00 |                         1283.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6-1-1 | Hardware-1-1-6 | Hardware-1-1-6-1 |                1 |        6 |               1 |       1 |         63 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                      1 |                     0.00 |                      3.08 |                           0.00 |                         5536.48 |                           0.00 |                         5737.81 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     76.80 |                           0.00 |                          104.33 |                           0.00 |                          164.63 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         63 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    237.50 |                           0.00 |                          143.65 |                           0.00 |                          212.86 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     49.68 |                           0.00 |                          139.46 |                           0.00 |                          206.57 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         63 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    142.58 |                           0.00 |                          235.93 |                           0.00 |                          362.81 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         63 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      3.11 |                           0.00 |                         1182.79 |                           0.00 |                         1283.46 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 |         63 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      3.08 |                           0.00 |                         5536.48 |                           0.00 |                         5737.81 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        62.71 |      2.49 |           0.03 |                  0.03 |
| Hardware-1-1-2-1 |        67.90 |      1.91 |           0.04 |                  0.04 |
| Hardware-1-1-3-1 |        59.10 |      1.61 |           0.04 |                  0.04 |
| Hardware-1-1-4-1 |        72.89 |      2.15 |           0.09 |                  0.09 |
| Hardware-1-1-5-1 |        64.14 |      1.67 |           0.09 |                  0.09 |
| Hardware-1-1-6-1 |        62.89 |      2.54 |           0.27 |                  0.27 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.57 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.57 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.57 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.44 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-5-1 |         0.56 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-6-1 |         0.53 |      0.02 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

The Per Phase table lists one row per block size/queue depth combination; bandwidth can be
derived from `hardware_fio_write_iops × hardware_fio_bs`.

---

### 12. OLTP/WAL contention proxy

A single-profile approximation of foreground OLTP traffic contending with WAL flushes on one
queue: mixed random read/write with fsync on the write side. This is **not** the same as true
concurrent checkpoint+WAL+OLTP contention — that needs several parallel benchmarker jobs with
different fio profiles running in the same round, which bexhoma does not yet support for Hardware
(the closest existing precedent is the TPC-H refresh-stream mechanism, see
`bexhoma/experiments/CLAUDE.md` §8, which could be adapted for this in the future). This proxy is
what is achievable today with the single-profile-per-round model used throughout this page.

```bash
bexhoma hardware \
  -dbms Hardware \
  -xht fio \
  -xts 4G \
  -xtd 60 \
  -xfrw randrw \
  -xfmx 70 \
  -xfbs 8k \
  -xfid 64 \
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
  run &>$LOG_DIR/docs_hardware_fio_oltp_wal_contention_proxy.log
```

### Result

docs_hardware_fio_oltp_wal_contention_proxy.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 183s 
* Code: 1783201425
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randrw'].
  * Block size(s) swept: ['8k'].
  * Queue depth(s) swept: [64].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [1].
  * Fdatasync interval(s) swept: [0].
  * Read mix percentage(s) swept: [70].
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
  * disk:831834
  * volume_size:50.0G
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783201425

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783201425-655946dbcb-qxgkb: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         72 | randrw            | 8k                |                     64 | libaio                |                    1 |                        0 |                       70 |                      1 |                  1955.51 |                    835.77 |                          49.02 |                          100.14 |                         170.92 |                          316.67 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         72 | randrw            | 8k                |                     64 | libaio                |                    1 |                        0 |                       70 |                  1955.51 |                    835.77 |                          49.02 |                          100.14 |                         170.92 |                          316.67 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        70.17 |      1.80 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.50 |      0.00 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero read or write IOPS
```

`hardware_fio_read_iops` and `hardware_fio_write_iops` in the single result row can be compared
against the isolated `randread` result from command 5 at the same depth and block size.

### Which PostgreSQL parameter each command informs

| Command(s) | Informs |
|---|---|
| 1, 2 (depth sweep + refinement) | `effective_io_concurrency`, `maintenance_io_concurrency` |
| 3 (numjobs) | `max_parallel_workers_per_gather` and friends |
| 4 (block size) | Reasoning about checkpoint/bgwriter I/O coalescing |
| 5, 6 (8k depth sweep, page cost) | `effective_io_concurrency` at the real page size; `random_page_cost` |
| 7, 8 (WAL sync fsync/fdatasync) | `wal_sync_method`, expected max commit rate |
| 9 (group commit) | `commit_delay`, `commit_siblings` |
| 10 (WAL record size) | Expectations around `full_page_writes` bursts and large transactions |
| 11 (checkpoint bandwidth) | `checkpoint_completion_target`, `max_wal_size` |
| 12 (OLTP/WAL proxy) | Sanity check under mixed load |

## Sysbench CPU noisy-neighbor benchmarks

Unlike the fio sweeps above, these four commands (`-xht sysbench`) are not about
characterizing storage — they use no disk I/O at all, so none of them need `-rst`/`-rss`/`-rsr`.
The question they investigate is whether a Kubernetes CPU limit (`-lc`) on the SUT container
actually **isolates** co-located workloads from each other, the way it's supposed to. Command 13
calibrates the per-pod saturation point; 14 and 15 are cheap sanity checks against a single SUT
(no second SUT pod needed); 16 is the actual cross-tenant test.

Each command sets `-xtd 60`, capping both of `run_sysbench.sh`'s phases (CPU, then memory) at 60
seconds instead of sysbench's own short built-in default — without it, a round can finish before
`-m`/`-mc`'s Prometheus scrape interval ever samples it, showing no monitoring data at all. Total
round length ends up roughly 1-2 minutes (up to 2x60s, since the memory phase can finish earlier
once its 10G transfers, plus SSH/pod overhead). The result DataFrame's `duration` column reports
the actual measured wall-clock length (`BEXHOMA_DURATION`) for every hardware benchmark — fio or
sysbench — so a suspiciously short round is visible directly in the table rather than only in the
raw log.

References:
1. sysbench: https://github.com/akopytov/sysbench
1. Kubernetes CPU limits and CFS quota: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### 13. CPU-quota calibration (thread sweep)

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

### Result

docs_hardware_sysbench_cpu_quota_calibration.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 569s 
* Code: 1783201632
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [1, 2, 4, 8], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 2, 4, 8] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824317
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783201632
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820813
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783201632
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:826667
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783201632
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:821568
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783201632

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783201632-5cbcd87c5f-5rsxq: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                1216.19 |                                60.00 |                               0.84 |                             6960860.82 |                                     6797.72 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2425.42 |                                60.00 |                               0.86 |                             6356430.17 |                                     6207.45 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2417.14 |                                60.01 |                               0.92 |                             1147806.39 |                                     1120.90 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                2413.27 |                                60.05 |                               1.01 |                             1072236.03 |                                     1047.11 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                1216.19 |                                60.00 |                               0.84 |                             6960860.82 |                                     6797.72 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2425.42 |                                60.00 |                               0.86 |                             6356430.17 |                                     6207.45 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2417.14 |                                60.01 |                               0.92 |                             1147806.39 |                                     1120.90 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                2413.27 |                                60.05 |                               1.01 |                             1072236.03 |                                     1047.11 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        49.76 |      1.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |       107.62 |      2.00 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |       103.64 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-4-1 |       133.97 |      2.00 |           0.01 |                  0.01 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.25 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.30 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         0.31 |      0.02 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         0.25 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

### 14. Harness-overhead sweep (`-nbp`)

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

### Result

docs_hardware_sysbench_nbp_overhead_sweep.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 450s 
* Code: 1783202226
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823668
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202226
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:820400
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202226
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822066
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202226

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783202226-57d4db9fff-2q594: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2421.27 |                                60.00 |                               0.92 |                             2159458.19 |                                     2108.85 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1241.33 |                                60.00 |                               0.83 |                             1651070.04 |                                     1612.37 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1208.00 |                                60.03 |                               0.94 |                             3275980.07 |                                     3199.20 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 609.85 |                                60.00 |                               0.89 |                             3762704.60 |                                     3674.52 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 612.99 |                                60.03 |                               0.87 |                             3809677.72 |                                     3720.39 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 611.84 |                                60.00 |                               0.87 |                             3933162.03 |                                     3840.98 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                 607.30 |                                60.00 |                               0.89 |                             3686524.48 |                                     3600.12 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2421.27 |                                60.00 |                               0.92 |                             2159458.19 |                                     2108.85 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2449.33 |                                60.03 |                               0.94 |                             4927050.11 |                                     4811.57 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2441.98 |                                60.03 |                               0.89 |                            15192068.83 |                                    14836.01 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       108.60 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-2-1 |       115.81 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-3-1 |        81.57 |      2.00 |           0.02 |                  0.02 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.29 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.54 |      0.01 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         1.04 |      0.04 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

### 15. Shared-SUT saturation sweep (`-ne`)

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

### Result

docs_hardware_sysbench_ne_saturation_sweep.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 680s 
* Code: 1783202702
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4, 8] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818212
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202702
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:824999
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202702
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:822155
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202702
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:823755
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783202702

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783202702-6d86f5ffdc-lk5nh: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2433.62 |                                60.00 |                               0.83 |                             6003493.54 |                                     5862.79 |                                  0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1217.40 |                                60.01 |                               0.89 |                             2805994.05 |                                     2740.23 |                                  0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                1225.65 |                                60.00 |                               0.89 |                             2235382.54 |                                     2182.99 |                                  0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 610.10 |                                60.00 |                               1.01 |                             1435383.79 |                                     1401.74 |                                  0.00 |        0 |
| Hardware-1-1-3-1-2 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 611.81 |                                60.07 |                               0.97 |                              887274.92 |                                      866.48 |                                  0.00 |        0 |
| Hardware-1-1-3-1-3 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 606.78 |                                60.00 |                               1.01 |                              917705.26 |                                      896.20 |                                  0.00 |        0 |
| Hardware-1-1-3-1-4 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 608.08 |                                60.07 |                               0.99 |                             1112504.59 |                                     1086.43 |                                  0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         79 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 304.27 |                                60.00 |                              87.56 |                              844755.00 |                                      824.96 |                                  0.00 |        0 |
| Hardware-1-1-4-1-2 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         83 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 298.18 |                                60.00 |                              89.16 |                              612420.38 |                                      598.07 |                                  0.00 |        0 |
| Hardware-1-1-4-1-3 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         78 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 304.57 |                                60.04 |                              89.16 |                              838966.61 |                                      819.30 |                                  0.00 |        0 |
| Hardware-1-1-4-1-4 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         80 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 312.14 |                                60.00 |                              84.47 |                              675932.43 |                                      660.09 |                                  0.00 |        0 |
| Hardware-1-1-4-1-5 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         82 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 302.99 |                                60.00 |                              87.56 |                              578640.28 |                                      565.08 |                                  0.00 |        0 |
| Hardware-1-1-4-1-6 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         82 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 301.18 |                                60.00 |                              87.56 |                              596260.25 |                                      582.29 |                                  0.00 |        0 |
| Hardware-1-1-4-1-7 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         76 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 306.11 |                                60.00 |                              86.00 |                              812929.54 |                                      793.88 |                                  0.00 |        0 |
| Hardware-1-1-4-1-8 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                 315.57 |                                60.06 |                              84.47 |                              881652.36 |                                      860.99 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2433.62 |                                60.00 |                               0.83 |                             6003493.54 |                                     5862.79 |                                  0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  4 |                                2443.05 |                                60.01 |                               0.89 |                             5041376.59 |                                     4923.22 |                                  0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                2436.77 |                                60.07 |                               1.01 |                             4352868.56 |                                     4250.85 |                                  0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         83 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 16 |                                2445.01 |                                60.06 |                              89.16 |                             5841556.85 |                                     5704.66 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       112.81 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-2-1 |       120.76 |      2.00 |           0.01 |                  0.01 |
| Hardware-1-1-3-1 |        93.42 |      2.00 |           0.02 |                  0.02 |
| Hardware-1-1-4-1 |       128.57 |      2.00 |           0.03 |                  0.03 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.26 |      0.00 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |         0.62 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-3-1 |         1.01 |      0.03 |           0.00 |                  0.00 |
| Hardware-1-1-4-1 |         1.99 |      0.10 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

### 16. Co-located noisy-neighbor test (`-mtn`/`-mtb container`)

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

### Result

docs_hardware_sysbench_noisy_neighbor.log
```markdown
﻿## Show Summary

### Workload
Hardware Benchmark (sysbench)
* Type: hardware
* Duration: 315s 
* Code: 1783203408
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Experiment uses bexhoma version 0.10.2.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker19.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:818012
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783203408
* Hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:816638
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783203408
* Hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:812371
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783203408
* Hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:812991
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * eval_parameters
    * code:1783203408

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783203408-76f6fd5d47-ltwzr: 0
* bexhoma-sut-hardware-2-1783203408-56b665cf75-bfphh: 0
* bexhoma-sut-hardware-3-1783203408-544968c7cf-j4lmp: 0
* bexhoma-sut-hardware-4-1783203408-6c947b8479-mph7k: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |        140 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2446.25 |                                60.00 |                               0.83 |                             3554824.71 |                                     3471.51 |                                  0.00 |        0 |
| Hardware-2-1-1-1-1 | Hardware-2-1-1 | Hardware-2-1-1-1 |                1 |        1 |               1 |       1 |        113 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2444.48 |                                60.00 |                               0.83 |                             6493159.81 |                                     6340.98 |                                  0.00 |        0 |
| Hardware-3-1-1-1-1 | Hardware-3-1-1 | Hardware-3-1-1-1 |                1 |        1 |               1 |       1 |         89 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2447.38 |                                60.00 |                               0.83 |                             3700791.83 |                                     3614.05 |                                  0.00 |        0 |
| Hardware-4-1-1-1-1 | Hardware-4-1-1 | Hardware-4-1-1-1 |                1 |        1 |               1 |       1 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2440.37 |                                60.00 |                               0.83 |                             4050259.50 |                                     3955.33 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| Hardware-1-1-1-0 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |        140 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2446.25 |                                60.00 |                               0.83 |                             3554824.71 |                                     3471.51 |                                  0.00 |        0 |
| Hardware-2-1-1-1 | Hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |        113 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2444.48 |                                60.00 |                               0.83 |                             6493159.81 |                                     6340.98 |                                  0.00 |        0 |
| Hardware-3-1-1-2 | Hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |         89 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2447.38 |                                60.00 |                               0.83 |                             3700791.83 |                                     3614.05 |                                  0.00 |        0 |
| Hardware-4-1-1-3 | Hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  2 |                                2440.37 |                                60.00 |                               0.83 |                             4050259.50 |                                     3955.33 |                                  0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        90.27 |      2.00 |           0.00 |                  0.00 |
| Hardware-2-1-1-1 |       102.15 |      2.00 |           0.01 |                  0.01 |
| Hardware-3-1-1-1 |        89.29 |      2.00 |           0.00 |                  0.00 |
| Hardware-4-1-1-1 |        97.22 |      2.00 |           0.00 |                  0.00 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         0.22 |      0.01 |           0.00 |                  0.00 |
| Hardware-2-1-1-1 |         0.26 |      0.01 |           0.00 |                  0.00 |
| Hardware-3-1-1-1 |         0.40 |      0.01 |           0.00 |                  0.00 |
| Hardware-4-1-1-1 |         0.26 |      0.01 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero CPU events/sec
```

## Netperf network benchmarks

The three commands below (`-xht netperf`) measure raw network latency/throughput using
[netperf](https://github.com/HewlettPackard/netperf) against a single `netserver` instance running
on the SUT (`netserver` forks a child per incoming test session natively, so — unlike sockperf
below — one instance already serves many concurrent clients with no per-pod server pool needed).
Netperf exists here alongside sockperf because sockperf's client is limited to exactly one
connection per process (confirmed against upstream:
[Mellanox/sockperf#133](https://github.com/Mellanox/sockperf/issues/133), where the maintainer
states plainly "sockperf does not support parallel client send operations"), so sockperf's own
pod-count sweeps below (23) never exceed as many real connections as pods. netperf's `TCP_RR` test
type is described by its own manual as "a user-space to user-space `ping` with no think time" —
synchronous, one transaction at a time, the same shape as PostgreSQL's simple-query protocol — and
that manual documents running many concurrent instances as the supported way to get aggregate
concurrency (["Care and Feeding of Netperf", §7](https://hewlettpackard.github.io/netperf/doc/netperf.html)).
`-nbt` here controls exactly that: how many concurrent `TCP_RR` connections
[`run_netperf.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_netperf.sh)
launches per pod, each pinned to its own fixed data port out of a 64-port pool
(`NETPERF_DATA_NUM_PORTS`, see
[`images/hardware/sut/Dockerfile`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/sut/Dockerfile))
so the k8s Service can forward it — netperf opens a fresh listening socket per test session rather
than one shared listener, so this is a hard, not incidental, ceiling on concurrency. All three
commands use `-xnpp tcp` (selects `TCP_RR`), matching PostgreSQL's actual wire protocol, same
reasoning as sockperf's `-xspp tcp` below.

17 fixes both pod count and connection count at 1, to establish a single-connection baseline. 18
sweeps the number of concurrent connections (1 to 64) within a single pod — a test sockperf cannot
do, since its client is limited to one connection per process. 19 holds total connection count
fixed and instead splits it across 1 vs 2 pods, the same "-nbp sweep at constant total threads"
shape used for pod-count comparisons elsewhere in this repo (e.g.
[`Example-Benchbase.md`](Example-Benchbase.md)).

### 17. Single-connection round-trip latency baseline (TCP_RR)

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

### Result

docs_hardware_netperf_postgresql_query_latency.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 206s 
* Code: 1783677623
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
  * Benchmark tool: netperf.
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
  * disk:872609
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677623

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783677623-64fd958dc8-vhwv8: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                             9642.15 |                              0.10 |                              0.08 |                              0.22 |                              0.34 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                             9642.15 |                              0.10 |                              0.08 |                              0.22 |                              0.34 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         8.65 |      0.19 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.80 |      0.35 |           0.00 |                  0.00 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

`hardware_netperf_transaction_rate` and the `hardware_netperf_latency_*_ms` columns report the
observed transaction rate and round-trip latency for this connection.

### 18. Concurrent-connection scaling (TCP_RR, `-nbt` sweep)

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

### Result

docs_hardware_netperf_postgresql_connection_scaling_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 769s 
* Code: 1783677848
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
  * Benchmark tool: netperf.
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
  * disk:872609
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677848
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:872610
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677848
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:872808
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677848
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:872611
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677848
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:872612
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783677848

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783677848-7b4b58fd7b-ms4fl: 0

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

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         61 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                             9256.39 |                              0.11 |                              0.08 |                              0.23 |                              0.34 |                                0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                            59670.23 |                              0.15 |                              0.10 |                              0.34 |                              0.39 |                                0.00 |        0 |
| Hardware-1-1-3-1-1 | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                            94641.00 |                              0.20 |                              0.13 |                              0.40 |                              0.51 |                                0.00 |        0 |
| Hardware-1-1-4-1-1 | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           159780.62 |                              0.28 |                              0.22 |                              0.48 |                              0.61 |                                0.00 |        0 |
| Hardware-1-1-5-1-1 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         85 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 64 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           280260.84 |                              0.39 |                              0.36 |                              0.70 |                              2.08 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         61 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                             9256.39 |                              0.11 |                              0.08 |                              0.23 |                              0.34 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  8 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                            59670.23 |                              0.15 |                              0.10 |                              0.34 |                              0.38 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 16 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                            94641.00 |                              0.20 |                              0.13 |                              0.40 |                              0.51 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           159780.62 |                              0.28 |                              0.22 |                              0.48 |                              0.61 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 |         85 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 64 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           280260.84 |                              0.39 |                              0.36 |                              0.70 |                              2.08 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         7.31 |      0.20 |           0.21 |                  0.21 |
| Hardware-1-1-2-1 |        74.58 |      1.40 |           0.21 |                  0.21 |
| Hardware-1-1-3-1 |       107.02 |      2.67 |           0.21 |                  0.21 |
| Hardware-1-1-4-1 |       218.43 |      4.88 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       428.66 |      7.28 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         7.85 |      0.35 |           0.00 |                  0.00 |
| Hardware-1-1-2-1 |       105.31 |      2.92 |           0.01 |                  0.01 |
| Hardware-1-1-3-1 |       268.11 |      7.37 |           0.01 |                  0.01 |
| Hardware-1-1-4-1 |       444.19 |     17.40 |           0.01 |                  0.01 |
| Hardware-1-1-5-1 |      1017.52 |     35.53 |           0.03 |                  0.03 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

Compare `hardware_netperf_transaction_rate` and `hardware_netperf_latency_*_ms` across the five
rows of the Per Phase table to see how they change as connection count grows.

### 19. Pod-count scaling at fixed total concurrency (TCP_RR, `-nbp` sweep)

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

### Result

docs_hardware_netperf_postgresql_pod_scaling_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (netperf)
* Type: hardware
* Duration: 407s 
* Code: 1783678637
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
  * Benchmark tool: netperf.
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
  * disk:872612
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783678637
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:872613
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783678637

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783678637-748c558fb6-bhlj8: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         86 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 64 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           273146.51 |                              0.36 |                              0.37 |                              0.69 |                              1.21 |                                0.00 |        0 |
| Hardware-1-1-2-1-1 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           132543.81 |                              0.52 |                              0.41 |                              1.07 |                              2.39 |                                0.00 |        0 |
| Hardware-1-1-2-1-2 | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 32 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                        0 |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           136550.29 |                              0.49 |                              0.40 |                              1.01 |                              2.10 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         86 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 64 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           273146.51 |                              0.36 |                              0.37 |                              0.69 |                              1.21 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                 64 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 |                          |                              |                           0 |                         |                               0.00 |                               0.00 |                               0.00 |                                0.00 |                                 0.00 |                                0.00 | tcp                         |                           269094.10 |                              0.52 |                              0.41 |                              1.07 |                              2.39 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |       411.81 |      6.84 |           0.22 |                  0.22 |
| Hardware-1-1-2-1 |       403.49 |      6.90 |           0.22 |                  0.22 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |      1282.83 |     21.06 |           0.03 |                  0.03 |
| Hardware-1-1-2-1 |      1122.67 |     33.99 |           0.01 |                  0.01 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero netperf transaction rate
```

Compare `hardware_netperf_transaction_rate` and `hardware_netperf_latency_*_ms` between the two
rows of the Per Phase table to see how they change when the same total connection count is split
across more pods.

## Sockperf network benchmarks

The four commands below (`-xht sockperf`) measure raw network latency/throughput using
[sockperf](https://github.com/Mellanox/sockperf) against a static pool of 16 TCP+UDP server pairs
running on the SUT (`SOCKPERF_NUM_SERVERS`, see
[`images/hardware/sut/entrypoint.sh`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/sut/entrypoint.sh)).
Unlike fio/sysbench, sockperf traffic does not go over SSH — each benchmarker pod connects
directly to its own dedicated server (picked via `BEXHOMA_CHILD` modulo the server pool, so
several pods never contend on one socket) over the SUT's Kubernetes Service. No disk I/O is
involved, so none of these commands use `-rst`/`-rss`/`-rsr` either.

All four commands use `-xspp tcp`, matching PostgreSQL's actual wire protocol (it is never UDP) —
testing over UDP would skip exactly the overhead (TCP handshake, per-flow conntrack state through
the Service, kernel socket buffers) that real DBMS connections actually pay.

20 and 23 both sweep `-nbp 1,2,4,8,16` (capped at the 16-server pool: beyond that, pods start
sharing a server via the `BEXHOMA_CHILD` modulo, which would confound scaling with server-side
contention instead of measuring pure client/network scaling), but measure different things: 20
uses `-xspm ul` (under-load, continuous send) to test whether *aggregate throughput* holds up as
concurrent pods grow, while 23 uses `-xspm pp` (ping-pong) to test whether *each individual
connection's round-trip latency* stays flat at the same pod counts. The two together separate
"does the pipe still carry the same total traffic" from "does my query still come back just as
fast" as concurrency grows — the latter is what `max_connections`/PgBouncer pool-size decisions
actually depend on, and a pool can look fine on the first question while quietly degrading on the
second. 21 and 22 instead fix `-nbp 1` and vary sockperf's message pattern/size to model one
connection's shape in isolation: 21 is a single synchronous query round-trip loop, 22 is a single
WAL-sender/`COPY`-style stream. See the netperf section above for the same questions asked at real
(not just per-pod) connection concurrency.

### 20. Pod/client scaling sweep

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

### Result

docs_hardware_sockperf_pod_scaling_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 906s 
* Code: 1783597421
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
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
  * disk:873765
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783597421
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873766
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783597421
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873567
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783597421
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873568
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783597421
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873569
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783597421

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783597421-685ffdf4df-lg6mt: 0

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

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.16 |                               0.11 |                               0.60 |                                0.88 |                              4969.66 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.17 |                               0.14 |                               0.60 |                                0.85 |                              4833.95 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.21 |                               0.15 |                               0.81 |                                1.05 |                              5069.14 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.19 |                               0.14 |                               0.86 |                                1.12 |                              4479.16 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.20 |                               0.14 |                               0.79 |                                1.39 |                              5089.91 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.18 |                               0.14 |                               0.70 |                                1.00 |                              4554.76 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.20 |                               0.16 |                               0.82 |                                1.20 |                              4439.97 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.18 |                               0.12 |                               0.78 |                                1.42 |                              4149.94 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.20 |                               0.16 |                               0.83 |                                1.55 |                              3774.32 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.16 |                               0.11 |                               0.75 |                                1.42 |                              4247.43 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.18 |                               0.14 |                               0.76 |                                1.44 |                              3953.01 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.17 |                               0.12 |                               0.75 |                                1.38 |                              4199.38 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.20 |                               0.16 |                               0.87 |                                1.86 |                              3593.45 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.19 |                               0.14 |                               0.83 |                                1.47 |                              4155.57 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.19 |                               0.15 |                               0.77 |                                1.98 |                              3792.28 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.23 |                               0.12 |                               1.65 |                                3.37 |                              2657.26 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         73 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.31 |                               0.20 |                               1.73 |                                3.15 |                              3811.08 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               1.71 |                               1.79 |                               4.10 |                                5.23 |                              4604.06 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         72 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.28 |                               0.19 |                               1.74 |                                3.44 |                              2681.46 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.34 |                               0.24 |                               1.80 |                                3.81 |                              2554.84 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         71 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.24 |                               0.13 |                               1.69 |                                3.93 |                              2615.10 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.32 |                               0.20 |                               1.68 |                                2.80 |                              3550.38 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.44 |                               0.37 |                               1.73 |                                2.82 |                              3727.24 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.26 |                               0.14 |                               1.61 |                                2.68 |                              3851.29 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               0.27 |                               0.18 |                               1.69 |                                3.31 |                              3925.88 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               1.92 |                               2.00 |                               4.51 |                                7.43 |                              3367.88 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               1.78 |                               1.85 |                               4.16 |                                5.19 |                              4494.25 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               1.87 |                               1.94 |                               4.47 |                                6.82 |                              3457.50 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.29 |                               0.18 |                               1.75 |                                3.75 |                              3725.49 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               1.88 |                               1.95 |                               4.41 |                                7.01 |                              3259.50 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.45 |                               0.37 |                               1.80 |                                3.31 |                              3753.87 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                               0.16 |                               0.11 |                               0.60 |                                0.88 |                              4969.66 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                               0.21 |                               0.15 |                               0.81 |                                1.05 |                              9903.09 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                               0.20 |                               0.16 |                               0.86 |                                1.39 |                             18563.80 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                               0.20 |                               0.16 |                               0.87 |                                1.98 |                             31865.38 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                          64 | max                     |                               1.92 |                               2.00 |                               4.51 |                                7.43 |                             56037.06 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        10.24 |      0.19 |           0.20 |                  0.20 |
| Hardware-1-1-2-1 |        15.27 |      0.37 |           0.20 |                  0.20 |
| Hardware-1-1-3-1 |        45.14 |      0.77 |           0.20 |                  0.20 |
| Hardware-1-1-4-1 |        71.48 |      1.46 |           0.21 |                  0.21 |
| Hardware-1-1-5-1 |       113.82 |      2.28 |           0.21 |                  0.21 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        41.18 |      1.05 |           0.10 |                  0.10 |
| Hardware-1-1-2-1 |        51.75 |      2.91 |           0.10 |                  0.10 |
| Hardware-1-1-3-1 |       157.43 |      6.08 |           0.10 |                  0.10 |
| Hardware-1-1-4-1 |       224.92 |     12.51 |           0.10 |                  0.10 |
| Hardware-1-1-5-1 |       535.28 |     24.91 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

### 21. PostgreSQL simple-query round-trip latency (ping-pong, TCP)

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

### Result

docs_hardware_sockperf_postgresql_query_latency.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 203s 
* Code: 1783598350
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
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
  * disk:873767
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598350

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783598350-5bc87c7bb9-qpppc: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.18 |                                0.21 |                              9058.66 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.18 |                                0.21 |                              9058.66 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         5.85 |      0.17 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        14.55 |      0.30 |           0.55 |                  0.55 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

### 22. PostgreSQL streaming/bulk throughput (WAL sender/COPY, TCP, 8k)

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

### Result

docs_hardware_sockperf_postgresql_streaming_throughput.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 170s 
* Code: 1783598573
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
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
  * disk:873574
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598573

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783598573-6f767ccbc5-lfsq5: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Execution

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1 | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                        8192 | max                     |                    20000 |                               0.35 |                               0.14 |                               4.88 |                                5.47 |                              1318.47 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         62 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | ul                       | tcp                          |                        8192 | max                     |                               0.35 |                               0.14 |                               4.88 |                                5.47 |                              1318.47 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        17.34 |      0.37 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        43.29 |      0.98 |           0.10 |                  0.10 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

### 23. PostgreSQL query latency under concurrent connections (ping-pong, TCP, `-nbp` sweep)

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

### Result

docs_hardware_sockperf_postgresql_latency_scaling_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (sockperf)
* Type: hardware
* Duration: 880s 
* Code: 1783598913
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), or network latency/throughput (sockperf) performance.
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
  * disk:873581
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598913
* Hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873571
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598913
* Hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873572
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598913
* Hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873573
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598913
* Hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.10.4
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:873574
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * eval_parameters
    * code:1783598913

### SUT Container Restarts
* bexhoma-sut-hardware-1-1783598913-677b5c5c79-79vxp: 0

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

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1-1-1  | Hardware-1-1-1 | Hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.05 |                               0.04 |                               0.18 |                                0.20 |                             10124.16 |                                0.00 |        0 |
| Hardware-1-1-2-1-1  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8989.67 |                                0.00 |        0 |
| Hardware-1-1-2-1-2  | Hardware-1-1-2 | Hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              8751.78 |                                0.00 |        0 |
| Hardware-1-1-3-1-1  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.05 |                               0.04 |                               0.19 |                                0.23 |                              9324.48 |                                0.00 |        0 |
| Hardware-1-1-3-1-2  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                              7936.14 |                                0.00 |        0 |
| Hardware-1-1-3-1-3  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.05 |                               0.04 |                               0.18 |                                0.21 |                              9917.53 |                                0.00 |        0 |
| Hardware-1-1-3-1-4  | Hardware-1-1-3 | Hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.05 |                               0.04 |                               0.18 |                                0.21 |                             10536.26 |                                0.00 |        0 |
| Hardware-1-1-4-1-1  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.05 |                               0.21 |                                0.25 |                              7033.85 |                                0.00 |        0 |
| Hardware-1-1-4-1-2  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.07 |                               0.04 |                               0.21 |                                0.25 |                              7302.25 |                                0.00 |        0 |
| Hardware-1-1-4-1-3  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.07 |                               0.05 |                               0.21 |                                0.25 |                              7047.86 |                                0.00 |        0 |
| Hardware-1-1-4-1-4  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.07 |                               0.05 |                               0.21 |                                0.25 |                              7240.82 |                                0.00 |        0 |
| Hardware-1-1-4-1-5  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.08 |                               0.05 |                               0.21 |                                0.26 |                              6574.69 |                                0.00 |        0 |
| Hardware-1-1-4-1-6  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.05 |                               0.04 |                               0.19 |                                0.24 |                              9115.40 |                                0.00 |        0 |
| Hardware-1-1-4-1-7  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.05 |                               0.04 |                               0.18 |                                0.23 |                              9981.98 |                                0.00 |        0 |
| Hardware-1-1-4-1-8  | Hardware-1-1-4 | Hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.04 |                               0.21 |                                0.25 |                              7380.59 |                                0.00 |        0 |
| Hardware-1-1-5-1-1  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.08 |                               0.05 |                               0.25 |                                0.29 |                              6513.90 |                                0.00 |        0 |
| Hardware-1-1-5-1-2  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6642.08 |                                0.00 |        0 |
| Hardware-1-1-5-1-3  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         74 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.08 |                               0.05 |                               0.25 |                                0.29 |                              6608.19 |                                0.00 |        0 |
| Hardware-1-1-5-1-4  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         73 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6361.53 |                                0.00 |        0 |
| Hardware-1-1-5-1-5  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         72 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6432.16 |                                0.00 |        0 |
| Hardware-1-1-5-1-6  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.05 |                               0.25 |                                0.28 |                              6925.19 |                                0.00 |        0 |
| Hardware-1-1-5-1-7  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.08 |                               0.06 |                               0.26 |                                0.29 |                              6095.21 |                                0.00 |        0 |
| Hardware-1-1-5-1-8  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.09 |                               0.06 |                               0.26 |                                0.29 |                              5557.31 |                                0.00 |        0 |
| Hardware-1-1-5-1-9  | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.06 |                               0.05 |                               0.24 |                                0.28 |                              7731.07 |                                0.00 |        0 |
| Hardware-1-1-5-1-10 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.07 |                               0.05 |                               0.25 |                                0.28 |                              7441.31 |                                0.00 |        0 |
| Hardware-1-1-5-1-11 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         69 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.08 |                               0.05 |                               0.25 |                                0.28 |                              6260.27 |                                0.00 |        0 |
| Hardware-1-1-5-1-12 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.06 |                               0.05 |                               0.22 |                                0.27 |                              8862.54 |                                0.00 |        0 |
| Hardware-1-1-5-1-13 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.07 |                               0.05 |                               0.25 |                                0.28 |                              6750.51 |                                0.00 |        0 |
| Hardware-1-1-5-1-14 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.07 |                               0.05 |                               0.25 |                                0.28 |                              6708.82 |                                0.00 |        0 |
| Hardware-1-1-5-1-15 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.08 |                               0.06 |                               0.26 |                                0.29 |                              6184.27 |                                0.00 |        0 |
| Hardware-1-1-5-1-16 | Hardware-1-1-5 | Hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                      0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.08 |                               0.05 |                               0.25 |                                0.29 |                              6385.32 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  1 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.05 |                               0.04 |                               0.18 |                                0.20 |                             10124.16 |                                0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           2 |         65 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                             17741.45 |                                0.00 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           4 |         67 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.06 |                               0.04 |                               0.19 |                                0.23 |                             37714.41 |                                0.00 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.05 |                               0.21 |                                0.26 |                             61677.45 |                                0.00 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |          16 |         75 |                   |                   |                      0 |                       |                    0 |                        0 |                        0 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |                  0 |                                   0.00 |                                 0.00 |                               0.00 |                                   0.00 |                                        0.00 |                                  0.00 | pp                       | tcp                          |                          64 | max                     |                               0.09 |                               0.06 |                               0.26 |                                0.29 |                            107459.69 |                                0.00 |        0 |

### Monitoring

### Execution phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |         5.46 |      0.17 |           0.20 |                  0.20 |
| Hardware-1-1-2-1 |        17.60 |      0.34 |           0.20 |                  0.20 |
| Hardware-1-1-3-1 |        40.23 |      0.68 |           0.20 |                  0.20 |
| Hardware-1-1-4-1 |        75.12 |      1.32 |           0.20 |                  0.20 |
| Hardware-1-1-5-1 |       127.93 |      2.61 |           0.20 |                  0.20 |

### Execution phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| Hardware-1-1-1-1 |        16.81 |      0.32 |           0.55 |                  0.55 |
| Hardware-1-1-2-1 |        20.83 |      0.88 |           0.55 |                  0.55 |
| Hardware-1-1-3-1 |        63.97 |      2.13 |           0.55 |                  0.55 |
| Hardware-1-1-4-1 |        83.70 |      3.54 |           0.55 |                  0.55 |
| Hardware-1-1-5-1 |       156.00 |      7.14 |           0.55 |                  0.55 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
* TEST passed: Execution Phase: every round has non-zero sockperf message rate
```

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
