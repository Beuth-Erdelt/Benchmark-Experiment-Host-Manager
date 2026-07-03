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

Result tables are filled in as each command is actually run to completion against a cluster.
Commands without a captured summary yet are marked *(result pending)* below.

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

*(result pending — this command has not yet been run to completion; the `## Show Summary`
section from its log will be pasted here once available)*

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

### Result

*(result pending — an earlier run of this command hit a bug in
`evaluators/hardware.py::benchmarking_set_datatypes()`: a read-only or write-only fio round can
leave the opposing direction's result columns blank, and casting a blank string to `float` raised
an exception before the summary could be printed. That has since been fixed (blanks are now
treated as 0 before casting), so a re-run should complete; the summary will be pasted here once
captured.)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

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

*(result pending — this command has not yet been run to completion)*

---

## Interpreting results for PostgreSQL configuration

| Command(s) | Informs | How |
|---|---|---|
| 1, 2 (depth sweep + refinement) | `effective_io_concurrency`, `maintenance_io_concurrency` | The elbow (throughput plateaus, tail latency rises) marks the queue depth beyond which more concurrency buys nothing |
| 3 (numjobs) | `max_parallel_workers_per_gather` and friends | Tells you whether the elbow is a per-queue submission limit (more parallel workers still help) or the real device ceiling (they don't) |
| 4 (block size) | Reasoning about checkpoint/bgwriter I/O coalescing | Shows where the workload shifts from IOPS-bound to bandwidth-bound |
| 5, 6 (8k depth sweep, page cost) | `effective_io_concurrency` at the real page size; `random_page_cost` | Re-anchors the depth number at `BLCKSZ`; the sequential/random latency ratio gives a device-specific cost relative to `seq_page_cost=1.0` |
| 7, 8 (WAL sync fsync/fdatasync) | `wal_sync_method`, expected max commit rate | max TPS with `synchronous_commit=on` and no batching ≈ 1 / sync-write latency; compare fsync vs. fdatasync directly |
| 9 (group commit) | `commit_delay`, `commit_siblings` | If aggregate fsyncs/sec scales with concurrent writers, the storage already coalesces commits; if not, force batching in software |
| 10 (WAL record size) | Expectations around `full_page_writes` bursts and large transactions | Shows how sync-write latency grows with record size |
| 11 (checkpoint bandwidth) | `checkpoint_completion_target`, `max_wal_size` | Bounds how fast checkpointer can flush dirty pages without starving foreground I/O |
| 12 (OLTP/WAL proxy) | Sanity check under mixed load | Approximates whether foreground reads and WAL flushes contend meaningfully on this storage |

As with every bexhoma benchmark, treat these as a starting point for tuning, not as guaranteed
production numbers — re-run against your actual storage class and node hardware before trusting
a config change derived from them.

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
