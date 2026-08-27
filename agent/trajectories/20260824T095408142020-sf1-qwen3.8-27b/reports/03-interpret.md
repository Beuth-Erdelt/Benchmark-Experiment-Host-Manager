

# Benchmark Study Result

## Original question

Choose a database system for a 1 GB analytical reporting workload under 16 CPU cores and 64 GiB RAM, and determine whether the recommendation remains valid with concurrent analysts.

## Hypothesis

The chain tested two linked hypotheses. The first run (code `1787558149`) tested that **PgDuckDB with forced DuckDB execution beats PostgreSQL** on a 1 GB TPC-H workload at 16c/64GiB, with the ranking preserved from 1 to 2 concurrent analysts. That was refuted (PostgreSQL led at both levels), so the follow-up run (code `1787562545`, this report) tested the surviving question: **PostgreSQL's lead over PgDuckDB (forced DuckDB) persists at 4 concurrent analysts** — the point where PostgreSQL's parallel-worker demand (2 workers per gather × 4 concurrent queries = 8) exceeds the `analytical-ssd` profile's `max_parallel_workers=4` — preserving the system ranking; if the lead narrows materially or the ranking flips at 4 analysts, the PostgreSQL recommendation is valid only up to 2 concurrent analysts.

## Experiments performed

Two completed experiments in the chain, both TPC-H SF=1 (≈1 GB, Q1–Q22, 300 s per-query timeout, each query repeated 2×), 3 full repetitions, identical systems, tuning, resources, and placement.

**Previous run `1787558149`** — "single vs concurrent analysts": concurrency sweep rounds [1, 2] (1 and 2 benchmarking pods). Established the base ranking: PostgreSQL ahead of PgDuckDB at 1 and 2 analysts, both scaling near-linearly.

**Current run `1787562545`** — "concurrency sweep 1/2/4 analysts": the only change is the sweep extended to rounds **[1, 2, 4]** (1, 2, and 4 benchmarking pods; 22, 44, and 88 query executions per phase). Everything else held fixed:

- **Systems:** PostgreSQL vs PgDuckDB, both profile `analytical-ssd`, PgDuckDB with `duckdb_force_execution: true` (all queries through the DuckDB engine).
- **Tuning (identical, from index.md Workload):** shared_buffers 20480MB, effective_cache_size 49152MB, work_mem 1024MB, maintenance_work_mem 2048MB, max_parallel_workers_per_gather 2, max_parallel_workers 4, max_worker_processes 6, io_uring, random_page_cost 1.1, effective_io_concurrency 200.
- **Resources (fixed):** 16 CPU request/limit, 64 GiB RAM request/limit, 10 GiB ephemeral storage.
- **Placement (fixed):** SUT cl-worker21, loading cl-worker17 (2 pods, 1 thread, post-load indexes/constraints/statistics), benchmarking cl-worker19.
- **Observation:** SUT sidecar monitoring on; cluster/app monitoring off. bexhoma 0.10.8. Total benchmarking duration 3264 s.

## Validity

Index frontmatter (`report/index.md`): `overall_status: passed: 6, failed: 5, skipped: 1`.

**Failed (5):**
1–4. **Four monitoring-CPU checks** (Loading: SUT deployment and loader; Execution: SUT deployment and benchmarker) — `monitoring.md`/index Monitoring section show 0.00 CPUs / 0.00 Gb RAM for every component in both phases. **Scope:** all CPU/RAM resource-consumption metrics are void and are not quoted below.
5. **SQL errors** — 2 events, both PgDuckDB, both `PSQLException: (PGDuckDB/Duckdb_ExecCustomScan_Cpp) Executor Error: Query cancelled` (300 s timeout): Q3 on `PgDuckDB-1-1-1-1-1` (numRun 1) and Q18 on `PgDuckDB-1-2-3-1-3` (numRun 2) (`execution.md` Errors). **Scope:** per-query metrics for those two specific attempts, and the phase-level Throughput@Size of those two phases (223.73 and 838.10, phase times 354 s and 378 s vs ~27–79 s elsewhere). All PostgreSQL metrics and all other PgDuckDB cells are unaffected; the ranking is unchanged when the two contaminated phases are excluded.

