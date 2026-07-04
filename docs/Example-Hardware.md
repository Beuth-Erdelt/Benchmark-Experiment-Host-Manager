# Benchmark: Hardware

`Hardware` is not a DBMS benchmark — it runs [fio](https://fio.readthedocs.io/) (disk I/O) or
[sysbench](https://github.com/akopytov/sysbench) (CPU/memory) directly against a dedicated SUT
container over SSH, bypassing any database engine entirely. There is no data loading phase and
no `-dbms` engine choice beyond the single `Hardware` target (see [DBMS.md](DBMS.md#hardware)).

The purpose of these benchmarks is not to rank hardware, but to **calibrate DBMS configuration**
against the actual storage a cluster provides — for example finding the queue depth
[PostgreSQL](https://www.postgresql.org/)'s `effective_io_concurrency` should target, a realistic
`random_page_cost`, or the raw fsync latency that bounds commit throughput under
`synchronous_commit=on`. This page walks through the fio sweeps in
[`scripts/test-docs-hardware.ps1`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/test-docs-hardware.ps1)
and explains what each one is for (unlike most other benchmarks in this repo, there is no `.sh`
twin of this script yet).

**The results are not official benchmark results.
Exact performance depends on a number of parameters, including the underlying storage class,
node hardware, and cluster load at the time of the run.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

Result tables below are real output from an actual cluster run of every command on this page —
including a couple of surprises (an inverted `random_page_cost` signal, a reproducible all-zero
anomaly at `numjobs=16`) that are called out rather than smoothed over, and a caveat where two
commands landed on different cluster nodes and so aren't directly comparable in absolute terms.

References:
1. fio documentation: https://fio.readthedocs.io/en/latest/fio_doc.html
1. fio `--fsync` / `--fdatasync`: https://fio.readthedocs.io/en/latest/fio_doc.html#cmdoption-arg-fsync
1. PostgreSQL WAL configuration: https://www.postgresql.org/docs/current/wal-configuration.html
1. PostgreSQL `effective_io_concurrency`: https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY

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
before benchmarking, so every command below goes straight to `run`. All twelve commands share
the same `Hardware-1` SUT/PVC and run **sequentially**; two `hardware.py run` invocations must
never overlap in time, because the PVC name is fixed (`storage_label='hardware'`, not scoped by
experiment code) and a second SUT pod would either fail to attach the volume or silently write
into the same test-file path as the first (see the project notes on `-rsr` and PVC sharing).

The fio workload flags (`-xfrw`, `-xfbs`, `-xfid`, `-xfe`, `-xfsy`, `-xffd`, `-xfmx`) each accept
a comma-separated list. Every combination across the lists is run as one more sequential round
against the same SUT, so a parameter sweep is expressed as a single invocation instead of one
process per value — see `python hardware.py -h` at the bottom of this page.

---

## 1. Queue-depth sweep

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
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
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2281s 
* Code: 1783105778
* fio/sysbench driver runs the experiment.
* This experiment measures raw hardware I/O (fio) or CPU/memory (sysbench) performance.
  * Benchmark tool: fio.
  * Test file size is '4G', duration per round is 60s.
  * I/O pattern(s) swept: ['randread', 'randwrite'].
  * Block size(s) swept: ['4k'].
  * Queue depth(s) swept: [1, 2, 4, 8, 16, 32, 64, 128].
  * I/O engine(s) swept: ['libaio'].
  * Fsync interval(s) swept: [0].
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
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:4.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (16 connections total, one per queue-depth × pattern round, all on the same SUT pod)

### Execution

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                      1 | libaio                |                    0 |                       50 |                     8.82 |                      0.00 |                         135.27 |                            0.00 |                        1753.22 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                      2 | libaio                |                    0 |                       50 |                    30.20 |                      0.00 |                         130.55 |                            0.00 |                        1317.01 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                      4 | libaio                |                    0 |                       50 |                    53.70 |                      0.00 |                         137.36 |                            0.00 |                         759.17 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                      8 | libaio                |                    0 |                       50 |                    96.02 |                      0.00 |                         135.27 |                            0.00 |                         960.50 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                     16 | libaio                |                    0 |                       50 |                    76.75 |                      0.00 |                         137.36 |                            0.00 |                        1786.77 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 4k                |                     32 | libaio                |                    0 |                       50 |                   146.35 |                      0.00 |                         177.21 |                            0.00 |                        6207.57 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                       50 |                   211.70 |                      0.00 |                         404.75 |                            0.00 |                        8925.48 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randread          | 4k                |                    128 | libaio                |                    0 |                       50 |                  1336.25 |                      0.00 |                         133.69 |                            0.00 |                        3271.56 |                            0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                      1 | libaio                |                    0 |                       50 |                     0.00 |                     21.49 |                           0.00 |                          193.99 |                           0.00 |                          700.45 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                      2 | libaio                |                    0 |                       50 |                     0.00 |                     52.47 |                           0.00 |                          158.33 |                           0.00 |                          574.62 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 4k                |                      4 | libaio                |                    0 |                       50 |                     0.00 |                    187.05 |                           0.00 |                           73.92 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 4k                |                      8 | libaio                |                    0 |                       50 |                     0.00 |                    307.33 |                           0.00 |                           90.70 |                           0.00 |                          312.48 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 4k                |                     16 | libaio                |                    0 |                       50 |                     0.00 |                    584.94 |                           0.00 |                          103.28 |                           0.00 |                          316.67 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 4k                |                     32 | libaio                |                    0 |                       50 |                     0.00 |                    898.88 |                           0.00 |                          107.48 |                           0.00 |                          383.78 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                       50 |                     0.00 |                   1573.27 |                           0.00 |                          137.36 |                           0.00 |                          522.19 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                       50 |                     0.00 |                   2276.72 |                           0.00 |                          168.82 |                           0.00 |                          926.94 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

**Reading the curve**: IOPS scales roughly 2× per doubling of depth through 64
(`randwrite`: 22→52→187→307→585→899→1573 across depths 1→64), but the 64→128 step is sublinear
(1573→2277, only 1.45×) while `randwrite` p99 latency jumps from ~522ms to ~927ms at the same
step, and `randread` p99 spikes even harder (8925ms → 3272ms is noisy, but the depth=64 point
itself already shows p99 climbing to nearly 9s). That combination — throughput plateauing while
tail latency rises — is the elbow: on this storage it sits around queue depth 64, not 128.

---

## 2. Depth-sweep refinement around the elbow

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_refine.log
```

10 rounds (2 patterns × 5 depths) ≈ 10 minutes.

### Result

docs_hardware_fio_depth_sweep_refine.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1389s 
* Code: 1783118630
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * node:cl-worker37
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (10 connections total, one per queue-depth × pattern round)

### Execution

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5098.45 |                      0.00 |                          33.42 |                            0.00 |                         143.65 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                  8719.86 |                      0.00 |                          27.39 |                            0.00 |                         132.64 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                  9583.97 |                      0.00 |                          39.06 |                            0.00 |                         173.02 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                 11924.60 |                      0.00 |                          28.97 |                            0.00 |                         149.95 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  6462.60 |                      0.00 |                          52.69 |                            0.00 |                         522.19 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1729.36 |                           0.00 |                          141.56 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randwrite         | 4k                |                     80 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2011.50 |                           0.00 |                          149.95 |                           0.00 |                          379.58 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     96 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2260.57 |                           0.00 |                          166.72 |                           0.00 |                          497.03 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                    112 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2607.39 |                           0.00 |                          170.92 |                           0.00 |                          574.62 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2481.92 |                           0.00 |                          185.60 |                           0.00 |                          708.84 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

**Important caveat**: this run landed on `cl-worker37` (Xeon Gold 6438Y+), while the coarse depth
sweep above landed on `cl-worker36` (Xeon Platinum 8570) — a different node behind the same
`shared` storage class. That alone likely explains why depth=64 shows ~5098 randread IOPS here
versus ~212 IOPS in the coarse sweep — the two runs are not directly comparable. `-rnn` pins the
SUT to a specific node when set explicitly; if you want sweeps to be comparable, pin all of them
to the same node rather than relying on the scheduler's default choice.

Within *this* run, `randwrite` still shows the sublinear-throughput / rising-latency signature
between 96 and 128 (2261→2607→2482 IOPS, not monotonic; p99 keeps climbing 497→575→709ms),
suggesting the elbow on this node sits closer to 96-112 rather than 64. `randread` keeps climbing
all the way to 112 before dropping at 128, which is more consistent with a device/queue
saturation point than a clean plateau — worth a third, even finer pass if you need a precise
number for this specific node.

---

## 3. Numjobs sweep at fixed queue depth (elbow check)

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_numjobs_sweep.log
```

An earlier attempt at this command hit a bug in
`evaluators/hardware.py::benchmarking_set_datatypes()`: a read-only or write-only fio round left
the opposing direction's result columns blank, and casting a blank string to `float` raised an
exception before the summary could be printed. That is now fixed (blanks are treated as 0 before
casting), and the re-run below completed.

### Result

docs_hardware_fio_numjobs_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1388s 
* Code: 1783115274
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1, 2, 4, 8, 16] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * node:cl-worker37
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (10 connections total, one per numjobs × pattern round)

### Execution

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3926.64 |                      0.00 |                          29.49 |                            0.00 |                         101.19 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  6279.35 |                      0.00 |                          57.41 |                            0.00 |                         354.42 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3984.66 |                      0.00 |                         108.53 |                            0.00 |                        2164.26 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  4114.35 |                      0.00 |                         371.20 |                            0.00 |                        3472.88 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3826.61 |                      0.00 |                         734.00 |                            0.00 |                        5268.05 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1604.06 |                           0.00 |                          149.95 |                           0.00 |                          371.20 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2170.72 |                           0.00 |                          206.57 |                           0.00 |                          901.78 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1988.53 |                           0.00 |                          240.12 |                           0.00 |                         3036.68 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2858.75 |                           0.00 |                          591.40 |                           0.00 |                         3707.76 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

**Anomaly**: the `numjobs=16` round (`Hardware-1-1-10`, last row) reports exactly zero for every
metric despite `errors=0` and all tests passing — the round completed without an explicit error
but fio produced no usable result for it. The same numjobs=16 point shows the identical all-zero
pattern in the group-commit sweep below (command 9), so this looks like a reproducible issue at
that specific concurrency level on this cluster (a resource limit inside the benchmarker
container is a plausible cause), not one-off noise. Treat any numjobs=16 datapoint on this
cluster with suspicion until investigated.

Setting that aside, `randread` throughput does **not** keep climbing with more threads at fixed
depth 64 — it stays in the 3800-6300 IOPS range across 1, 2, 4, 8 threads with no clear trend,
while p99 latency rises steadily (101→354→2164→3473→5268ms). `randwrite` throughput does grow
with thread count (1604→2171→1989→2859, noisy but trending up) while its own p99 latency also
balloons (371→902→3037→3708ms). Read together, more threads at the same depth mostly buys
latency, not much extra throughput — consistent with 64 already being close to this node's real
device ceiling rather than a per-queue submission limit.

---

## 4. Block-size sweep at fixed queue depth (throughput curve)

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_blocksize_sweep.log
```

### Result

docs_hardware_fio_blocksize_sweep.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 1915s 
* Code: 1783116687
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (14 connections total, one per block-size × pattern round)

### Execution

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3351.79 |                      0.00 |                          43.78 |                            0.00 |                         152.04 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3020.85 |                      0.00 |                          45.88 |                            0.00 |                         181.40 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  3394.22 |                      0.00 |                          57.41 |                            0.00 |                         240.12 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                  7386.03 |                      0.00 |                          33.82 |                            0.00 |                         120.06 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  8507.16 |                      0.00 |                          30.80 |                            0.00 |                         107.48 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                  4715.52 |                      0.00 |                          61.60 |                            0.00 |                         223.35 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                  2304.79 |                      0.00 |                         117.96 |                            0.00 |                         518.00 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randwrite         | 4k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2080.16 |                           0.00 |                          141.56 |                           0.00 |                          287.31 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2536.05 |                           0.00 |                          101.19 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 16k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2361.70 |                           0.00 |                          106.43 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 64k               |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1827.37 |                           0.00 |                          104.33 |                           0.00 |                          219.15 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 128k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1657.47 |                           0.00 |                          107.48 |                           0.00 |                          252.71 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 256k              |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1435.64 |                           0.00 |                          124.26 |                           0.00 |                          235.93 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 1M                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    865.35 |                           0.00 |                          198.18 |                           0.00 |                          320.86 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

`randread` IOPS peak at 128k (8507) and drop off at 256k/1M (2305 at 1M) — the classic
IOPS-bound → bandwidth-bound crossover: effective bandwidth (IOPS × block size) keeps rising past
that point even as IOPS falls (128k@8507 ≈ 1.04GB/s, 1M@2305 ≈ 2.25GB/s), so the workload has
shifted from being limited by request rate to being limited by raw throughput. `randwrite` IOPS
instead falls off monotonically as block size grows (2080→2536→2362→1827→1657→1436→865) with no
peak — writes on this storage are IOPS-bound across the whole range tested here.

---

## 5. Depth sweep at PostgreSQL's page size (8k)

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_depth_sweep_8k.log
```

### Result

docs_hardware_fio_depth_sweep_8k.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 2200s 
* Code: 1783120041
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (16 connections total, one per queue-depth × pattern round)

### Execution

#### Per Phase

| DBMS            | phase           |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:----------------|:----------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1  | Hardware-1-1-1  |                1 |        1 |               1 |           1 | randread          | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                    61.41 |                      0.00 |                          35.91 |                            0.00 |                          94.90 |                            0.00 |        0 |
| Hardware-1-1-2  | Hardware-1-1-2  |                1 |        2 |               1 |           1 | randread          | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                   149.89 |                      0.00 |                          33.42 |                            0.00 |                          96.99 |                            0.00 |        0 |
| Hardware-1-1-3  | Hardware-1-1-3  |                1 |        3 |               1 |           1 | randread          | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                   374.10 |                      0.00 |                          28.97 |                            0.00 |                          85.46 |                            0.00 |        0 |
| Hardware-1-1-4  | Hardware-1-1-4  |                1 |        4 |               1 |           1 | randread          | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                   858.62 |                      0.00 |                          26.35 |                            0.00 |                          82.31 |                            0.00 |        0 |
| Hardware-1-1-5  | Hardware-1-1-5  |                1 |        5 |               1 |           1 | randread          | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                  1990.59 |                      0.00 |                          21.36 |                            0.00 |                          74.97 |                            0.00 |        0 |
| Hardware-1-1-6  | Hardware-1-1-6  |                1 |        6 |               1 |           1 | randread          | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                  3202.98 |                      0.00 |                          31.85 |                            0.00 |                          99.09 |                            0.00 |        0 |
| Hardware-1-1-7  | Hardware-1-1-7  |                1 |        7 |               1 |           1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  5124.44 |                      0.00 |                          47.45 |                            0.00 |                         170.92 |                            0.00 |        0 |
| Hardware-1-1-8  | Hardware-1-1-8  |                1 |        8 |               1 |           1 | randread          | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                  6655.83 |                      0.00 |                          63.18 |                            0.00 |                         463.47 |                            0.00 |        0 |
| Hardware-1-1-9  | Hardware-1-1-9  |                1 |        9 |               1 |           1 | randwrite         | 8k                |                      1 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     91.12 |                           0.00 |                           40.11 |                           0.00 |                           93.85 |        0 |
| Hardware-1-1-10 | Hardware-1-1-10 |                1 |       10 |               1 |           1 | randwrite         | 8k                |                      2 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    164.24 |                           0.00 |                           45.35 |                           0.00 |                          102.24 |        0 |
| Hardware-1-1-11 | Hardware-1-1-11 |                1 |       11 |               1 |           1 | randwrite         | 8k                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    287.73 |                           0.00 |                           48.50 |                           0.00 |                          114.82 |        0 |
| Hardware-1-1-12 | Hardware-1-1-12 |                1 |       12 |               1 |           1 | randwrite         | 8k                |                      8 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    515.01 |                           0.00 |                           54.26 |                           0.00 |                          120.06 |        0 |
| Hardware-1-1-13 | Hardware-1-1-13 |                1 |       13 |               1 |           1 | randwrite         | 8k                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    907.01 |                           0.00 |                           61.08 |                           0.00 |                          160.43 |        0 |
| Hardware-1-1-14 | Hardware-1-1-14 |                1 |       14 |               1 |           1 | randwrite         | 8k                |                     32 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   1419.89 |                           0.00 |                           80.22 |                           0.00 |                          214.96 |        0 |
| Hardware-1-1-15 | Hardware-1-1-15 |                1 |       15 |               1 |           1 | randwrite         | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2013.53 |                           0.00 |                          109.58 |                           0.00 |                          400.56 |        0 |
| Hardware-1-1-16 | Hardware-1-1-16 |                1 |       16 |               1 |           1 | randwrite         | 8k                |                    128 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                   2267.28 |                           0.00 |                          135.27 |                           0.00 |                          851.44 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

Same node as the original 4k sweep (`cl-worker36`), so this is directly comparable to it.
`randread` climbs smoothly all the way to 128 (61→150→374→859→1991→3203→5124→6656 IOPS) with no
plateau yet — at 8k the read elbow for this node/storage sits beyond depth 128, higher than the
4k sweep suggested. `randwrite`, on the other hand, clearly flattens between 64 and 128
(2014→2267 IOPS, only 1.13× for a 2× depth increase) while p99 latency more than doubles
(401→851ms) — the write-side elbow at 8k lands in the same place (~64) as it did at 4k, so
`effective_io_concurrency`/`maintenance_io_concurrency` values derived from the write-heavy part
of the original 4k sweep still hold at the real page size; the read-side number should probably
be revisited with depths beyond 128 if reads dominate your workload.

---

## 6. `random_page_cost` calibration

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_random_page_cost.log
```

### Result

docs_hardware_fio_random_page_cost.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 339s 
* Code: 1783122269
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (2 connections total, one per pattern round)

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | read              | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  3296.15 |                      0.00 |                          44.30 |                            0.00 |                         185.60 |                            0.00 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | randread          | 8k                |                     64 | libaio                |                    0 |                        0 |                       50 |                  6456.66 |                      0.00 |                          35.39 |                            0.00 |                         141.56 |                            0.00 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

**Surprising result**: sequential read is *slower* than random read on this storage — 3296 IOPS
sequential vs. 6457 IOPS random, and p99 latency is worse for sequential too (186ms vs. 142ms).
This is the opposite of the assumption `random_page_cost > seq_page_cost` is built on. It's not
unusual for network-attached/distributed storage (the `shared` storage class here): a single
sequential stream at depth 64 may hit fewer backend paths than a random workload's depth-64
requests, which fan out and parallelize across more of the backend. Taken at face value, this
data argues for setting `random_page_cost` **at or below** `seq_page_cost` on this cluster's
`shared` class, rather than the classic 4.0 default aimed at spinning disks — the opposite of
what the "default" tuning advice usually says, and a good illustration of why this needs
measuring per storage class rather than assuming.

---

## 7. WAL sync-write latency (fsync)

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fsync.log
```

### Result

docs_hardware_fio_wal_sync_fsync.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 171s 
* Code: 1783122632
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
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    123.40 |                           0.00 |                           33.42 |                           0.00 |                           71.83 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

123.4 sustained fsync'd 8k writes/sec, p99 latency 71.83ms. With `synchronous_commit=on` and no
group commit, that's an upper bound of roughly **123 commits/sec** for a single backend on this
storage — compare against command 8 below for the `fdatasync` variant.

---

## 8. WAL sync-write latency (fdatasync)

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_sync_fdatasync.log
```

### Result

docs_hardware_fio_wal_sync_fdatasync.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 173s 
* Code: 1783122827
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    0 |                        1 |                       50 |                     0.00 |                    122.30 |                           0.00 |                           33.42 |                           0.00 |                           61.60 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

122.3 IOPS vs. fsync's 123.4 — essentially identical sustained throughput, but p99 latency is
about 14% lower (61.60ms vs. 71.83ms). On this storage `fdatasync` gives a modestly better tail
latency for the same steady-state rate, consistent with it skipping the inode-metadata sync that
`fsync` performs — a small but real reason to confirm `wal_sync_method=fdatasync` (Postgres'
Linux default) rather than switching to `fsync`.

---

## 9. WAL group-commit scaling

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_group_commit.log
```

### Result

docs_hardware_fio_wal_group_commit.log
```markdown
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
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:50.0G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (6 connections total, one per backend-count round)

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    120.28 |                           0.00 |                           38.54 |                           0.00 |                           81.26 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    153.31 |                           0.00 |                           54.79 |                           0.00 |                          139.46 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    408.90 |                           0.00 |                           48.50 |                           0.00 |                          106.43 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    752.88 |                           0.00 |                           50.07 |                           0.00 |                          107.48 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                      0.00 |                           0.00 |                            0.00 |                           0.00 |                            0.00 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                   2308.15 |                           0.00 |                           66.85 |                           0.00 |                          127.40 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

Row 5 (`numjobs=16`) is the same all-zero anomaly flagged in command 3 — same concurrency level,
same symptom, on the same cluster. Setting that row aside, aggregate fsync'd write throughput
keeps climbing all the way to 32 concurrent writers with no sign of flattening (120→153→409→753,
skip, →2308 IOPS) — nearly 19× the single-writer rate at 32 backends. That is a strong signal
that this storage/controller coalesces concurrent commits well, so `commit_delay`/
`commit_siblings` tuning to force artificial batching is unlikely to help here — the storage
already does it.

---

## 10. WAL record-size sweep

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_wal_record_size.log
```

### Result

docs_hardware_fio_wal_record_size.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 708s 
* Code: 1783123891
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:1081853939712
  * CPU:Intel(R) Xeon(R) Gold 6438Y+
  * Cores:128
  * node:cl-worker37
  * volume_size:50.0G
  * volume_used:48.6G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (5 connections total, one per record-size round)

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 1k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    139.97 |                           0.00 |                           38.01 |                           0.00 |                           78.12 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | write             | 8k                |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                    120.23 |                           0.00 |                           34.34 |                           0.00 |                           74.97 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 | write             | 16k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     78.76 |                           0.00 |                           47.97 |                           0.00 |                           95.94 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 | write             | 32k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     80.55 |                           0.00 |                           47.97 |                           0.00 |                          111.67 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 | write             | 64k               |                      1 | libaio                |                    1 |                        0 |                       50 |                     0.00 |                     49.40 |                           0.00 |                           68.68 |                           0.00 |                          129.50 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

Sync-write throughput falls and p99 latency rises steadily as the record size grows
(140→120→79→81→49 IOPS; 78→75→96→112→130ms p99, 1k through 64k) — bigger WAL records (or
post-checkpoint `full_page_writes` bursts that write a full 8k page instead of a delta) cost
proportionally more commit latency on this storage. Note this ran on `cl-worker37`, not
`cl-worker36`, so the 8k point here (120 IOPS) isn't directly comparable in absolute terms to
command 7's 8k fsync result (123 IOPS on `cl-worker36`) — though the two happen to be close in
this case.

---

## 11. Checkpoint writeback bandwidth

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_checkpoint_writeback.log
```

### Result

docs_hardware_fio_checkpoint_writeback.log
```markdown
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
  * node:cl-worker37
  * volume_size:50.0G
  * volume_used:48.6G
  * requests_cpu:4
  * requests_memory:16Gi
* ... (6 connections total, one per block-size × depth round)

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | write             | 1M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     49.09 |                           0.00 |                          238.03 |                           0.00 |                          484.44 |        0 |
| Hardware-1-1-2 | Hardware-1-1-2 |                1 |        2 |               1 |           1 | write             | 1M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                    123.78 |                           0.00 |                          379.58 |                           0.00 |                         1115.68 |        0 |
| Hardware-1-1-3 | Hardware-1-1-3 |                1 |        3 |               1 |           1 | write             | 4M                |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     28.86 |                           0.00 |                          350.22 |                           0.00 |                         1061.16 |        0 |
| Hardware-1-1-4 | Hardware-1-1-4 |                1 |        4 |               1 |           1 | write             | 4M                |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     91.54 |                           0.00 |                          371.20 |                           0.00 |                         2164.26 |        0 |
| Hardware-1-1-5 | Hardware-1-1-5 |                1 |        5 |               1 |           1 | write             | 16M               |                      4 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     13.66 |                           0.00 |                          826.28 |                           0.00 |                         2499.81 |        0 |
| Hardware-1-1-6 | Hardware-1-1-6 |                1 |        6 |               1 |           1 | write             | 16M               |                     16 | libaio                |                    0 |                        0 |                       50 |                     0.00 |                     20.85 |                           0.00 |                         1686.11 |                           0.00 |                        14831.06 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

Converting IOPS to bandwidth (IOPS × block size): 1M@depth4 ≈ 49MB/s → depth16 ≈ 124MB/s;
4M@depth4 ≈ 115MB/s → depth16 ≈ 366MB/s; 16M@depth4 ≈ 219MB/s → depth16 ≈ 334MB/s. Sustained
writeback bandwidth tops out in the 330-370MB/s range around 4M-16M blocks at depth 16 — that's
roughly the ceiling checkpointer/bgwriter can push on this storage without help from more
parallelism. The 16M/depth16 combination also has a striking p99 latency of nearly 14.8 seconds
(vs. ~2.5s at depth 4) — pushing both block size and depth that far starts queuing far more data
than the storage can drain promptly, which is exactly the failure mode
`checkpoint_completion_target` is meant to avoid by spreading writeback over more of the
checkpoint interval instead of bursting it.

---

## 12. OLTP/WAL contention proxy

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
  -rst $BEXHOMA_STORAGE_CLASS \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_hardware_fio_oltp_wal_contention_proxy.log
```

### Result

docs_hardware_fio_oltp_wal_contention_proxy.log
```markdown
## Show Summary

### Workload
Hardware Benchmark (fio)
* Type: hardware
* Duration: 205s 
* Code: 1783125493
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
  * Database is persisted to disk of type shared and size 50Gi.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.

### Connections
* Hardware-1-1-1-1 uses docker image bexhoma/sut_hardware:0.10.2
  * RAM:2164173246464
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * node:cl-worker36
  * volume_size:50.0G
  * volume_used:48.6G
  * requests_cpu:4
  * requests_memory:16Gi

### Execution

#### Per Phase

| DBMS           | phase          |   experiment_run |   client |   benchmark_run |   pod_count | hardware_fio_rw   | hardware_fio_bs   |   hardware_fio_iodepth | hardware_fio_engine   |   hardware_fio_fsync |   hardware_fio_fdatasync |   hardware_fio_rwmixread |   hardware_fio_read_iops |   hardware_fio_write_iops |   hardware_fio_read_lat_p95_ms |   hardware_fio_write_lat_p95_ms |   hardware_fio_read_lat_p99_ms |   hardware_fio_write_lat_p99_ms |   errors |
|:---------------|:---------------|-----------------:|---------:|----------------:|------------:|:------------------|:------------------|-----------------------:|:----------------------|---------------------:|-------------------------:|-------------------------:|-------------------------:|--------------------------:|-------------------------------:|--------------------------------:|-------------------------------:|--------------------------------:|---------:|
| Hardware-1-1-1 | Hardware-1-1-1 |                1 |        1 |               1 |           1 | randrw            | 8k                |                     64 | libaio                |                    1 |                        0 |                       70 |                   877.40 |                    375.88 |                         103.28 |                          196.08 |                        1052.77 |                         1149.24 |        0 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Workflow as planned
```

The read/write split (877/376 ≈ 70/30) matches the requested mix, confirming the round ran as
configured. Compare the read side against the isolated `randread` result at the same depth and
block size from command 5 (`cl-worker36`, 5124 IOPS, p99 170.92ms): mixing in fsync'd writes at
the same time drops read throughput to 877 IOPS (an ~83% reduction) and pushes read p99 latency
from 171ms to 1053ms (roughly 6×). That is a concrete demonstration of WAL-fsync traffic
degrading foreground read performance on this storage when they share one queue — exactly the
contention a dedicated, separate WAL volume (see the storage-placement idea from the original
planning discussion) is meant to avoid.

---

## Interpreting results for PostgreSQL configuration

| Command(s) | Informs | What this cluster's run actually showed |
|---|---|---|
| 1, 2 (depth sweep + refinement) | `effective_io_concurrency`, `maintenance_io_concurrency` | Write-side elbow around depth 64 on `cl-worker36` (4k), but the refinement run landed on a different node (`cl-worker37`) and suggested 96-112 there — pin `-rnn` consistently before trusting an absolute number |
| 3 (numjobs) | `max_parallel_workers_per_gather` and friends | More threads at fixed depth 64 didn't grow `randread` throughput, only latency — 64 looks like a real ceiling on this node, not a per-queue limit. (`numjobs=16` also reproduced an all-zero anomaly, worth investigating separately) |
| 4 (block size) | Reasoning about checkpoint/bgwriter I/O coalescing | `randread` peaks at 128k (~8500 IOPS) then shifts to bandwidth-bound; `randwrite` is IOPS-bound throughout the tested range with no peak |
| 5, 6 (8k depth sweep, page cost) | `effective_io_concurrency` at the real page size; `random_page_cost` | Write elbow confirmed at ~64 for 8k too; but sequential read was *slower* than random read (3296 vs. 6457 IOPS) — on this storage class, `random_page_cost` should not be set above `seq_page_cost` |
| 7, 8 (WAL sync fsync/fdatasync) | `wal_sync_method`, expected max commit rate | ~123 commits/sec ceiling either way; `fdatasync` gave ~14% better p99 latency than `fsync` at the same throughput |
| 9 (group commit) | `commit_delay`, `commit_siblings` | Throughput scaled from 120 to 2308 IOPS across 1→32 concurrent writers with no plateau — this storage already coalesces commits well, so forcing batching in software is unlikely to help |
| 10 (WAL record size) | Expectations around `full_page_writes` bursts and large transactions | Throughput fell steadily from 140 to 49 IOPS as record size grew from 1k to 64k |
| 11 (checkpoint bandwidth) | `checkpoint_completion_target`, `max_wal_size` | Writeback bandwidth plateaus around 330-370MB/s at 4M-16M blocks/depth 16; pushing 16M blocks at depth 16 spiked p99 latency to ~14.8s — don't let checkpoint writeback queue that deep |
| 12 (OLTP/WAL proxy) | Sanity check under mixed load | Concurrent fsync'd writes cut foreground read throughput by ~83% and raised p99 latency ~6× versus isolated reads — real contention on this storage, supporting a separate WAL volume |

As with every bexhoma benchmark, treat these as a starting point for tuning, not as guaranteed
production numbers. Several results above disagree with the textbook defaults (`random_page_cost`
in particular) precisely because they were measured on this cluster's actual storage rather than
assumed — re-run against your own storage class and node hardware before trusting a config change
derived from them, and keep `-rnn` consistent across commands you intend to compare directly.

## Adjust Parameters

There are various ways to change parameters.

### Manifests

The YAML manifests for the components can be found in
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/k8s
(`deploymenttemplate-Hardware.yml`, `jobtemplate-benchmarking-hardware.yml`).

### Benchmarker script

The fio invocation itself lives in
https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/hardware/benchmarker/run_fio.sh

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
                   [-dbms [{Hardware} ...]] [-xht {fio,sysbench}]
                   [-xts HARDWARE_SIZE] [-xtd HARDWARE_DURATION]
                   [-xfrw FIO_RW] [-xfbs FIO_BS] [-xfid FIO_IODEPTH]
                   [-xfe FIO_ENGINE] [-xfsy FIO_FSYNC] [-xffd FIO_FDATASYNC]
                   [-xfmx FIO_RWMIXREAD]
                   {run,start,summary}

Run Hardware (fio/sysbench) benchmarks against a SUT in Kubernetes. Controls
fio workload shape (read/write pattern, block size, queue depth, engine) or
selects sysbench for CPU/memory benchmarking.

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
  -xht {fio,sysbench}, --xhardware-type {fio,sysbench}
                        benchmark tool: fio (disk I/O) or sysbench
                        (CPU/memory)
  -xts HARDWARE_SIZE, --xtest-size HARDWARE_SIZE
                        fio test file size (e.g. 1G, 64G)
  -xtd HARDWARE_DURATION, --xtest-duration HARDWARE_DURATION
                        fio/sysbench run duration in seconds
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
```
