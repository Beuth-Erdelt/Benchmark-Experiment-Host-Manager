# Plan: tenancy sweep on the `nvme` pool

Status: **planned** (2026-10-11), not run. One small code change (M0a fio
overwrite, added 2026-10-16, **implemented 2026-10-17**, image rebuild and
validation run open); placements A, B and D with the
same workload for all tenants are then measurement with `hardware.py`.
Placement C and the synchronized noisy neighbor need per-tenant placement and
workload, which is a separate, generic plan:
[plan-per-config-overrides.md](plan-per-config-overrides.md) (split out
2026-10-16; formerly M1 and M2 here).

## Goal

Measure how per-tenant and total storage performance change as more pods,
each with its own volume, share the `nvme` pool, and find out where the limit
sits: in the OSDs on cl-worker40 or on the client node.

Questions:

1. How do WAL commits/s, p99 fdatasync, 8k random IOPS and 1 MiB sequential
   throughput per tenant change for N = 1, 2, 4, 8, 16 tenants?
2. At which N does the total stop growing, and is the split between tenants
   fair?
3. Does one tenant writing large blocks hurt the commit latency of the others,
   as the parallel HammerDB run did on 2026-10-11 (−40% commits, p99
   fdatasync 3.5–5 ms)?
4. Is the remote limit (~0.4 GB/s for 1 MiB writes, against ~1.35 GB/s local)
   per client node or per OSD?

## Facts this plan relies on

**Cluster** (2026-10-11)

- `nvme`: RBD pool, replica size 1, 6 OSDs (13, 35, 36, 37, 39, 40), all on
  cl-worker40 (EPYC 7413, Zen 3, 48 threads, kernel 6.8). The OSD pods have no
  CPU request or limit, so they share all 48 threads; memory 10 Gi request,
  18 Gi limit.
- Single tenant, from earlier fio runs: local (client on cl-worker40)
  ~3,050 commits/s, fdatasync 0.31 ms, 1 MiB sequential ~1.35 GB/s; remote
  (cl-worker21, EPYC 7542, Zen 2) ~2,700 commits/s, fdatasync 0.36 ms,
  ~0.4 GB/s. 8k random write at QD32 ~10k IOPS in both places, so for small
  random I/O the OSDs are the limit, not the network.
- Candidate client nodes: cl-worker21 (`cpu`, the only modern non-GPU worker),
  cl-worker34 and cl-worker37 (`gpu`, EPYC 7453, Zen 3). Storage nodes are
  tainted `node-role.kubernetes.io/storage:NoSchedule`; namespace `perdelt` is
  excluded from the Kyverno toleration policy.
- krbd shares one Ceph client instance per node across all mapped images by
  default, so all tenants on one node share one messenger connection per OSD.
  The map option `noshare` gives each image its own client.

**Bexhoma**

- `hardware.py -mtb container -mtn N` already creates one SUT pod and one PVC
  per tenant (`hardware-{tenant}-{N}`), and the Redis round counter starts
  all tenants' fio runs at the same moment (`experiments/base.py`
  `work_benchmark_list()`).
- fio runs **inside the SUT pod** over SSH (`images/hardware/sut`), against
  `/database/fio-test` on the PVC. The SUT's node is the client's node.
- The fio flags `-xfrw`, `-xfbs`, `-xfid`, `-xfsy`/`-xffd`, `-xfe` sweep as
  sequential rounds within one experiment.
- `-rst nvme -rsr` gives fresh volumes on `nvme`.
- `run_fio.sh` writes into a **fresh** test file (fio's default
  `fallocate=native`, i.e. unwritten ext4 extents). Every O_DIRECT write then
  converts an extent, and every fdatasync commits an ext4 journal entry. A/B
  on 2026-10-16 (separate pod on cl-worker36, nvme PVC, 256 PGs, 8k write,
  QD1, sync, `fdatasync=1`, 30 s):

  | Test file | commits/s | write clat p50 | fdatasync mean / p99 |
  |---|---:|---:|---:|
  | fresh (as bexhoma today), run twice | 361 / 370 | 0.93 / 0.89 ms | 1.85 / 3.16 ms |
  | fresh, `fallocate=none` | 346 | 0.95 ms | 1.95 / 3.46 ms |
  | prefilled once (1M seq write), then the same job | 1,538 | 0.64 ms | 0.003 / 0.003 ms |

  On a prefilled file fdatasync is a no-op (krbd advertises no volatile write
  cache), so a commit costs one RBD write round trip. PostgreSQL WAL segments
  are zero-filled when created and recycled later, so WAL behaves like the
  prefilled case. The bexhoma run `fio_write_latency_nvme` (1792162949,
  ~400 commits/s) therefore understates WAL commits by ~4×. The ~0.64 ms is
  still slower than the 0.36 ms fdatasync of the 2026-10-11 manual run
  (cl-worker21, 1 PG); that gap is not explained yet.