**Passed (6):** No SUT container restarts; Geo Times [s], Power@Size [~Q/h], Throughput@Size all contain no 0/NaN; no SQL warnings (no result mismatch); workflow as planned (pod counts 1/2/4 matched the sweep).

**Skipped (1):** Loading data-generator CPU check (data pre-existing) — never invalidates.

**Verdict:** The run is sound for the questions asked. Correctness, completeness of the three headline metrics, workflow fidelity, and SUT stability all passed. The void areas are resource monitoring (not asked) and two isolated PgDuckDB timeout events (handled by exclusion; they are themselves evidence about PgDuckDB's tail behavior).

## Results

All figures from `report/index.md` (Key Metrics) and `report/execution.md` (Per Phase, Latency of Timer Execution [ms]).

**Headline metrics per phase (3 runs × 3 concurrency levels):**

| Phase (run-client) | Analysts | Geo Times [s] | Power@Size [~Q/h] | Throughput@Size |
|---|---|---|---|---|
| PostgreSQL-1-1-1 / -1-2-1 / -1-3-1 | 1 | 0.38 / 0.38 / 0.36 | 9359.56 / 9357.08 / 9974.07 | 2554.84 / 2554.84 / 2933.33 |
| PgDuckDB-1-1-1 / -1-2-1 / -1-3-1 | 1 | 1.02 / 1.07 / 1.02 | 3512.49 / 3375.89 / 3530.19 | 223.73* / 1389.47 / 1466.67 |
| PostgreSQL-1-1-2 / -1-2-2 / -1-3-2 | 2 | 0.40 / 0.40 / 0.36 | 9079.82 / 9035.44 / 9902.13 | 5109.68 / 4800.00 / 5866.67 |
| PgDuckDB-1-1-2 / -1-2-2 / -1-3-2 | 2 | 1.08 / 1.08 / 1.07 | 3340.11 / 3323.55 / 3362.65 | 2731.03 / 2684.75 / 2684.75 |
| PostgreSQL-1-1-3 / -1-2-3 / -1-3-3 | 4 | 0.43 / 0.44 / 0.41 | 8374.67 / 8205.32 / 8835.79 | 6740.43 / 7200.00 / 8123.08 |
| PgDuckDB-1-1-3 / -1-2-3 / -1-3-3 | 4 | 1.29 / 1.31 / 1.36 | 2790.05 / 2738.66 / 2649.70 | 4224.00 / 838.10* / 4010.13 |

\* contaminated by a 300 s query timeout (see Validity); excluded from clean means.

**Clean means across runs:**

| Analysts | PG Geo [s] | Duck Geo [s] | PG Throughput@Size | Duck Throughput@Size | PG lead (×) |
|---|---|---|---|---|---|
| 1 | 0.373 | 1.045 | 2681.0 | 1428.1 | 1.88× |
| 2 | 0.387 | 1.077 | 5258.8 | 2700.2 | 1.95× |
| 4 | 0.427 | 1.325 | 7354.5 | 4117.1 | 1.79× |

**Concurrency scaling (clean Throughput@Size):** PostgreSQL 2681 → 5259 → 7355 (1.96× then 1.40× per doubling); PgDuckDB 1428 → 2700 → 4117 (1.90× then 1.52× per doubling). Both sub-linear from 1→4; the absolute lead widens at every step (1253 → 2559 → 3238).

**Per-query latency (run 1, ms, `execution.md` Latency table):** PostgreSQL wins 18 of 22 queries at every concurrency level; PgDuckDB wins the same four — Q1, Q13, Q14, Q18 — at 1, 2, and 4 analysts. At 4 analysts (run 1): PG Q4 184–187 vs Duck 1276–1977; PG Q8 191–196 vs Duck 2344–2453; PG Q21 570–583 vs Duck 3647–4449. Two PostgreSQL queries show worker-starvation signatures at 4 analysts: Q14 jumps from ~2.1–2.3 s (1–2 analysts) to 4267–6373 ms, and Q1 from ~1.97 s to 1942–5495 ms — consistent with 8 demanded parallel workers against a supply of 4.

## Interpretation

**System choice (settled):** PostgreSQL is the correct system for a 1 GB analytical reporting workload at 16c/64GiB. It beats PgDuckDB (forced DuckDB) on all three headline metrics at every concurrency level — Geo Times ~0.36–0.44 s vs ~1.02–1.36 s (~2.8–3.1× lower), Power@Size ~8205–9974 vs ~2650–3530 ~Q/h (~2.8–3.1× higher), Throughput@Size ~2555–8123 vs ~1389–4224 (clean runs, ~1.8–1.9× higher) — and wins 18 of 22 individual queries. The original hypothesis that PgDuckDB would win is **refuted**.

**Concurrency robustness (settled through 4 analysts):** The follow-up hypothesis is **confirmed**. At 4 analysts — exactly the saturation point the design targeted (worker demand 8 > supply 4) — the ranking does not flip and the lead does not narrow materially: the throughput lead moves from 1.88× (1 analyst) to 1.79× (4 analysts), the absolute lead widens, and per-analyst Geo Times degrade only ~15% for PostgreSQL (0.373 → 0.427 s) vs ~27% for PgDuckDB (1.045 → 1.325 s). The recommendation is concurrency-robust across the tested range.

**Evidence vs mechanism:** The evidence establishes *that* PostgreSQL stays ahead at 4 analysts. The per-query degradation of PG's Q1 and Q14 at 4 analysts is consistent with the hypothesized parallel-worker starvation (demand 8 > `max_parallel_workers` 4), but the result folder contains no scheduler/worker telemetry to confirm the mechanism directly — that is inference, not measured fact. Conversely, the two PgDuckDB 300 s timeouts (Q3 at 1 analyst, Q18 at 4 analysts) are measured evidence that the DuckDB path has fragile tail latency under this workload, even though its aggregate ranking never threatened PostgreSQL's.

## Follow-up experiment

The previous run's handoff recorded a follow-up, which is this run (`1787562545`). It was needed because the user's concurrency question is unbounded while the first run only covered 1→2 analysts, and a concrete catalog-grounded mechanism (PostgreSQL worker demand 8 > supply 4 at 4 analysts) could have flipped the ranking beyond 2. The controlled intervention extended only the rounds sweep from [1, 2] to [1, 2, 4], holding systems, profiles, tuning, 16c/64GiB resources, placement, and 3 repetitions fixed. It resolved the uncertainty: the ranking does not flip and the lead does not narrow materially at 4 analysts, so the PostgreSQL recommendation is valid through 4 concurrent analysts.

## Final verdict

**Choose PostgreSQL** for the 1 GB analytical reporting workload under 16 CPU cores / 64 GiB RAM. The recommendation **remains valid with concurrent analysts through 4 concurrent analysts** (the maximum tested): PostgreSQL leads PgDuckDB (forced DuckDB) on Geo Times, Power@Size, and Throughput@Size at 1, 2, and 4 analysts, wins 18 of 22 queries at every level, and its per-analyst latency degrades less under concurrency.

Remaining limitations:
- **Concurrency beyond 4 analysts is unmeasured** — the user's question is unbounded, and both systems were already scaling sub-linearly (1.40–1.52× per doubling from 2→4), so behavior at 8+ analysts is not established.
- **Resource-consumption metrics are void** (4 failed monitoring checks, all 0.00 CPUs/0.00 Gb RAM): the run shows both systems operated within the enforced 16c/64GiB limits without restarts, but no measured utilization is available.
- **Two PgDuckDB queries hit the 300 s timeout** (Q3 at 1 analyst, Q18 at 4 analysts); the affected phase Throughput@Size values (223.73, 838.10) were excluded, and the ranking is unaffected, but it indicates PgDuckDB tail-latency fragility.
- Per the contract, comparisons are valid only within experiment code `1787562545`; the 1/2/4 analysis above uses only that run.
