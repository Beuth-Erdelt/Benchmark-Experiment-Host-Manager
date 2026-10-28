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
(I/O engine), `-xfsy`/`-xffd` (fsync/fdatasync interval), `-xfmx` (read percentage for mixed
`randrw`), and `-xfow` (overwrite, see below) — each accepts a comma-separated list, and every combination across the lists runs as one
more sequential round against the same SUT, so a whole sweep is one invocation instead of one
process per value. Because fio writes real data, request and size a persistent volume with
`-rst`/`-rss`, and pass `-rsr` so each command starts from a freshly recreated, empty volume rather
than inheriting whatever an earlier command left behind. The PVC name is fixed and shared across
the whole page (not scoped by experiment code), so fio commands must never be run concurrently
against the same SUT.

By default (`-xfow 0`) a write round writes into a fresh test file that fio has only fallocated, so
each write converts unwritten extents and each fsync/fdatasync also commits a filesystem journal
entry. That matches a table or index growing during a bulk load, but not PostgreSQL's WAL, whose
segments are zero-filled when created and then recycled, nor checkpoint writes into existing
relation files. `-xfow 1` lays out (fully writes) the test file before the timed part of the round,
so writes go into already written blocks. On a Ceph RBD volume (ext4) this made a large difference
for 8k writes with fdatasync after each, one job: about 370 commits/s on a fresh file versus about
1,540 on a prefilled one, with fdatasync dropping from 1.85 ms to a few µs. Use `-xfow 1` for
WAL-like rounds, or `-xfow 0,1` to measure both.