- `-rnn <node>` pins **every** SUT to one node (`experiments/base.py:683`).
  Spreading tenants over several nodes is not possible today.
  Per-tenant placement is covered by
  [plan-per-config-overrides.md](plan-per-config-overrides.md).

## Design

### Tenant

One SUT pod with its own PVC on `nvme` (one RBD image), fio as the only
workload. N ∈ {1, 2, 4, 8, 16}. Fresh volumes per experiment (`-rsr`).
Test file large enough to leave the OSD caches: `-xts 16G` per tenant
(16 tenants = 256 GiB on a replica-1 pool; check free space first).

### Workloads (one fio round each, all tenants run the same one)

| Name | fio | Main metric |
|---|---|---|
| `commit` | write, 8k, QD1, `fdatasync=1`, sync, overwrite (`-xfow 1`, M0a) | commits/s, p50/p99 fdatasync |
| `randwrite` | randwrite, 8k, QD32, libaio | IOPS, p99 |
| `seqwrite` | write, 1M, QD8, libaio | MB/s |

Duration 60 s per round (`-xtd 60`, see the ramp-time risk below), 3 repetitions, order of N alternated
between repetitions (up, down, up), as in the remote/local rerun that
confirmed the 0.4 vs 1.35 GB/s gap.

### Noisy neighbor (question 3)

N tenants of which tenant 0 runs `seqwrite` and the others `commit`, at the
same time. Today all tenants of one round get the same fio parameters, so this
needs the per-tenant env override of
[plan-per-config-overrides.md](plan-per-config-overrides.md). Until then it is approximated with two experiments started together
by hand (one `seqwrite` tenant, N−1 `commit` tenants), which loses the
synchronized start.

### Placement (question 4)

| Placement | N | Purpose |
|---|---|---|
| A: all on cl-worker21 | 1, 2, 4, 8, 16 | realistic case: SUTs do not run on storage nodes |
| B: all on cl-worker40 | 1, 4, 16 | reference without the network; tenants compete with the OSDs for CPU |
| C: round-robin over cl-worker21, cl-worker34, cl-worker37 | 3, 6, 12 | separates a client-node limit from an OSD limit; needs the per-tenant node override |
| D: like A, krbd `noshare` | 4, 16 | only if A stalls below C: tests the shared-connection hypothesis |

Reading rule for A against C at the same N:

- C's total clearly above A's: the limit is on the client node (shared krbd
  connection, packet processing, client CPU).
- Both stall at the same total: the OSDs on cl-worker40 are the limit.

B is not a second copy of A. Clients on cl-worker40 use loopback and take CPU
from the OSDs, so B shows the best case for latency and the worst case for
CPU sharing.

### What is recorded

- Per tenant, per round: fio's result (Bexhoma `HardwareEvaluator`).
- Derived: per-tenant median, min/max ratio and Jain's fairness index, total
  over tenants, N at which the total grows by < 10% when N doubles.
- Per run, from Prometheus (by hand until `plan-ceph-pool-metrics.md` lands):
  - `ceph_pool_wr_bytes` / `ceph_pool_wr` for `nvme`, to confirm no other
    tenant wrote to the pool during the run (abort and repeat if it did);
  - node CPU per mode (incl. softirq) on cl-worker40 and every client node;
  - NIC bytes on cl-worker40 and every client node;
  - NVMe device utilization on cl-worker40.
- During one `seqwrite` round at N = 16, placement A: per-thread CPU of the
  OSD processes (`top -H` on cl-worker40 if a debug pod is allowed, otherwise
  `container_cpu_usage_seconds_total` per OSD pod) and per-CPU softirq on
  cl-worker21, to see whether a single thread or core is at 100%.

### Run budget

Per placement and N: 3 workloads × 60 s + ramp and setup ≈ 6 min; × 3
repetitions. A ≈ 1.5 h, B ≈ 1 h, C ≈ 1 h, D ≈ 40 min, noisy neighbor ≈ 1 h.

