

## Interpretation of experiment 1787125351

### Trustworthiness — partially sound, with one major gap

The run is **valid for the head-to-head comparison but blind on resources**:

- **Sound:** No SUT container restarts, workflow ran exactly as planned, no SQL result-mismatch warnings, and all headline metrics (Geo Times, Power@Size, Throughput@Size) are complete with no 0/NaN (`report/index.md`, Tests table).
- **Failed checks that scope the numbers:**
  - **SQL errors: 3** — all on `PgDuckDB-32Gi`, all `ERROR: (PGDuckDB/Duckdb_ExecCustomScan_Cpp) Executor Error: Query cancelled` (300 s timeout): Q21 in phase `PgDuckDB-32Gi-1-4` (stream 7, repeat 10), Q21 in `PgDuckDB-32Gi-2-2` (stream 1, repeat 2), Q9 in `PgDuckDB-32Gi-3-4` (stream 2, repeat 1) (`report/execution.md`, Errors subsection). Per-query metrics for those specific queries are void; the phases' wall times (380 s, 358 s, 365 s vs. ~56–89 s for clean phases, `report/execution.md`, Per Phase table) and their low Throughput@Size (378.95, 100.56, 394.52) are artifacts of the hangs, not representative performance.
  - **All four monitoring tests failed** — every CPU and RAM value for SUT and benchmarker is 0.00 (`report/monitoring.md`, Execution phase: SUT deployment; `report/index.md` Monitoring section: "0.00 CPUs, 0.00 Gb RAM (peak)" for every component). **No resource data exists in this run.**

### 1. Is pg_duckdb better on joins than PostgreSQL, even under concurrency? — No, clearly not

PostgreSQL wins at every concurrency level, by a wide margin (`report/index.md` Key Metrics; `report/execution.md` Per Phase):

| Concurrency (streams) | PostgreSQL Geo Times [s] | PgDuckDB Geo Times [s] | PostgreSQL Throughput@Size | PgDuckDB Throughput@Size |
|---|---|---|---|---|
| 1 | 0.20–0.24 | 0.96–1.10 | 1285–1385 | 305–346 |
| 2 | 0.22–0.24 | 0.97–1.15 | 2571 | 581–667 |
| 4 | 0.26–0.30 | 1.39–1.46 | 3273–3789 | 847–935 |
| 8 | 0.34–0.37 | 1.47–1.57 | 5143–5538 | 1618–1655 |

PostgreSQL is ~4–5× faster per query (geometric mean) on Q5/Q7/Q8/Q9/Q21 at SF=1, and it stays ahead as streams scale 1→8. Both systems' total throughput scale roughly linearly with concurrency (PostgreSQL ~1300→~5400 Q/h; PgDuckDB ~320→~1640 Q/h), so the gap is not a concurrency artifact — it holds at 1 stream too.

### 2. Memory starvation per stream, or thread contention? — Not resolvable from this run; the evidence points both ways

First, a correction to the premise: **throughput does not degrade as streams increase** — it rises for all four configurations. What degrades is *per-query latency* (Geo Times: PgDuckDB ~1.0 s → ~1.5 s; PostgreSQL ~0.23 s → ~0.36 s from 1 to 8 streams), which is normal resource sharing.

The two candidate mechanisms each leave a signature:

- **Thread/CPU contention signature:** the latency degradation is *similar at both memory limits* — PgDuckDB 32Gi goes 1.01→1.53 s median across rounds while 64Gi goes 1.07→1.55 s; PostgreSQL is likewise flat between 32Gi and 64Gi at every round. CPU is identical (16 cores) in both configurations, and the hypothesis's own discriminator said "degradation similar at both memory limits ⇒ thread contention." That pattern is present.
- **Memory-starvation signature:** all 3 query cancellations (queries hanging until the 300 s timeout) occurred **only on the 32Gi configuration** — two in 8-stream rounds, one in a 2-stream round — while the 64Gi configuration completed all 12 phases cleanly. A pure CPU-contention effect should appear at both limits; a 32Gi-only hang pattern is consistent with memory pressure (e.g., spilling/thrashing under 8 concurrent DuckDB instances).