To compare storage backends in one experiment, give `-rst` a comma-separated list, e.g.
`-rst nvme,cephcsi,` (the empty last entry is the SUT's ephemeral storage). Each class gets its own
SUT (`Hardware-1`, `Hardware-2`, ...) with its own volume, and every fio round runs against each of
them. As in the other benchmarks, `-rc/-lc/-rr/-lr` may carry lists of the same length, paired by
position with `-rst`. Add `-ms 1` so the SUTs run one after another and do not compete for the
network or the storage cluster.

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
* Duration: 1928s 
* Code: 1793237274
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
  * disk:363101
  * volume_size:48.9G
  * volume_used:24.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
* hardware-1-1-10-1 uses docker image bexhoma/sut_hardware:0.11.10
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
    * code:1793237274
* hardware-1-1-11-1 uses docker image bexhoma/sut_hardware:0.11.10
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
    * code:1793237274
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
    * code:1793237274
* hardware-1-1-13-1 uses docker image bexhoma/sut_hardware:0.11.10
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
    * code:1793237274
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
    * code:1793237274
* hardware-1-1-15-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363118
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
* hardware-1-1-16-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363315
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363109
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
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
    * code:1793237274
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363111
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363111
  * volume_size:48.9G
  * volume_used:32.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793237274
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
    * code:1793237274
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
    * code:1793237274
* hardware-1-1-8-1 uses docker image bexhoma/sut_hardware:0.11.10
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
    * code:1793237274
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
    * code:1793237274

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793237274-5676867cfc-tcfqk: 0

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
| hardware-1-1-1-1-1  | hardware-1-1-1  | hardware-1-1-1-1  |                1 |        1 |               1 |       1 |         68 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  1902.43 |                      0.00 |                           0.72 |                            0.00 |                           0.79 |                            0.00 |                  1 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2  | hardware-1-1-2-1  |                1 |        2 |               1 |       1 |         67 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  3642.16 |                      0.00 |                           0.74 |                            0.00 |                           0.84 |                            0.00 |                  1 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3  | hardware-1-1-3-1  |                1 |        3 |               1 |       1 |         67 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                  7663.76 |                      0.00 |                           0.77 |                            0.00 |                           0.90 |                            0.00 |                  1 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4  | hardware-1-1-4-1  |                1 |        4 |               1 |       1 |         67 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 16518.27 |                      0.00 |                           0.74 |                            0.00 |                           0.87 |                            0.00 |                  1 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5  | hardware-1-1-5-1  |                1 |        5 |               1 |       1 |         67 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 33322.13 |                      0.00 |                           0.77 |                            0.00 |                           0.94 |                            0.00 |                  1 |        0 |
| hardware-1-1-6-1-1  | hardware-1-1-6  | hardware-1-1-6-1  |                1 |        6 |               1 |       1 |         67 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 54011.30 |                      0.00 |                           0.91 |                            0.00 |                           1.06 |                            0.00 |                  1 |        0 |
| hardware-1-1-7-1-1  | hardware-1-1-7  | hardware-1-1-7-1  |                1 |        7 |               1 |       1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                 84408.26 |                      0.00 |                           1.14 |                            0.00 |                           1.48 |                            0.00 |                  1 |        0 |
| hardware-1-1-8-1-1  | hardware-1-1-8  | hardware-1-1-8-1  |                1 |        8 |               1 |       1 |         66 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                118733.23 |                      0.00 |                           1.66 |                            0.00 |                           2.38 |                            0.00 |                  1 |        0 |
| hardware-1-1-9-1-1  | hardware-1-1-9  | hardware-1-1-9-1  |                1 |        9 |               1 |       1 |         64 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                    962.80 |                           0.00 |                            1.20 |                           0.00 |                            2.41 |                  1 |        0 |
| hardware-1-1-10-1-1 | hardware-1-1-10 | hardware-1-1-10-1 |                1 |       10 |               1 |       1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   2121.36 |                           0.00 |                            1.16 |                           0.00 |                            2.24 |                  1 |        0 |
| hardware-1-1-11-1-1 | hardware-1-1-11 | hardware-1-1-11-1 |                1 |       11 |               1 |       1 |         63 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                   5796.29 |                           0.00 |                            1.03 |                           0.00 |                            1.71 |                  1 |        0 |
| hardware-1-1-12-1-1 | hardware-1-1-12 | hardware-1-1-12-1 |                1 |       12 |               1 |       1 |         63 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  12453.04 |                           0.00 |                            0.91 |                           0.00 |                            1.56 |                  1 |        0 |
| hardware-1-1-13-1-1 | hardware-1-1-13 | hardware-1-1-13-1 |                1 |       13 |               1 |       1 |         64 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  22336.81 |                           0.00 |                            1.02 |                           0.00 |                            1.63 |                  1 |        0 |
| hardware-1-1-14-1-1 | hardware-1-1-14 | hardware-1-1-14-1 |                1 |       14 |               1 |       1 |         63 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  36512.05 |                           0.00 |                            1.27 |                           0.00 |                            1.84 |                  1 |        0 |
| hardware-1-1-15-1-1 | hardware-1-1-15 | hardware-1-1-15-1 |                1 |       15 |               1 |       1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  56583.03 |                           0.00 |                            1.71 |                           0.00 |                            2.28 |                  1 |        0 |
| hardware-1-1-16-1-1 | hardware-1-1-16 | hardware-1-1-16-1 |                1 |       16 |               1 |       1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                      1 |                     0.00 |                  70224.79 |                           0.00 |                            3.16 |                           0.00 |                            4.75 |                  1 |        0 |

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors | hardware_type   |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|:----------------|
| hardware-1-1-1  | hardware-1-1-1  |                1 |        1 |               1 |           1 |         68 | randread          | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                  1902.43 |                      0.00 |                           0.72 |                            0.00 |                           0.79 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-2  | hardware-1-1-2  |                1 |        2 |               1 |           1 |         67 | randread          | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                  3642.16 |                      0.00 |                           0.74 |                            0.00 |                           0.84 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-3  | hardware-1-1-3  |                1 |        3 |               1 |           1 |         67 | randread          | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                  7663.76 |                      0.00 |                           0.77 |                            0.00 |                           0.90 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-4  | hardware-1-1-4  |                1 |        4 |               1 |           1 |         67 | randread          | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                 16518.27 |                      0.00 |                           0.74 |                            0.00 |                           0.87 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-5  | hardware-1-1-5  |                1 |        5 |               1 |           1 |         67 | randread          | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                 33322.13 |                      0.00 |                           0.77 |                            0.00 |                           0.94 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-6  | hardware-1-1-6  |                1 |        6 |               1 |           1 |         67 | randread          | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                 54011.30 |                      0.00 |                           0.91 |                            0.00 |                           1.06 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-7  | hardware-1-1-7  |                1 |        7 |               1 |           1 |         67 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                 84408.26 |                      0.00 |                           1.14 |                            0.00 |                           1.48 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-8  | hardware-1-1-8  |                1 |        8 |               1 |           1 |         66 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                118733.23 |                      0.00 |                           1.66 |                            0.00 |                           2.38 |                            0.00 |                  1 |        0 | fio             |
| hardware-1-1-9  | hardware-1-1-9  |                1 |        9 |               1 |           1 |         64 | randwrite         | 4k                |                      1 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                    962.80 |                           0.00 |                            1.20 |                           0.00 |                            2.41 |                  1 |        0 | fio             |
| hardware-1-1-10 | hardware-1-1-10 |                1 |       10 |               1 |           1 |         64 | randwrite         | 4k                |                      2 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   2121.36 |                           0.00 |                            1.16 |                           0.00 |                            2.24 |                  1 |        0 | fio             |
| hardware-1-1-11 | hardware-1-1-11 |                1 |       11 |               1 |           1 |         63 | randwrite         | 4k                |                      4 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                   5796.29 |                           0.00 |                            1.03 |                           0.00 |                            1.71 |                  1 |        0 | fio             |
| hardware-1-1-12 | hardware-1-1-12 |                1 |       12 |               1 |           1 |         63 | randwrite         | 4k                |                      8 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  12453.04 |                           0.00 |                            0.91 |                           0.00 |                            1.56 |                  1 |        0 | fio             |
| hardware-1-1-13 | hardware-1-1-13 |                1 |       13 |               1 |           1 |         64 | randwrite         | 4k                |                     16 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  22336.81 |                           0.00 |                            1.02 |                           0.00 |                            1.63 |                  1 |        0 | fio             |
| hardware-1-1-14 | hardware-1-1-14 |                1 |       14 |               1 |           1 |         63 | randwrite         | 4k                |                     32 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  36512.05 |                           0.00 |                            1.27 |                           0.00 |                            1.84 |                  1 |        0 | fio             |
| hardware-1-1-15 | hardware-1-1-15 |                1 |       15 |               1 |           1 |         63 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  56583.03 |                           0.00 |                            1.71 |                           0.00 |                            2.28 |                  1 |        0 | fio             |
| hardware-1-1-16 | hardware-1-1-16 |                1 |       16 |               1 |           1 |         63 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                        0 |                       50 |                     0.00 |                  70224.79 |                           0.00 |                            3.16 |                           0.00 |                            4.75 |                  1 |        0 | fio             |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |        70.23 |      2.05 |           0.21 |                  0.21 |
| hardware-1-1-2-1  |        69.24 |      1.73 |           0.21 |                  0.21 |
| hardware-1-1-3-1  |        64.32 |      2.20 |           0.21 |                  0.21 |
| hardware-1-1-4-1  |        62.95 |      1.64 |           0.21 |                  0.21 |
| hardware-1-1-5-1  |        79.04 |      2.69 |           0.23 |                  0.66 |
| hardware-1-1-6-1  |        70.86 |      1.80 |           0.21 |                  0.21 |
| hardware-1-1-7-1  |        86.91 |      2.27 |           0.33 |                  4.33 |
| hardware-1-1-8-1  |        90.48 |      1.97 |           0.33 |                  4.33 |
| hardware-1-1-9-1  |        40.92 |      1.03 |           0.21 |                  0.22 |
| hardware-1-1-10-1 |        56.76 |      1.74 |           0.21 |                  0.22 |
| hardware-1-1-11-1 |        68.32 |      1.92 |           0.22 |                  0.22 |
| hardware-1-1-12-1 |        71.60 |      1.92 |           0.21 |                  0.23 |
| hardware-1-1-13-1 |        67.29 |      2.00 |           0.21 |                  0.23 |
| hardware-1-1-14-1 |        82.60 |      2.28 |           0.23 |                  0.24 |
| hardware-1-1-15-1 |        81.59 |      2.16 |           0.22 |                  0.24 |
| hardware-1-1-16-1 |        86.67 |      2.08 |           0.22 |                  0.25 |

### Benchmarking phase: component benchmarker

| DBMS              |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:------------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1  |         0.86 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-2-1  |         0.86 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-3-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-4-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-5-1  |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-6-1  |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-7-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-8-1  |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-9-1  |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-10-1 |         0.84 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-11-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-12-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-13-1 |         0.84 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-14-1 |         0.83 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-15-1 |         0.85 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-16-1 |         0.84 |      0.03 |           0.00 |                  0.00 |

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
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-12-1 (bexhoma-metrics-hardware-1-1-12-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-13-1 (bexhoma-metrics-hardware-1-1-13-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-14-1 (bexhoma-metrics-hardware-1-1-14-1-benchmarker.log, expected: series exists only while non-zero)
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
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
  -xfow 1 \
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
* Duration: 159s 
* Code: 1793241233
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
  * Overwrite (prefilled test file) swept: ['1'].
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
  * disk:363111
  * volume_size:48.9G
  * volume_used:24.0K
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241233

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793241233-6b76797bb5-n5n2n: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_numjobs |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-----------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         67 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                        1 |                       50 |                      1 |                     0.00 |                    372.14 |                           0.00 |                            1.09 |                           0.00 |                            1.47 |                  1 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_overwrite |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   hardware_threads |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|-------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         67 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                        1 |                       50 |                     0.00 |                    372.14 |                           0.00 |                            1.09 |                           0.00 |                            1.47 |                  1 |        0 | fio             |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        59.63 |      2.02 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.83 |      0.04 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Read Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* Filesystem Write Total, Largest Device (RAID Counted Once) [MiB] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 468s 
* Code: 1793241417
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [1, 2, 4, 8], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 2, 4, 8] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363112
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241417
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363112
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241417
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363113
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241417
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363113
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241417

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793241417-84b9b8fdf9-bxlxd: 0

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

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                  1 |                                1206.48 |                                60.00 |                               0.83 |                             6970690.44 |                                     6807.31 |                                  0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         63 |                  2 |                                2377.81 |                                60.00 |                               0.92 |                             3585340.29 |                                     3501.31 |                                  0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         70 |                  4 |                                2326.14 |                                60.00 |                               1.30 |                             1170079.84 |                                     1142.66 |                                  0.00 |        0 |
| hardware-1-1-4-1-1 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         72 |                  8 |                                2146.57 |                                60.05 |                               1.34 |                              973370.75 |                                      950.56 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                  1 |                                1206.48 |                                60.00 |                               0.83 |                             6970690.44 |                                     6807.31 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           1 |         63 |                  2 |                                2377.81 |                                60.00 |                               0.92 |                             3585340.29 |                                     3501.31 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           1 |         70 |                  4 |                                2326.14 |                                60.00 |                               1.30 |                             1170079.84 |                                     1142.66 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           1 |         72 |                  8 |                                2146.57 |                                60.05 |                               1.34 |                              973370.75 |                                      950.56 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        50.96 |      1.00 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |       119.90 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        91.45 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-4-1 |       119.87 |      2.00 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.60 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         0.61 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |         0.59 |      0.01 |           0.00 |                  0.00 |
| hardware-1-1-4-1 |         0.63 |      0.00 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 373s 
* Code: 1793241911
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [4], split across pod count(s): [1, 2, 4].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [4] threads, split into [1, 2, 4] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363114
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241911
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363312
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241911
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363116
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793241911

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793241911-68d9bdd7c4-4g57q: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)
* DBMS Hardware-1 - Experiment 1 Client 3: hardware (4 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         70 |                  4 |                                2274.51 |                                60.01 |                               1.32 |                             1226736.16 |                                     1197.98 |                                  0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         67 |                  2 |                                1157.44 |                                60.00 |                               1.32 |                             1869665.41 |                                     1825.85 |                                  0.00 |        0 |
| hardware-1-1-2-1-2 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         68 |                  2 |                                1143.71 |                                60.02 |                               1.32 |                             1983394.56 |                                     1936.91 |                                  0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         67 |                  1 |                                 551.85 |                                60.00 |                               1.32 |                             3632711.06 |                                     3547.57 |                                  0.00 |        0 |
| hardware-1-1-3-1-2 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         66 |                  1 |                                 550.71 |                                60.02 |                               1.32 |                             3482405.80 |                                     3400.79 |                                  0.00 |        0 |
| hardware-1-1-3-1-3 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         66 |                  1 |                                 551.21 |                                60.00 |                               1.32 |                             3857258.34 |                                     3766.85 |                                  0.00 |        0 |
| hardware-1-1-3-1-4 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                  1 |                                 549.85 |                                60.00 |                               1.32 |                             3683711.40 |                                     3597.37 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         70 |                  4 |                                2274.51 |                                60.01 |                               1.32 |                             1226736.16 |                                     1197.98 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         68 |                  4 |                                2301.15 |                                60.02 |                               1.32 |                             3853059.97 |                                     3762.76 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         67 |                  4 |                                2203.62 |                                60.02 |                               1.32 |                            14656086.60 |                                    14312.58 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       127.21 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |        92.27 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |       102.54 |      2.00 |           0.22 |                  0.22 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.61 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         1.25 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |         2.61 |      0.03 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 494s 
* Code: 1793242315
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1, 2, 4, 8] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363117
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242315
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363117
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242315
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363118
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242315
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363119
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242315

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793242315-544bc5bbbc-zzsmz: 0

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

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  2 |                                2222.29 |                                60.00 |                               1.27 |                             3679035.89 |                                     3592.81 |                                  0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         67 |                  2 |                                1133.29 |                                60.02 |                               1.32 |                             2279492.18 |                                     2226.07 |                                  0.00 |        0 |
| hardware-1-1-2-1-2 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         67 |                  2 |                                1113.07 |                                60.00 |                               1.32 |                             2167667.94 |                                     2116.86 |                                  0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         72 |                  2 |                                 542.75 |                                60.00 |                              32.53 |                             1485844.64 |                                     1451.02 |                                  0.00 |        0 |
| hardware-1-1-3-1-2 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         70 |                  2 |                                 554.26 |                                60.00 |                              32.53 |                             1627649.15 |                                     1589.50 |                                  0.00 |        0 |
| hardware-1-1-3-1-3 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         71 |                  2 |                                 549.23 |                                60.03 |                              32.53 |                             1389097.90 |                                     1356.54 |                                  0.00 |        0 |
| hardware-1-1-3-1-4 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         69 |                  2 |                                 546.77 |                                60.01 |                              32.53 |                             1579677.10 |                                     1542.65 |                                  0.00 |        0 |
| hardware-1-1-4-1-1 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         85 |                  2 |                                 272.04 |                                60.00 |                              56.84 |                              609501.22 |                                      595.22 |                                  0.00 |        0 |
| hardware-1-1-4-1-2 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         86 |                  2 |                                 270.72 |                                60.03 |                              56.84 |                              539698.01 |                                      527.05 |                                  0.00 |        0 |
| hardware-1-1-4-1-3 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         82 |                  2 |                                 264.47 |                                60.00 |                              56.84 |                              669886.93 |                                      654.19 |                                  0.00 |        0 |
| hardware-1-1-4-1-4 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         85 |                  2 |                                 271.11 |                                60.00 |                              56.84 |                              550114.73 |                                      537.22 |                                  0.00 |        0 |
| hardware-1-1-4-1-5 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         83 |                  2 |                                 270.91 |                                60.00 |                              56.84 |                              551894.34 |                                      538.96 |                                  0.00 |        0 |
| hardware-1-1-4-1-6 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         79 |                  2 |                                 269.66 |                                60.00 |                              56.84 |                              688110.45 |                                      671.98 |                                  0.00 |        0 |
| hardware-1-1-4-1-7 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         78 |                  2 |                                 283.99 |                                60.00 |                              56.84 |                              740823.43 |                                      723.46 |                                  0.00 |        0 |
| hardware-1-1-4-1-8 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         78 |                  2 |                                 271.15 |                                60.00 |                              56.84 |                              687796.40 |                                      671.68 |                                  0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  2 |                                2222.29 |                                60.00 |                               1.27 |                             3679035.89 |                                     3592.81 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         67 |                  4 |                                2246.36 |                                60.02 |                               1.32 |                             4447160.12 |                                     4342.93 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         72 |                  8 |                                2193.01 |                                60.03 |                              32.53 |                             6082268.79 |                                     5939.71 |                                  0.00 |        0 | sysbench        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         86 |                 16 |                                2174.05 |                                60.03 |                              56.84 |                             5037825.51 |                                     4919.76 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       107.64 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |       108.08 |      2.00 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        78.63 |      2.00 |           0.22 |                  0.22 |
| hardware-1-1-4-1 |       136.31 |      2.00 |           0.23 |                  0.23 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         0.62 |      0.02 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |         1.30 |      0.00 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |         2.64 |      0.03 |           0.00 |                  0.00 |
| hardware-1-1-4-1 |         6.10 |      0.19 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 176s 
* Code: 1793242840
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sysbench.
  * Duration per round is 60s, capping each of the CPU and memory phases (see images/hardware/benchmarker/run_sysbench.sh).
  * Total sysbench thread count(s) swept: [2], split across pod count(s): [1].
  * CPU phase: sysbench cpu --cpu-max-prime=20000 (fixed).
  * Memory phase: sysbench memory --memory-block-size=1K --memory-total-size=10G (fixed; may finish before the duration cap if this transfers first).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [2] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Number of tenants is 4, one container per tenant.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * Results are validated against basic correctness requirements.
  * SUT requests 2 CPU and 16Gi RAM. CPU limit is 2.

### Connections
* hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242840
* hardware-2-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242840
* hardware-3-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242840
* hardware-4-1-1-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:2
  * requests_memory:16Gi
  * limits_cpu:2
  * resources_total: 2.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 2.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793242840

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793242840-685b6b98f6-mr8z6: 0
* bexhoma-sut-hardware-2-1793242840-85dbc7778b-rn6vr: 0
* bexhoma-sut-hardware-3-1793242840-86445ffd96-znf9b: 0
* bexhoma-sut-hardware-4-1793242840-986ff76f8-2zlxk: 0

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

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         68 |                  2 |                                2216.68 |                                60.00 |                               1.27 |                             6373949.37 |                                     6224.56 |                                  0.00 |        0 |
| hardware-2-1-1-1-1 | hardware-2-1-1 | hardware-2-1-1-1 |                1 |        1 |               1 |       1 |         65 |                  2 |                                2206.39 |                                60.00 |                               1.30 |                             4669439.19 |                                     4560.00 |                                  0.00 |        0 |
| hardware-3-1-1-1-1 | hardware-3-1-1 | hardware-3-1-1-1 |                1 |        1 |               1 |       1 |         67 |                  2 |                                2217.45 |                                60.00 |                               1.27 |                             3689508.72 |                                     3603.04 |                                  0.00 |        0 |
| hardware-4-1-1-1-1 | hardware-4-1-1 | hardware-4-1-1-1 |                1 |        1 |               1 |       1 |         69 |                  2 |                                2208.08 |                                60.00 |                               1.27 |                             3424810.06 |                                     3344.54 |                                  0.00 |        0 |

#### Per Phase

| DBMS             | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   tenant_id |   duration |   hardware_threads |   hardware_sysbench_cpu_events_per_sec |   hardware_sysbench_cpu_total_time_s |   hardware_sysbench_cpu_lat_p95_ms |   hardware_sysbench_memory_ops_per_sec |   hardware_sysbench_memory_throughput_mibps |   hardware_sysbench_memory_lat_p95_ms |   errors | hardware_type   |
|:-----------------|:---------------|-----------------:|---------:|----------------:|------------:|------------:|-----------:|-------------------:|---------------------------------------:|-------------------------------------:|-----------------------------------:|---------------------------------------:|--------------------------------------------:|--------------------------------------:|---------:|:----------------|
| hardware-1-1-1-0 | hardware-1-1-1 |                1 |        1 |               1 |           1 |           0 |         68 |                  2 |                                2216.68 |                                60.00 |                               1.27 |                             6373949.37 |                                     6224.56 |                                  0.00 |        0 | sysbench        |
| hardware-2-1-1-1 | hardware-2-1-1 |                1 |        1 |               1 |           1 |           1 |         65 |                  2 |                                2206.39 |                                60.00 |                               1.30 |                             4669439.19 |                                     4560.00 |                                  0.00 |        0 | sysbench        |
| hardware-3-1-1-2 | hardware-3-1-1 |                1 |        1 |               1 |           1 |           2 |         67 |                  2 |                                2217.45 |                                60.00 |                               1.27 |                             3689508.72 |                                     3603.04 |                                  0.00 |        0 | sysbench        |
| hardware-4-1-1-3 | hardware-4-1-1 |                1 |        1 |               1 |           1 |           3 |         69 |                  2 |                                2208.08 |                                60.00 |                               1.27 |                             3424810.06 |                                     3344.54 |                                  0.00 |        0 | sysbench        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       114.50 |      2.00 |           0.21 |                  0.21 |
| hardware-2-1-1-1 |       101.89 |      2.00 |           0.21 |                  0.21 |
| hardware-3-1-1-1 |       115.07 |      2.00 |           0.21 |                  0.21 |
| hardware-4-1-1-1 |       104.21 |      2.00 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         3.81 |      0.00 |           0.01 |                  0.01 |
| hardware-2-1-1-1 |         3.24 |      0.08 |           0.01 |                  0.01 |
| hardware-3-1-1-1 |         3.33 |      0.00 |           0.01 |                  0.01 |
| hardware-4-1-1-1 |         3.58 |      0.00 |           0.01 |                  0.01 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-2-1-1-1 (bexhoma-metrics-hardware-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-2-1-1-1 (bexhoma-metrics-hardware-2-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-3-1-1-1 (bexhoma-metrics-hardware-3-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-3-1-1-1 (bexhoma-metrics-hardware-3-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-4-1-1-1 (bexhoma-metrics-hardware-4-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-4-1-1-1 (bexhoma-metrics-hardware-4-1-1-1-benchmarker.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 154s 
* Code: 1793243040
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
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
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243040

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793243040-7b45bcb998-k4g44: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         60 |                  1 | tcp                         |                             9535.39 |                              0.10 |                              0.06 |                              0.27 |                              0.44 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         60 |                  1 | tcp                         |                             9535.39 |                              0.10 |                              0.06 |                              0.27 |                              0.44 |                                0.00 |        0 | netperf         |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         7.04 |      0.15 |           0.20 |                  0.20 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         6.55 |      0.24 |           0.00 |                  0.00 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 593s 
* Code: 1793243217
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1, 8, 16, 32, 64] threads, split into [1] pods.
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
  * disk:363121
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363122
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363123
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363123
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363124
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243217

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793243217-67bd87489d-7nrgd: 0

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

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         60 |                  1 | tcp                         |                             6253.52 |                              0.16 |                              0.07 |                              0.39 |                              0.47 |                                0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         62 |                  8 | tcp                         |                            59160.06 |                              0.21 |                              0.09 |                              0.45 |                              0.53 |                                0.00 |        0 |
| hardware-1-1-3-1-1 | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         63 |                 16 | tcp                         |                           129741.72 |                              0.20 |                              0.08 |                              0.46 |                              0.60 |                                0.00 |        0 |
| hardware-1-1-4-1-1 | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         65 |                 32 | tcp                         |                           351120.10 |                              0.17 |                              0.08 |                              0.45 |                              0.55 |                                0.00 |        0 |
| hardware-1-1-5-1-1 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         68 |                 64 | tcp                         |                           776966.99 |                              0.13 |                              0.09 |                              0.38 |                              0.54 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         60 |                  1 | tcp                         |                             6253.52 |                              0.16 |                              0.07 |                              0.39 |                              0.47 |                                0.00 |        0 | netperf         |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           1 |         62 |                  8 | tcp                         |                            59160.06 |                              0.21 |                              0.09 |                              0.45 |                              0.53 |                                0.00 |        0 | netperf         |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           1 |         63 |                 16 | tcp                         |                           129741.72 |                              0.20 |                              0.08 |                              0.46 |                              0.60 |                                0.00 |        0 | netperf         |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           1 |         65 |                 32 | tcp                         |                           351120.10 |                              0.17 |                              0.08 |                              0.44 |                              0.55 |                                0.00 |        0 | netperf         |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |           1 |         68 |                 64 | tcp                         |                           776966.99 |                              0.13 |                              0.09 |                              0.38 |                              0.54 |                                0.00 |        0 | netperf         |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         6.52 |      0.13 |           0.21 |                  0.21 |
| hardware-1-1-2-1 |        33.94 |      0.97 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        92.94 |      2.03 |           0.21 |                  0.21 |
| hardware-1-1-4-1 |       274.13 |      5.00 |           0.21 |                  0.21 |
| hardware-1-1-5-1 |       571.83 |     10.57 |           0.22 |                  0.22 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         8.48 |      0.25 |           0.00 |                  0.00 |
| hardware-1-1-2-1 |        67.19 |      1.82 |           0.00 |                  0.00 |
| hardware-1-1-3-1 |        93.40 |      3.52 |           0.01 |                  0.01 |
| hardware-1-1-4-1 |       235.79 |      6.15 |           0.01 |                  0.01 |
| hardware-1-1-5-1 |       438.66 |     13.06 |           0.02 |                  0.02 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 262s 
* Code: 1793243847
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: netperf.
  * Duration per round is 60s.
  * Protocol(s) swept: ['tcp'] (selects TCP_RR/UDP_RR).
  * Concurrent client instances per pod controlled via HARDWARE_THREADS (see images/hardware/benchmarker/run_netperf.sh).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [64] threads, split into [1, 2] pods.
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
  * disk:363125
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243847
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363126
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793243847

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793243847-5698fb5477-z2zhq: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)
* DBMS Hardware-1 - Experiment 1 Client 2: hardware (2 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         69 |                 64 | tcp                         |                           844302.74 |                              0.12 |                              0.09 |                              0.34 |                              0.49 |                                0.00 |        0 |
| hardware-1-1-2-1-1 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                 32 | tcp                         |                           387351.27 |                              0.12 |                              0.09 |                              0.37 |                              0.51 |                                0.00 |        0 |
| hardware-1-1-2-1-2 | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         65 |                 32 | tcp                         |                           397033.75 |                              0.12 |                              0.09 |                              0.36 |                              0.51 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_netperf_protocol   |   hardware_netperf_transaction_rate |   hardware_netperf_latency_avg_ms |   hardware_netperf_latency_p50_ms |   hardware_netperf_latency_p90_ms |   hardware_netperf_latency_p99_ms |   hardware_netperf_instances_failed |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:----------------------------|------------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         69 |                 64 | tcp                         |                           844302.74 |                              0.12 |                              0.09 |                              0.34 |                              0.49 |                                0.00 |        0 | netperf         |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                 64 | tcp                         |                           784385.02 |                              0.12 |                              0.09 |                              0.37 |                              0.51 |                                0.00 |        0 | netperf         |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       489.74 |     10.83 |           0.22 |                  0.22 |
| hardware-1-1-2-1 |       582.63 |     10.59 |           0.22 |                  0.22 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |       485.23 |     14.18 |           0.02 |                  0.02 |
| hardware-1-1-2-1 |       475.86 |     13.28 |           0.01 |                  0.01 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
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
* Duration: 623s 
* Code: 1793244151
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
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
  * disk:363127
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363128
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363128
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363129
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363327
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244151

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793244151-869c87cd7c-dqpvw: 0

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

### Benchmarking

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1  | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                  1 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.44 |                               0.42 |                               0.77 |                                1.91 |                              9252.41 |                                0.00 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.44 |                               0.36 |                               0.85 |                               27.21 |                             10830.26 |                                0.00 |        0 |
| hardware-1-1-2-1-2  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.45 |                               0.37 |                               2.14 |                               14.01 |                             10063.04 |                                0.00 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.40 |                               0.38 |                               0.95 |                                3.32 |                             10399.95 |                                0.00 |        0 |
| hardware-1-1-3-1-2  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.40 |                               0.37 |                               0.75 |                                9.28 |                              9912.96 |                                0.00 |        0 |
| hardware-1-1-3-1-3  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.50 |                               0.38 |                               4.94 |                               16.26 |                              9488.06 |                                0.00 |        0 |
| hardware-1-1-3-1-4  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.44 |                               0.43 |                               0.81 |                                2.30 |                              8417.20 |                                0.00 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.81 |                               0.41 |                              16.88 |                               43.07 |                              7782.85 |                                0.00 |        0 |
| hardware-1-1-4-1-2  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.45 |                               0.43 |                               0.89 |                                1.61 |                              8367.50 |                                0.00 |        0 |
| hardware-1-1-4-1-3  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         69 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.42 |                               0.41 |                               0.89 |                                1.72 |                              6935.79 |                                0.00 |        0 |
| hardware-1-1-4-1-4  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.45 |                               0.39 |                               1.00 |                               20.12 |                              6958.56 |                                0.00 |        0 |
| hardware-1-1-4-1-5  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.45 |                               0.39 |                               2.23 |                                6.46 |                              8387.32 |                                0.00 |        0 |
| hardware-1-1-4-1-6  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.71 |                               0.43 |                              12.90 |                               25.94 |                              7902.44 |                                0.00 |        0 |
| hardware-1-1-4-1-7  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.58 |                               0.41 |                               3.29 |                               30.59 |                              6955.55 |                                0.00 |        0 |
| hardware-1-1-4-1-8  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               0.40 |                               0.39 |                               0.79 |                                2.21 |                              8525.09 |                                0.00 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         76 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20000 |                               0.48 |                               0.45 |                               1.02 |                                4.79 |                              6152.54 |                                0.00 |        0 |
| hardware-1-1-5-1-2  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20001 |                               0.50 |                               0.41 |                               1.35 |                               21.84 |                              7303.27 |                                0.00 |        0 |
| hardware-1-1-5-1-3  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20002 |                               0.50 |                               0.37 |                               2.68 |                               21.54 |                             10424.57 |                                0.00 |        0 |
| hardware-1-1-5-1-4  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         75 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20003 |                               0.63 |                               0.27 |                               7.69 |                               28.30 |                              8436.13 |                                0.00 |        0 |
| hardware-1-1-5-1-5  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         74 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20004 |                               0.52 |                               0.38 |                               2.68 |                               21.52 |                              7669.17 |                                0.00 |        0 |
| hardware-1-1-5-1-6  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20005 |                               0.56 |                               0.45 |                               2.04 |                               20.07 |                              7540.68 |                                0.00 |        0 |
| hardware-1-1-5-1-7  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20006 |                               0.90 |                               0.27 |                               9.64 |                               40.42 |                              6530.85 |                                0.00 |        0 |
| hardware-1-1-5-1-8  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         72 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20007 |                               1.14 |                               0.28 |                              20.19 |                               23.92 |                              7639.16 |                                0.00 |        0 |
| hardware-1-1-5-1-9  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20008 |                               0.43 |                               0.38 |                               1.13 |                               11.62 |                              6565.58 |                                0.00 |        0 |
| hardware-1-1-5-1-10 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20009 |                               0.47 |                               0.40 |                               1.15 |                               14.60 |                              8829.54 |                                0.00 |        0 |
| hardware-1-1-5-1-11 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20010 |                               0.45 |                               0.41 |                               0.97 |                               10.47 |                              7806.15 |                                0.00 |        0 |
| hardware-1-1-5-1-12 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20011 |                               0.51 |                               0.38 |                               1.10 |                               24.92 |                              7255.52 |                                0.00 |        0 |
| hardware-1-1-5-1-13 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20012 |                               0.35 |                               0.31 |                               0.78 |                                5.94 |                              8654.83 |                                0.00 |        0 |
| hardware-1-1-5-1-14 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         67 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20013 |                               0.69 |                               0.30 |                               7.12 |                               22.81 |                              6340.31 |                                0.00 |        0 |
| hardware-1-1-5-1-15 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20014 |                               0.97 |                               0.31 |                              21.86 |                               35.13 |                              5937.63 |                                0.00 |        0 |
| hardware-1-1-5-1-16 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         65 |                  0 | ul                       | tcp                          |                          64 | max                     |                    20015 |                               0.75 |                               0.27 |                               6.99 |                               22.26 |                              7085.74 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                  1 | ul                       | tcp                          |                          64 | max                     |                               0.44 |                               0.42 |                               0.77 |                                1.91 |                              9252.41 |                                0.00 |        0 | sockperf        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.45 |                               0.37 |                               2.14 |                               27.21 |                             20893.30 |                                0.00 |        0 | sockperf        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.50 |                               0.43 |                               4.94 |                               16.26 |                             38218.18 |                                0.00 |        0 | sockperf        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         70 |                  0 | ul                       | tcp                          |                          64 | max                     |                               0.81 |                               0.43 |                              16.88 |                               43.07 |                             61815.09 |                                0.00 |        0 | sockperf        |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |          16 |         76 |                  0 | ul                       | tcp                          |                          64 | max                     |                               1.14 |                               0.45 |                              21.86 |                               40.42 |                            120171.68 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         4.34 |      0.12 |           0.20 |                  0.20 |
| hardware-1-1-2-1 |        14.63 |      0.27 |           0.21 |                  0.21 |
| hardware-1-1-3-1 |        34.54 |      0.69 |           0.21 |                  0.21 |
| hardware-1-1-4-1 |        35.65 |      0.98 |           0.21 |                  0.21 |
| hardware-1-1-5-1 |       135.65 |      2.79 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        39.47 |      1.06 |           0.10 |                  0.10 |
| hardware-1-1-2-1 |        81.00 |      2.10 |           0.10 |                  0.10 |
| hardware-1-1-3-1 |       210.65 |      4.44 |           0.10 |                  0.10 |
| hardware-1-1-4-1 |       437.32 |      8.76 |           0.10 |                  0.10 |
| hardware-1-1-5-1 |       717.16 |     17.49 |           0.10 |                  0.10 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 149s 
* Code: 1793244805
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
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
  * disk:363131
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244805

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793244805-dcb97bbfc-nqtmp: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         65 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.04 |                               0.22 |                                0.26 |                              7069.45 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         65 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.07 |                               0.04 |                               0.22 |                                0.26 |                              7069.45 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         9.09 |      0.15 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         9.30 |      0.21 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 144s 
* Code: 1793244979
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['ul'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [8192] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
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
  * disk:363132
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793244979

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793244979-5774786df-gfkvh: 0

### Workflow

#### Actual

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

#### Planned

* DBMS Hardware-1 - Experiment 1 Client 1: hardware (1 pods)

### Benchmarking

#### Per Connection

| DBMS               | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:-------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1 | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         63 |                  1 | ul                       | tcp                          |                        8192 | max                     |                    20000 |                               0.36 |                               0.12 |                               2.30 |                                2.71 |                              2225.99 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         63 |                  1 | ul                       | tcp                          |                        8192 | max                     |                               0.36 |                               0.12 |                               2.30 |                                2.71 |                              2225.99 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        25.09 |      0.52 |           0.21 |                  0.21 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        37.50 |      1.04 |           0.10 |                  0.10 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
* Duration: 623s 
* Code: 1793245151
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio), CPU/memory (sysbench), single-connection network latency/throughput (sockperf), or many-connection network throughput (netperf) performance.
  * Benchmark tool: sockperf.
  * Duration per round is 60s.
  * Mode(s) swept: ['pp'] (pp = ping-pong, ul = under-load).
  * Protocol(s) swept: ['tcp'].
  * Message size(s) swept: [64] bytes.
  * Message rate(s) swept: ['max'] (messages/sec, or 'max' for uncapped).
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.10.
  * System metrics are monitored by sidecar containers.
  * Experiment is limited to DBMS ['Hardware'].
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Benchmarking is tested with [1] threads, split into [1, 2, 4, 8, 16] pods.
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
  * disk:363133
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-2-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363331
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-3-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363160
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-4-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363221
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151
* hardware-1-1-5-1 uses docker image bexhoma/sut_hardware:0.11.10
  * RAM:2164173156352
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-147-generic
  * node:cl-worker36
  * disk:363221
  * cpu_list:0-223
  * requests_cpu:4
  * requests_memory:16Gi
  * resources_total: 4.0 CPU, 16.0 GiB RAM requested in 1 pods
    * sut: 1 x, 4.0 CPU, 16.0 GiB RAM
  * eval_parameters
    * code:1793245151

### SUT Container Restarts
* bexhoma-sut-hardware-1-1793245151-7d87d85bd7-k8kn6: 0

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

### Benchmarking

#### Per Connection

| DBMS                | phase          | job              |   experiment_run |   client |   benchmark_run |   child |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_port |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors |
|:--------------------|:---------------|:-----------------|-----------------:|---------:|----------------:|--------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|
| hardware-1-1-1-1-1  | hardware-1-1-1 | hardware-1-1-1-1 |                1 |        1 |               1 |       1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.04 |                               0.23 |                                0.27 |                              6749.86 |                                0.00 |        0 |
| hardware-1-1-2-1-1  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       1 |         65 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                              6359.14 |                                0.00 |        0 |
| hardware-1-1-2-1-2  | hardware-1-1-2 | hardware-1-1-2-1 |                1 |        2 |               1 |       2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                              6219.71 |                                0.00 |        0 |
| hardware-1-1-3-1-1  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       1 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.07 |                               0.04 |                               0.24 |                                0.28 |                              7489.42 |                                0.00 |        0 |
| hardware-1-1-3-1-2  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       2 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.09 |                               0.04 |                               0.25 |                                0.28 |                              5792.98 |                                0.00 |        0 |
| hardware-1-1-3-1-3  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       3 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.04 |                               0.03 |                               0.17 |                                0.25 |                             13741.78 |                                0.00 |        0 |
| hardware-1-1-3-1-4  | hardware-1-1-3 | hardware-1-1-3-1 |                1 |        3 |               1 |       4 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.09 |                               0.04 |                               0.25 |                                0.29 |                              5776.89 |                                0.00 |        0 |
| hardware-1-1-4-1-1  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       1 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.08 |                               0.04 |                               0.25 |                                0.29 |                              6597.88 |                                0.00 |        0 |
| hardware-1-1-4-1-2  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       2 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.05 |                               0.03 |                               0.23 |                                0.28 |                              9656.19 |                                0.00 |        0 |
| hardware-1-1-4-1-3  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       3 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.04 |                               0.03 |                               0.18 |                                0.24 |                             13907.59 |                                0.00 |        0 |
| hardware-1-1-4-1-4  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       4 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.07 |                               0.04 |                               0.25 |                                0.29 |                              7615.82 |                                0.00 |        0 |
| hardware-1-1-4-1-5  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       5 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.07 |                               0.04 |                               0.26 |                                0.29 |                              7217.13 |                                0.00 |        0 |
| hardware-1-1-4-1-6  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       6 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.07 |                               0.04 |                               0.25 |                                0.29 |                              6848.92 |                                0.00 |        0 |
| hardware-1-1-4-1-7  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       7 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.06 |                               0.04 |                               0.24 |                                0.28 |                              8930.63 |                                0.00 |        0 |
| hardware-1-1-4-1-8  | hardware-1-1-4 | hardware-1-1-4-1 |                1 |        4 |               1 |       8 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.08 |                               0.04 |                               0.25 |                                0.29 |                              6366.92 |                                0.00 |        0 |
| hardware-1-1-5-1-1  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       1 |         77 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20000 |                               0.06 |                               0.03 |                               0.27 |                                0.32 |                              8505.81 |                                0.00 |        0 |
| hardware-1-1-5-1-2  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       2 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20001 |                               0.06 |                               0.03 |                               0.27 |                                0.32 |                              8589.85 |                                0.00 |        0 |
| hardware-1-1-5-1-3  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       3 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20002 |                               0.08 |                               0.04 |                               0.29 |                                0.33 |                              6106.05 |                                0.00 |        0 |
| hardware-1-1-5-1-4  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       4 |         76 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20003 |                               0.05 |                               0.03 |                               0.27 |                                0.32 |                              9088.58 |                                0.00 |        0 |
| hardware-1-1-5-1-5  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       5 |         75 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20004 |                               0.04 |                               0.03 |                               0.25 |                                0.31 |                             11387.69 |                                0.00 |        0 |
| hardware-1-1-5-1-6  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       6 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20005 |                               0.10 |                               0.04 |                               0.29 |                                0.34 |                              5125.05 |                                0.00 |        0 |
| hardware-1-1-5-1-7  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       7 |         73 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20006 |                               0.07 |                               0.04 |                               0.29 |                                0.33 |                              6692.01 |                                0.00 |        0 |
| hardware-1-1-5-1-8  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       8 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20007 |                               0.07 |                               0.04 |                               0.27 |                                0.32 |                              6959.28 |                                0.00 |        0 |
| hardware-1-1-5-1-9  | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |       9 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20008 |                               0.08 |                               0.04 |                               0.29 |                                0.34 |                              5892.48 |                                0.00 |        0 |
| hardware-1-1-5-1-10 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      10 |         71 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20009 |                               0.11 |                               0.04 |                               0.30 |                                0.34 |                              4690.80 |                                0.00 |        0 |
| hardware-1-1-5-1-11 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      11 |         70 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20010 |                               0.07 |                               0.04 |                               0.28 |                                0.33 |                              7290.48 |                                0.00 |        0 |
| hardware-1-1-5-1-12 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      12 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20011 |                               0.05 |                               0.03 |                               0.25 |                                0.32 |                              9522.79 |                                0.00 |        0 |
| hardware-1-1-5-1-13 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      13 |         69 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20012 |                               0.09 |                               0.04 |                               0.29 |                                0.34 |                              5453.67 |                                0.00 |        0 |
| hardware-1-1-5-1-14 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      14 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20013 |                               0.08 |                               0.03 |                               0.29 |                                0.33 |                              6524.21 |                                0.00 |        0 |
| hardware-1-1-5-1-15 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      15 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20014 |                               0.04 |                               0.03 |                               0.20 |                                0.28 |                             13186.28 |                                0.00 |        0 |
| hardware-1-1-5-1-16 | hardware-1-1-5 | hardware-1-1-5-1 |                1 |        5 |               1 |      16 |         67 |                  0 | pp                       | tcp                          |                          64 | max                     |                    20015 |                               0.07 |                               0.04 |                               0.28 |                                0.32 |                              7618.00 |                                0.00 |        0 |

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count |   duration |   hardware_threads | hardware_sockperf_mode   | hardware_sockperf_protocol   |   hardware_sockperf_msgsize | hardware_sockperf_mps   |   hardware_sockperf_latency_avg_ms |   hardware_sockperf_latency_p50_ms |   hardware_sockperf_latency_p99_ms |   hardware_sockperf_latency_p999_ms |   hardware_sockperf_msg_rate_per_sec |   hardware_sockperf_dropped_per_sec |   errors | hardware_type   |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|-----------:|-------------------:|:-------------------------|:-----------------------------|----------------------------:|:------------------------|-----------------------------------:|-----------------------------------:|-----------------------------------:|------------------------------------:|-------------------------------------:|------------------------------------:|---------:|:----------------|
| hardware-1-1-1 | hardware-1-1-1 |                1 |        1 |               1 |           1 |         64 |                  1 | pp                       | tcp                          |                          64 | max                     |                               0.07 |                               0.04 |                               0.23 |                                0.27 |                              6749.86 |                                0.00 |        0 | sockperf        |
| hardware-1-1-2 | hardware-1-1-2 |                1 |        2 |               1 |           2 |         66 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.04 |                               0.24 |                                0.27 |                             12578.86 |                                0.00 |        0 | sockperf        |
| hardware-1-1-3 | hardware-1-1-3 |                1 |        3 |               1 |           4 |         68 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.09 |                               0.04 |                               0.25 |                                0.29 |                             32801.07 |                                0.00 |        0 | sockperf        |
| hardware-1-1-4 | hardware-1-1-4 |                1 |        4 |               1 |           8 |         72 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.08 |                               0.04 |                               0.26 |                                0.29 |                             67141.07 |                                0.00 |        0 | sockperf        |
| hardware-1-1-5 | hardware-1-1-5 |                1 |        5 |               1 |          16 |         77 |                  0 | pp                       | tcp                          |                          64 | max                     |                               0.11 |                               0.04 |                               0.30 |                                0.34 |                            122633.02 |                                0.00 |        0 | sockperf        |

### Monitoring

### Benchmarking phase: SUT deployment

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |         6.07 |      0.15 |           0.20 |                  0.20 |
| hardware-1-1-2-1 |        13.42 |      0.26 |           0.20 |                  0.20 |
| hardware-1-1-3-1 |        31.05 |      0.56 |           0.20 |                  0.20 |
| hardware-1-1-4-1 |        58.87 |      1.15 |           0.20 |                  0.20 |
| hardware-1-1-5-1 |       101.34 |      1.99 |           0.20 |                  0.20 |

### Benchmarking phase: component benchmarker

| DBMS             |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:-----------------|-------------:|----------:|---------------:|----------------------:|
| hardware-1-1-1-1 |        14.37 |      0.26 |           0.55 |                  0.55 |
| hardware-1-1-2-1 |        15.75 |      0.50 |           0.55 |                  0.55 |
| hardware-1-1-3-1 |        37.51 |      0.98 |           0.55 |                  0.55 |
| hardware-1-1-4-1 |        80.88 |      1.88 |           0.55 |                  0.55 |
| hardware-1-1-5-1 |       133.86 |      3.72 |           0.55 |                  0.55 |

### Missing Monitoring Metrics
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-1-1 (bexhoma-metrics-hardware-1-1-1-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-2-1 (bexhoma-metrics-hardware-1-1-2-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-3-1 (bexhoma-metrics-hardware-1-1-3-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-4-1 (bexhoma-metrics-hardware-1-1-4-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarker.log, expected: series exists only while non-zero)
* CPU Throttling Rate [s/s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)
* CPU Throttled Time [s] for connection hardware-1-1-5-1 (bexhoma-metrics-hardware-1-1-5-1-benchmarking.log, expected: series exists only while non-zero)

### Tests
* TEST passed: Loading measured in this experiment
* TEST passed: No SUT container restarts
* TEST skipped: SUT data survived container restarts (no restarts)
* TEST passed: Benchmarking phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Benchmarking phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Monitoring metrics missing (series exists only while non-zero)
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
usage: hardware.py [-h] [-aws] [-db] [-sl] [-ss] [-ar] [-cx CONTEXT]
                   [-e EXPERIMENT] [-m] [-ma] [-mc] [-mm MONITORING_METRICS]
                   [-ms MAX_SUT] [-mse MAX_SUT_EXPERIMENT]
                   [-et EXPERIMENT_TIMEOUT] [-lt LOADING_TIMEOUT]
                   [-nc NUM_CONFIG] [-ne NUM_QUERY_EXECUTORS] [-nw NUM_WORKER]
                   [-nwr NUM_WORKER_REPLICAS] [-nws NUM_WORKER_SHARDS]
                   [-nlp NUM_LOADING_PODS] [-nlt NUM_LOADING_THREADS]
                   [-nbp NUM_BENCHMARKING_PODS]
                   [-nbt NUM_BENCHMARKING_THREADS] [-sf SCALING_FACTOR]
                   [-t TIMEOUT] [-lr LIMIT_RAM] [-lc LIMIT_CPU]
                   [-rr REQUEST_RAM] [-rc REQUEST_CPU] [-rct REQUEST_CPU_TYPE]
                   [-rg REQUEST_GPU] [-rgt REQUEST_GPU_TYPE]
                   [-rst REQUEST_STORAGE_TYPE] [-rss REQUEST_STORAGE_SIZE]
                   [-rsr] [-rsrp] [-rnn [REQUEST_NODE_NAME]]
                   [-rnl [REQUEST_NODE_LOADING]]
                   [-rnb [REQUEST_NODE_BENCHMARKING]]
                   [-rnp [REQUEST_NODE_POOLING]] [-mtn MULTI_TENANT_NUM]
                   [-mtb MULTI_TENANT_BY] [-mtv] [-tr] [-rp] [--set SETS]
                   [-dbms [{Hardware} ...]]
                   [-xht {fio,sysbench,sockperf,netperf}] [-xts HARDWARE_SIZE]
                   [-xtd HARDWARE_DURATION] [-xfrw FIO_RW] [-xfbs FIO_BS]
                   [-xfid FIO_IODEPTH] [-xfe FIO_ENGINE] [-xfsy FIO_FSYNC]
                   [-xffd FIO_FDATASYNC] [-xfmx FIO_RWMIXREAD]
                   [-xfow FIO_OVERWRITE] [-xspm SOCKPERF_MODE] [-xspr SOCKPERF_MPS]
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
  -ar, --activate-reset
                        activate configured reset scripts (e.g.
                        CHECKPOINT/VACUUM) when set on a benchmarker entry;
                        off by default
  -cx, --context CONTEXT
                        kubectl context to use (default: current context)
  -e, --experiment EXPERIMENT
                        resume an existing experiment by its code
  -m, --monitoring      enable Prometheus monitoring for the SUT
  -ma, --monitoring-app
                        enable application-level metrics collection
  -mc, --monitoring-cluster
                        enable node-level monitoring for the entire cluster
  -mm, --monitoring-metrics MONITORING_METRICS
                        switch single cluster-wide hardware metrics of
                        cluster.config on or off for this experiment,
                        overriding their 'active' flag, e.g.
                        total_gpu_util=on,total_network_rx=off; needs -m or
                        -mc
  -ms, --max-sut MAX_SUT
                        maximum number of DBMS configurations to run in
                        parallel cluster-wide (default: no limit)
  -mse, --max-sut-experiment MAX_SUT_EXPERIMENT
                        maximum number of DBMS configurations in this
                        experiment to run in parallel (default: no limit)
  -et, --experiment-timeout EXPERIMENT_TIMEOUT
                        maximum wall-clock duration of the experiment in
                        minutes; when exceeded, the experiment is stopped and
                        all its components are removed from the cluster
                        (default: no limit)
  -lt, --loading-timeout LOADING_TIMEOUT
                        maximum loading duration per configuration in minutes;
                        captures diagnostics and removes the experiment when
                        exceeded (default: no limit)
  -nc, --num-config NUM_CONFIG
                        number of experiment repetitions per configuration
  -ne, --num-query-executors NUM_QUERY_EXECUTORS
                        comma-separated list of parallel client counts to
                        sweep
  -nw, --num-worker NUM_WORKER
                        number of worker nodes for distributed DBMS
  -nwr, --num-worker-replicas NUM_WORKER_REPLICAS
                        number of replicas per worker node
  -nws, --num-worker-shards NUM_WORKER_SHARDS
                        number of shards per worker node
  -nlp, --num-loading-pods NUM_LOADING_PODS
                        comma-separated list of total loader pod counts
  -nlt, --num-loading-threads NUM_LOADING_THREADS
                        comma-separated list of total loader threads (split
                        across pods)
  -nbp, --num-benchmarking-pods NUM_BENCHMARKING_PODS
                        comma-separated list of benchmarker pod counts
  -nbt, --num-benchmarking-threads NUM_BENCHMARKING_THREADS
                        total benchmarking threads, split evenly across pods
  -sf, --scaling-factor SCALING_FACTOR
                        scaling factor controlling dataset size
  -t, --timeout TIMEOUT
                        per-query timeout in seconds
  -lr, --limit-ram LIMIT_RAM
                        RAM limit for the SUT and worker pods (e.g. 64Gi; 0 =
                        no limit); comma-separated to sweep several settings
                        (e.g. 32Gi,64Gi), one configuration per entry
  -lc, --limit-cpu LIMIT_CPU
                        CPU limit for the SUT and worker pods (e.g. 4; 0 = no
                        limit); comma-separated to sweep, must then match the
                        length of any other swept resource list
  -rr, --request-ram REQUEST_RAM
                        RAM request for the SUT and worker pods (e.g. 16Gi);
                        comma-separated to sweep several settings (e.g.
                        32Gi,64Gi), one configuration per entry
  -rc, --request-cpu REQUEST_CPU
                        CPU request for the SUT and worker pods (e.g. 4);
                        comma-separated to sweep, must then match the length
                        of any other swept resource list
  -rct, --request-cpu-type REQUEST_CPU_TYPE
                        require SUT node to carry label cpu=<value>
  -rg, --request-gpu REQUEST_GPU
                        number of GPUs to request for the SUT pod
  -rgt, --request-gpu-type REQUEST_GPU_TYPE
                        require SUT node to carry label gpu=<value>
  -rst, --request-storage-type REQUEST_STORAGE_TYPE
                        storage class for the SUT persistent volume ('' or
                        unset = ephemeral, 'ramdisk' = in-memory; other values
                        must be declared for the active cluster context, see
                        cluster config 'storage_classes'); comma-separated to
                        sweep the class, one configuration per entry and
                        paired by position with -rc/-lc/-rr/-lr, an empty
                        entry meaning ephemeral
  -rss, --request-storage-size REQUEST_STORAGE_SIZE
                        size of the SUT persistent volume (e.g. 10Gi)
  -rsr, --request-storage-remove
                        delete any existing PVC for the SUT before starting
  -rsrp, --request-storage-remove-per-repetition
                        delete the PVC of the SUT before every repetition
                        (-nc), so each repetition loads into a fresh volume;
                        implies -rsr
  -rnn, --request-node-name [REQUEST_NODE_NAME]
                        pin the SUT pod to this Kubernetes node
  -rnl, --request-node-loading [REQUEST_NODE_LOADING]
                        pin loader pods to this Kubernetes node
  -rnb, --request-node-benchmarking [REQUEST_NODE_BENCHMARKING]
                        pin benchmarker pods to this Kubernetes node
  -rnp, --request-node-pooling [REQUEST_NODE_POOLING]
                        pin pooling pods to this Kubernetes node
  -mtn, --multi-tenant-num MULTI_TENANT_NUM
                        number of tenants for multi-tenant experiments
  -mtb, --multi-tenant-by MULTI_TENANT_BY
                        tenancy granularity: schema, database, or container
  -mtv, --multi-tenant-volume
                        allocate a separate persistent volume per tenant
  -tr, --test-result    validate that results meet basic correctness
                        requirements
  -rp, --report         also write a tiered Markdown summary report
                        (report/index.md + detail files) to the result folder
  --set SETS            override a deployment parameter, e.g.
                        deployment[bexhoma-deployment-postgres].container[dbms].
                        max_worker_processes=128
  -dbms, --dbms [{Hardware} ...]
                        hardware target(s) to test
  -xht, --xhardware-type {fio,sysbench,sockperf,netperf}
                        benchmark tool: fio (disk I/O), sysbench (CPU/memory),
                        sockperf (single-connection network
                        latency/throughput), or netperf (many-concurrent-
                        connection request/response)
  -xts, --xtest-size HARDWARE_SIZE
                        fio test file size (e.g. 1G, 64G)
  -xtd, --xtest-duration HARDWARE_DURATION
                        fio/sysbench/sockperf run duration in seconds
  -xfrw, --xfio-rw FIO_RW
                        comma-separated fio I/O patterns to sweep, each in
                        {write, read, randwrite, randread, randrw}
  -xfbs, --xfio-blocksize FIO_BS
                        comma-separated fio block sizes to sweep (e.g.
                        4k,64k,1M)
  -xfid, --xfio-iodepth FIO_IODEPTH
                        comma-separated fio queue depths to sweep
  -xfe, --xfio-engine FIO_ENGINE
                        comma-separated fio ioengines to sweep, each in {sync,
                        libaio, io_uring}
  -xfsy, --xfio-fsync FIO_FSYNC
                        comma-separated fsync intervals to sweep (0 disables
                        fsync); use fsync xor fdatasync, not both
  -xffd, --xfio-fdatasync FIO_FDATASYNC
                        comma-separated fdatasync intervals to sweep (0
                        disables fdatasync); use fsync xor fdatasync, not both
  -xfmx, --xfio-rwmixread FIO_RWMIXREAD
                        comma-separated read percentages to sweep when
                        -xfrw=randrw
  -xfow, --xfio-overwrite FIO_OVERWRITE
                        comma-separated overwrite modes to sweep, each in {0,
                        1}: 1 lays out (fully writes) the test file before the
                        timed run, so writes go into allocated blocks like
                        PostgreSQL WAL or existing relation files; 0 writes
                        into a fresh file like table growth during a bulk load
  -xspm, --xsockperf-mode SOCKPERF_MODE
                        comma-separated sockperf modes to sweep, each in {pp,
                        ul}
  -xspr, --xsockperf-mps SOCKPERF_MPS
                        comma-separated message rates to sweep (messages/sec);
                        each value is a positive integer or the literal "max"
  -xsps, --xsockperf-msgsize SOCKPERF_MSGSIZE
                        comma-separated message payload sizes in bytes to
                        sweep
  -xspp, --xsockperf-protocol SOCKPERF_PROTOCOL
                        comma-separated sockperf protocols to sweep, each in
                        {tcp, udp}
  -xnpp, --xnetperf-protocol NETPERF_PROTOCOL
                        comma-separated netperf protocols to sweep, each in
                        {tcp, udp} (selects TCP_RR/UDP_RR)
```
