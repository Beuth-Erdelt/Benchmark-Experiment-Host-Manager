# Plan: tenancy sweep on the `nvme` pool

Status: **planned** (2026-10-11), not run. One small code change (M1), the
rest is measurement with the existing `hardware.py`.

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
- `-rnn <node>` pins **every** SUT to one node (`experiments/base.py:683`).
  Spreading tenants over several nodes is not possible today.
  `SutConfiguration.set_resources(nodeSelector=...)` exists per
  configuration, so a per-tenant node is a small change.

## Design

### Tenant

One SUT pod with its own PVC on `nvme` (one RBD image), fio as the only
workload. N ∈ {1, 2, 4, 8, 16}. Fresh volumes per experiment (`-rsr`).
Test file large enough to leave the OSD caches: `-xts 16G` per tenant
(16 tenants = 256 GiB on a replica-1 pool; check free space first).

### Workloads (one fio round each, all tenants run the same one)

| Name | fio | Main metric |
|---|---|---|
| `commit` | write, 8k, QD1, `fdatasync=1`, sync | commits/s, p50/p99 fdatasync |
| `randwrite` | randwrite, 8k, QD32, libaio | IOPS, p99 |
| `seqwrite` | write, 1M, QD8, libaio | MB/s |

Duration 60 s per round (`-xtd 60`, see the ramp-time risk below), 3 repetitions, order of N alternated
between repetitions (up, down, up), as in the remote/local rerun that
confirmed the 0.4 vs 1.35 GB/s gap.

### Noisy neighbor (question 3)

N tenants of which tenant 0 runs `seqwrite` and the others `commit`, at the
same time. Today all tenants of one round get the same fio parameters, so this
needs M2. Until then it is approximated with two experiments started together
by hand (one `seqwrite` tenant, N−1 `commit` tenants), which loses the
synchronized start.

### Placement (question 4)

| Placement | N | Purpose |
|---|---|---|
| A: all on cl-worker21 | 1, 2, 4, 8, 16 | realistic case: SUTs do not run on storage nodes |
| B: all on cl-worker40 | 1, 4, 16 | reference without the network; tenants compete with the OSDs for CPU |
| C: round-robin over cl-worker21, cl-worker34, cl-worker37 | 3, 6, 12 | separates a client-node limit from an OSD limit |
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

### M1: per-tenant node placement (needed for C)

- `hardware.py`: new flag `-xtnn` / `--xtenant-nodes`, a comma-separated
  node list. With `-mtb container`, tenant *i* gets
  `config.set_resources(nodeSelector={'kubernetes.io/hostname':
  nodes[i % len(nodes)]})`. Refuse together with `-rnn`.
- Check that the configuration-level `nodeSelector` replaces the
  experiment-level one in the SUT manifest and is not merged with the `cpu`
  selector that `-rnn` sets (the `gpu` nodes carry no `cpu` label value).
- GPU nodes: check for taints or a toleration Kyverno would block.
- Record the node of each tenant in `connections.config` (it already holds
  the SUT's node from the pod) and show it in `connections.md`.
- Tests: the tenant → node assignment; refusal with `-rnn`.

### M2: per-tenant workload (needed for the synchronized noisy neighbor)

`-xtw` / `--xtenant-workload`: a comma-separated list of fio profiles
(`commit`, `randwrite`, `seqwrite`, as in the workload table), one per
tenant in tenant order. **The last entry repeats**, so
`-mtn 8 -xtw seqwrite,commit` is one noisy tenant and seven commit tenants,
and N can change without rewriting the list.

**Why not the per-pod mechanism.** Bexhoma can give each pod of one
benchmarker job its own parameters: `SutConfiguration._push_pod_configs()`
(`configurations/base.py:622`) writes `{queue}-config-{i}` to Redis from the
round entry's `pod_parameters`, and `images/hardware/benchmarker/benchmarker.sh`
(lines 75–85) exports it as `BEXHOMA_POD_<key>`. With `-mtb container`,
however, every tenant is its own configuration with its own job of one pod,
so per-tenant values belong in the tenant loop of `hardware.py`, not in
`pod_parameters`. (As of 2026-10-11 the per-pod path is plumbing only: no
code fills `pod_parameters`, `add_benchmarking_parameters()` /
`add_benchmark_list()` do not carry it, and no script reads a
`BEXHOMA_POD_*` variable.)

Case A, for this plan (Python only, no image rebuild):

- `hardware.py`: a `FIO_PROFILES` dict mapping each profile name to its
  `HARDWARE_FIO_*` values, and `workload_of(workloads, i)` returning
  `workloads[min(i, len(workloads) - 1)]`.
- In the existing tenant loop, merge `FIO_PROFILES[workload_of(...)]` (plus
  `HARDWARE_FIO_PROFILE=<name>`) last into `add_benchmarking_parameters()`,
  so it wins over the sweep values.
- Validation: only with `-xht fio`; refused together with non-default
  `-xfrw`/`-xfbs`/`-xfid`/`-xfe`/`-xfsy`/`-xffd` (the sweep would otherwise
  produce identical rounds); unknown profile names refused.
- Evaluation needs no change: `HardwareEvaluator` reads the fio parameters
  from each pod's log (last match) and already has a per-tenant summary
  (`get_summary_benchmark_per_phase_multitenant`). Optional:
  `HARDWARE_FIO_PROFILE` as a readable column (one `echo` in
  `benchmarker.sh`, one key in `_KEYS_TYPE_PARAMETERS`).
- Tests: tenant → profile mapping including the repeating last entry;
  refusals.

Example:

```
python hardware.py run -mtb container -mtn 8 -rst nvme -rsr -rnn cl-worker21 \
    -xtw seqwrite,commit -xts 16G -xtd 60
```

Case B, a separate later step (not needed for this plan): several fio
pods on **one** SUT and volume (`-nbp N`), i.e. contention on the same
volume. This is where the per-pod mechanism fits:

1. `configurations/base.py`: `add_benchmarking_parameters(...,
   pod_parameters=None, ...)` stores `pod_parameters` in the round entry;
   `add_benchmark_list()` keeps it when rebuilding (generic, all benchmarks).
2. `hardware.py`: without tenancy, `-xtw` becomes
   `pod_parameters=[FIO_PROFILES[workload_of(w, i)] for i in range(pods)]`.
3. `benchmarker.sh`, after reading the per-pod config: export every
   `BEXHOMA_POD_HARDWARE_*` as `HARDWARE_*` and echo it, so the evaluator
   (last match) records the pod's actual values. Image rebuild.
4. `evaluators/hardware.py:326-330`: per-phase aggregation sums IOPS/bandwidth
   over pods and takes fio parameters from the first pod; with mixed
   profiles in one phase, group by `hardware_fio_profile` (or the fio
   parameter columns) instead.
5. The shell parser handles only string values without commas or quotes;
   `_push_pod_configs` should `str()` all values.

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
  of each round are measured. fio lays out the test file before the timed
  run, but with N tenants the layouts finish at different times, so the
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