**But the run cannot adjudicate**, because the data that would confirm either mechanism — CPU utilization (was the 16-core limit saturated?) and RAM usage (did 32Gi get close to its ceiling?) — is entirely missing: every monitoring value is 0.00, and the corresponding validity tests failed. A secondary confound: the 32Gi and 64Gi configurations also differ in PostgreSQL tuning (shared_buffers 10 vs 20 GB, work_mem 512 MB vs 1 GB, effective_cache_size 24 vs 48 GB, per the deployment overrides in `report/index.md`), so the memory-limit comparison is not perfectly isolated, though with `duckdb_force_execution: true` the DuckDB side is the dominant factor.

### What the hypothesis got right and wrong

- **Wrong:** "PgDuckDB matches or beats PostgreSQL on multi-way TPC-H joins as concurrent streams scale 1→8." It lost at every level, by ~4–5× on per-query time.
- **Partially right:** the degradation-vs-concurrency mechanism. The hypothesis predicted memory starvation would show as "degradation markedly worse at 32Gi than 64Gi." The *latency* degradation was in fact similar at both limits (the thread-contention branch), but the 32Gi-only 300 s query cancellations are a memory-limit-dependent failure the hypothesis's latency-based discriminator doesn't capture. So the data suggests **both**: ordinary thread/CPU contention driving the smooth latency rise, plus a memory-pressure failure mode that only manifests at 32Gi under concurrency.
- **For your 64 GB servers:** the 64Gi configuration (your ceiling) ran clean with no cancellations at 8 streams, so PgDuckDB is workable there — but on this 1 GB join workload PostgreSQL is the faster engine, and the 32Gi results warn that tighter memory caps make PgDuckDB's tail behavior (queries hanging to timeout) a real risk under concurrency.

**Bottom line:** the head-to-head answer is settled (PostgreSQL wins on these joins, including under concurrency); the memory-vs-contention question is only partially answered — directionally thread contention for the general degradation, with a 32Gi-specific memory-pressure failure mode — and the missing (all-zero) CPU/RAM monitoring is the evidence needed to close it.



Validation passed on the first attempt. The estimate confirms **24 runs** (1 system × 2 memory cells × 4 concurrency rounds × 3 repetitions), matching the design.

## What the proposed run would settle

**The unresolved mechanism question** — whether PgDuckDB's (forced DuckDB execution) per-query latency degradation as streams scale 1→8, and the 32Gi-only 300 s query cancellations, are driven by **per-stream memory starvation** or **thread/CPU contention**.

The prior run was blind on this: every CPU/RAM value was 0.00 because its clean phases (56–89 s) fell inside the catalog's 2–5 min monitoring warm-up window. This run's single controlled change — `query_repeats` 10 → 50 — stretches each phase to ~4.7–7.4 min so the SUT and cluster scrapes accumulate real samples, producing the non-zero CPU and RAM time series the discriminator needs.

**How the result adjudicates:**
- **CPU saturates near 16 cores at both 32Gi and 64Gi, RAM well below ceiling** → thread/CPU contention is the driver.
- **RAM approaches the 32Gi limit only in the 32Gi config, which also shows the worse degradation/cancellations** → per-stream memory starvation is the driver.
- **Both signatures co-occur** → the run quantifies their relative contribution (the interpretation's directional read was "both").

**What it deliberately does *not* re-test:** the head-to-head (PostgreSQL already won at every concurrency level, ~4–5× on per-query time), so PostgreSQL is dropped from `systems` — halving cost and keeping the run attributable to the mechanism. `discriminates` is therefore `[concurrency, memory]` (system and CPU are held fixed).

**Feasibility confirmed:** cl-worker36 (224 CPU / ~2015 GiB / ~1.58 TiB) comfortably fits the 16 CPU + 64Gi + 10Gi node-local request; `storage_class` stays unset (node-local) since no `ssd` class exists in the environment and the `analytical-ssd` profile permits `null`.

The specification is validated and ready; I'm stopping here without submitting.
