# PostgreSQL pod-count degradation: is it the network? — findings so far

## Background

`docs/Example-Benchbase.md`'s PostgreSQL scale test
(`logs_tests/docs_benchbase_postgresql_scale.log`) showed throughput dropping ~21% and
latency rising ~27% when splitting 160 constant total threads from 1 benchmarking pod
into 2 (`-nbp 1,2 -nbt 160`). MySQL reproduces the same pattern. This note tracks the
investigation into whether that degradation comes from the Kubernetes network path
itself, or from the DBMS/benchmark-tool layer on top of it.

Tooling built along the way: a `netperf` (`TCP_RR`) `HARDWARE_TYPE` was added to the
`Hardware` benchmark (`hardware.py`, `images/hardware/`, `bexhoma/evaluators/hardware.py`,
`k8s/deploymenttemplate-Hardware.yml`) specifically to run many real concurrent TCP
connections with no database engine in the loop, as a network-only control. It's
documented for general use in `docs/Example-Hardware.md` (commands 17-19). This file is
the investigation notes, not documentation — it keeps the specific numbers and
conclusions that don't belong in neutral tool docs.

Scripts:
* `dev/test-netperf-pods.ps1` — early 1-vs-2-pod sockperf smoke test (superseded by netperf
  for this question; sockperf can't run more than 1 connection per process, see below).
* `dev/test-network-degeneration-postgresql-calibration.ps1` — finds each DB tool's
  uncapped 1-pod/64-thread throughput ceiling.
* `dev/test-network-degeneration-postgresql-comparison.ps1` — the actual 1/2/4-pod
  comparison: YCSB and Benchbase throttled to ~60% of their calibrated ceiling, netperf
  left uncapped (see "Why netperf isn't throttled" below).

## Why netperf, not just sockperf

sockperf's client supports exactly one connection per process
([Mellanox/sockperf#133](https://github.com/Mellanox/sockperf/issues/133): "sockperf does
not support parallel client send operations"), so a sockperf `-nbp` sweep only ever tests
as many connections as pods — nowhere near real DBMS connection counts. netperf's `TCP_RR`
can run many concurrent connections from one pod (`-nbt`, see `run_netperf.sh`), each
pinned to a fixed port out of a 64-port pool (`NETPERF_DATA_NUM_PORTS`) so the k8s Service
can forward it (only explicitly declared Service ports are reachable — confirmed the hard
way: a `port-sut-` naming/length-limit bug had to be fixed before this worked at all, see
git history for `k8s/deploymenttemplate-Hardware.yml`).

## Why netperf isn't throttled but YCSB/Benchbase are

DB engines get noisy right at their throughput ceiling — checkpoint stalls, lock
contention, buffer pressure all become bursty near saturation. The original benchbase
scale-test numbers were likely already at that noisy ceiling (achieved throughput matched
neither a low nor a comfortable fraction of the configured target). Calibrating each
tool's real ceiling first, then running the comparison at a stable, submaximal, controlled
target, was expected to give a cleaner signal — confirmed below.

netperf's `TCP_RR` is not throttled: it's inherently self-paced per connection (at most
one request in flight, bounded by real RTT, not an aggressive flood), so it isn't exposed
to the same near-saturation instability a DB engine gets from internal state. There's also
no rate-limiting flag wired for it in `hardware.py`.

## Calibration (1 pod, 64 threads, uncapped)

| Tool | Ceiling achieved | Throttle target used | % of ceiling |
|---|---|---|---|
| YCSB (workload a) | 81,228.17 ops/s | 16384×3 = 49,152 | ~60.5% |
| Benchbase (TPC-C) | 9,246.47 req/s | 1024×5 = 5,120 | ~55.4% |

Logs: `netdegen_ycsb_postgresql_calibration.log`, `netdegen_benchbase_postgresql_calibration.log`.

## Run 1: uncapped 1/2/4-pod comparison (before throttling was added)

| | 1 pod | 2 pods | 4 pods |
|---|---|---|---|
| Benchbase (req/s) | 9192.37 | 8303.00 (-9.7%) | 7515.99 (**-18.2%**) |
| YCSB (ops/s) | 82494.64 | 89264.71 (**+8.2%**) | 88955.35 (+7.8%) |
| netperf (trans/s) | 231050.78 | 223206.39 (-3.4%) | 232518.43 (+0.6%) |

netperf flat within noise at every pod count. Benchbase and YCSB diverge in **opposite**
directions from each other — both ride the same network path, so that divergence itself
points at the engine/workload layer, not the network. But YCSB's latency numbers in this
run were noisy/non-monotonic (see below), consistent with operating near its ceiling.

Logs: `netdegen_benchbase_postgresql_pod_scaling.log` (run at 15:26),
`netdegen_ycsb_postgresql_pod_scaling.log` (14:59), `netdegen_netperf_postgresql_pod_scaling.log` (15:48) —
these got overwritten by run 2 below; timestamps refer to the original run.

## Run 2: throttled comparison (YCSB/Benchbase at ~60% ceiling, netperf uncapped)

Throughput (YCSB/Benchbase hit target almost exactly at every pod count, as expected —
no longer an informative axis on its own):

| | 1 pod | 2 pods | 4 pods |
|---|---|---|---|
| YCSB (ops/s, target 49152) | 48470.75 | 48541.34 | 48580.25 |
| Benchbase (req/s, target 5120) | 5119.92 | 5119.55 | 5119.95 |
| netperf (trans/s, uncapped) | 231422.83 | 233989.74 | 241007.52 |

Latency at constant throughput — the actually informative signal here:

| | 1 pod | 2 pods | 4 pods | Δ 1→4 |
|---|---|---|---|---|
| Benchbase avg / p95 (µs) | 4886 / 12226 | 5095 / 12879 | 5671 / 14812 | **+16% / +21%**, clean monotonic |
| YCSB UPDATE p99 (µs) | 1963 | 1829 | 2279 | +16%, non-monotonic |
| netperf avg / p99 (ms) | 0.55 / 1.48 | 0.63 / 1.86 | 0.38 / 2.71 | avg non-monotonic; **p99 +83%** |

Logs: `netdegen_ycsb_postgresql_pod_scaling.log`, `netdegen_benchbase_postgresql_pod_scaling.log`,
`netdegen_netperf_postgresql_pod_scaling.log` (all in `logs_tests/local/`, run 2026-07-10 ~19:28-20:17).

## Current read

1. Throttling worked as hoped: Benchbase's latency curve went from noisy/non-monotonic
   (uncapped) to clean and monotonic (throttled). YCSB's 99th-percentile latency dropped
   from ~9-11ms (uncapped, near its ceiling) to ~2ms (throttled) — it was clearly in a
   noisy regime before.
2. **The nbp=1-vs-2 comparisons done earlier in this investigation (netperf flat
   throughput and latency) do not straightforwardly extend to nbp=4.** At 4 pods, even the
   pure-network netperf control shows p99 latency nearly doubling (+83%), despite
   throughput staying flat/rising. That's new evidence of a real network-layer tail-latency
   cost that only becomes visible beyond 2 pods — it does not rule the network back in as
   the primary cause (Benchbase's degradation is still larger and more consistent), but it
   means "the network isn't involved" can no longer be stated without the nbp≤2
   qualification.
3. Benchbase shows the cleanest, most consistent pod-count-correlated latency
   degradation of the three tools under controlled load. YCSB's is smaller and less
   consistent. Both ride the same network path as netperf, which also degrades at nbp=4 —
   so at this point the honest conclusion is "network contributes something at higher pod
   counts, DBMS-layer effects likely still explain most of Benchbase's degradation," not
   a clean single-cause story either way.

## Open questions / next steps

* Repeat runs (n≥3 per pod count) to get real variance estimates — everything above is a
  single run per configuration, so "clean monotonic" vs "noisy" is an eyeball judgment,
  not a statistical one.
* Extend netperf's own `-nbp` sweep to include intermediate points (e.g. 1,2,3,4) to see
  whether the tail-latency cost appears gradually or jumps at a specific pod count —
  current data only has nbp=1,2,4, so we can't tell if 3 already shows it.
* CPU/monitoring columns (`-m`) were collected in every run above but not yet examined —
  worth checking whether the netperf p99 jump at nbp=4 correlates with benchmarker-node
  (`cl-worker19`) CPU saturation from running 4 concurrent pods' worth of client processes,
  which would point back at client-side contention rather than the network path itself.
* The original degradation was observed at 160 total threads/connections; everything here
  used 64 (netperf's current `NETPERF_DATA_NUM_PORTS` ceiling). Raising that pool would
  allow testing at the original scale directly.