## Implementation sketch

### M0a: fio overwrite option (`-xfow`)

**Implemented 2026-10-17** as sketched below, with these differences and open
points:

- `hardware.py` splits `-xfow` as strings (like `-xfrw`/`-xfe`), so an
  invalid value is a parser error instead of an `int()` ValueError. The value
  shares the `fio_fdatasync` loop level via `itertools.product` instead of
  a new nesting level; rounds are ordered fdatasync-major, overwrite-minor.
- `bexhoma/hardware_baseline.py`: `HARDWARE_FIO_OVERWRITE: "0"` in
  `_FIO_DEFAULTS`.
- Docs: flag paragraph and a note on fresh vs. prefilled in
  `docs/Example-Hardware.md`, help output there updated. `-xfow 1` added to
  the commands of `wal_sync_fsync` (docs case 4), `wal_sync_fdatasync`,
  `wal_group_commit`, `wal_record_size`, `checkpoint_writeback` and
  `oltp_wal_contention_proxy` in `scripts/test-docs-{cases,hardware}.{sh,ps1}`,
  `docs/TestCases.md` and `docs/Example-Hardware.md`. **Their result sections
  still show the old fresh-file runs until these cases are rerun.**
- Tests: `tests/test_hardware_fio_overwrite.py`. The `run_fio.sh` tests are
  skipped on Windows; checked by hand with Git bash (1 → `--overwrite=1`,
  0/unset → none).
- **Open:** rebuild `bexhoma/benchmarker_hardware` (old images ignore
  `HARDWARE_FIO_OVERWRITE` and silently measure a fresh file; the round's
  log then lacks the `HARDWARE_FIO_OVERWRITE:` line), then the validation
  run below.

Needed before M0, so that `commit` measures WAL-like commits (see the A/B in
"Facts"). An option, not always-on: both behaviours are real database
patterns.

| `-xfow 1` (prefilled) | `-xfow 0` (fresh, today) |
|---|---|
| PostgreSQL WAL, InnoDB redo (preallocated, recycled) | table/index growth during bulk load or COPY |
| checkpoint and random page writes into existing relations | append-only files (logs, LSM SSTables), a new database |

The effect is not limited to sync tests: on a fresh file the O_DIRECT write
itself was slower too (0.93 vs 0.64 ms p50), so randwrite and throughput
rounds are affected, less strongly.

- `hardware.py`: `-xfow` / `--xfio-overwrite`, comma-separated sweep list
  like the other fio flags, values `0`/`1`, **default `0`** (keeps existing
  results comparable). Add a loop level next to `fio_fdatasync` in both
  sweep blocks (`hardware.py:203`, `:272`) and pass
  `HARDWARE_FIO_OVERWRITE` with the other `HARDWARE_FIO_*` values
  (`:234`, `:303`). Refuse values other than 0/1.
- `images/hardware/benchmarker/run_fio.sh`: echo `HARDWARE_FIO_OVERWRITE`
  in the parameter block; append `--overwrite=1` when it is `1`. fio then
  lays the file out by writing it fully before the timed part (layout is not
  part of `--runtime`). Default `0` when unset, so old round entries still
  work. Add `overwrite` to the CSV header/row. Image rebuild.
- `bexhoma/evaluators/hardware.py`: `HARDWARE_FIO_OVERWRITE` in the key list
  (`:44`), type `int` (`:242`), and in the grouping/column lists
  (`:327`, `:359`, `:412`, `:462`). Missing key in old logs → 0.
- `bexhoma/benchmarks/hardware.py:84-92`: summary line
  "Overwrite (prefilled test file) swept: [...]".
- Docs: `docs/Example-Hardware.md` (flag table, a note on fresh vs.
  prefilled with the A/B numbers), `docs/TestCases.md`. Set `-xfow 1` in the
  WAL-style test cases (`wal_sync_fdatasync`, `wal_sync_fsync`,
  `wal_record_size`, `wal_group_commit`, `oltp_wal_contention_proxy`) in
  `scripts/test-docs-*.{sh,ps1}` and `scripts/test-docs-cases.{sh,ps1}`;
  `checkpoint_writeback` too (writes into existing relation files). Their
  logs in `logs_tests/` then need a rerun.
- Cost: layout writes `-xts` per job before each round (seconds for 1G,
  longer for 8G/16G × numjobs). With the tenancy barrier, layout must happen
  before the synchronized start; this also resolves the "No ramp time" risk
  for write workloads if layout precedes the barrier (check in M0).
- Tests: flag parsing and refusal; `run_fio.sh` argument building with
  0/1/unset; evaluator reads old logs without the key as 0.
- Validation run: `-xfrw write -xfbs 8k -xffd 1 -xfe sync -xfow 0,1 -rst nvme`
  should reproduce ~370 vs ~1,500 commits/s.

### M0: run A and B with the code as it is

```
python hardware.py run -mtb container -mtn {N} -rst nvme -rss 20Gi -rsr \
    -rnn cl-worker21 -xts 16G -xtd 60 \
    -xfrw write,randwrite -xfbs 8k,1M ...
```

The rw × bs × iodepth × fsync lists are crossed. To get exactly the three
workloads, run one experiment per workload, or accept the extra rounds.
Check that the 16 tenants are all `Running` before the round counter
releases them, and that the 16 PVCs bind.

### Placement C and noisy neighbor: per-tenant overrides

Moved to [plan-per-config-overrides.md](plan-per-config-overrides.md)
(2026-10-16). Instead of `hardware.py`-only flags (`-xtnn`, `-xtw`), tenants
are addressed by tenant id in a generic `--set` scope, for every benchmark:

```
# placement C
--set "sut@tenant:0,3,6,9.node=cl-worker21"
--set "sut@tenant:1,4,7,10.node=cl-worker34"
--set "sut@tenant:2,5,8,11.node=cl-worker37"
# noisy neighbor: tenant 0 seqwrite, the others the commit default
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_BS]=1M"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_IODEPTH]=8"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_ENGINE]=libaio"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_FDATASYNC]=0"
```

The fio profiles of the workload table become documented bundles of such
lines. The per-pod mechanism (several fio pods on one SUT and volume,
formerly "Case B" here) is described there under "Not covered".

### M3: krbd `noshare` (needed for D)

Not a Bexhoma change: a second StorageClass `nvme-noshare` with
`mapOptions: noshare` (cluster admin). Run A again with `-rst nvme-noshare`.

## Risks and open points

- **The pool is shared.** Others can write to `nvme` at any time (HammerDB
  did). The pool counters before and during each run decide whether a run
  counts.
- **Replica 1, no redundancy.** Data on `nvme` is disposable. 16 × 16 GiB test
  files plus other users must fit.
- **Hardware differs between clients.** cl-worker21 is Zen 2, cl-worker34/37
  and cl-worker40 are Zen 3; kernels may differ. C mixes them. Check NIC speed
  and MTU on cl-worker34/37 before using them; if they differ from
  cl-worker21, C compares more than placement.
- **Sixteen SUT pods on one node** (A at N = 16) also share the client node's
  CPU. The page cache is not involved: `run_fio.sh` passes `--direct=1`.
- **No ramp time.** `run_fio.sh` has no `--ramp_time`, so the first seconds
  of each round are measured. For write workloads fio only fallocates the
  test file (no data written) unless `--overwrite=1` (M0a); with it, or for
  reads, fio lays out the file before the timed run. With N tenants the layouts finish at different times, so the
  synchronized start covers the timed part only if layout happens before the
  barrier. Check this in M0; if not, add an optional `HARDWARE_FIO_RAMP`
  to `run_fio.sh`.
- **OSD cache warm-up.** The first round after creating fresh volumes can be
  slow (seen once: ~60 commits/s). Discard a first warm-up round or
  repeat until stable.
- **Jumbo frames are not needed to explain the remote gap.** iperf3 on the
  host network from cl-worker21 to cl-worker40 (2026-10-11, MTU 1500 on
  both, bond0 2 × 25 GbE) reached 16.3 Gbit/s (≈ 2 GB/s) on a single TCP
  stream and 23.5 Gbit/s with 4 streams, against ~0.4 GB/s for 1 MiB RBD
  writes. The limit is in the krbd/Ceph path, not in TCP packet handling.

Related: [plan-ceph-pool-metrics.md](plan-ceph-pool-metrics.md) (pool and
other-volume metrics, would replace the manual Prometheus queries),
[plan-storage-class-sweep.md](plan-storage-class-sweep.md),
[plan-ycsb-sysbench-noisy-neighbor.md](plan-ycsb-sysbench-noisy-neighbor.md)
(CPU contention, not storage).
