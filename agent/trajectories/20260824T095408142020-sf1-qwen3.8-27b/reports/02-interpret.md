

# Benchmark Study Result

## Original question

Choose a database system for a 1 GB analytical reporting workload under 16 CPU cores and 64 GiB RAM, and determine whether the recommendation remains valid with concurrent analysts.

## Hypothesis

The experiment chain tested the hypothesis that, under a 16-core / 64 GiB budget, **PgDuckDB with forced DuckDB execution beats PostgreSQL** on a 1 GB TPC-H analytical workload (higher Throughput@Size, lower Geo Times), and that **this system ranking is preserved** when the workload moves from 1 to 2 concurrent analysts. The experiment was designed to discriminate on two axes: `system` (PostgreSQL vs PgDuckDB) and `concurrency` (1 vs 2 analysts).

## Experiments performed

One completed experiment (code `1787558149`), mode `run`, titled "TPC-H SF1 system choice under 16c/64GiB: single vs concurrent analysts."

- **Workload:** TPC-H, scaling factor 1 (≈1 GB), 22 queries (Q1–Q22), 300 s per-query timeout, each query repeated 2 times.
- **Systems (treatment):** PostgreSQL (profile `analytical-ssd`) vs PgDuckDB (profile `analytical-ssd`, override `duckdb_force_execution: true` so all queries run through the DuckDB engine). Both received identical analytical tuning (shared_buffers 20480MB, effective_cache_size 49152MB, work_mem 1024MB, parallel workers 2/4/6, io_uring, random_page_cost 1.1, effective_io_concurrency 200).
- **Concurrency sweep (rounds):** benchmarking run as [1, 2]× the number of benchmarking pods — i.e., client 1 = 1 concurrent analyst (1 pod, 22 queries), client 2 = 2 concurrent analysts (2 pods, 44 queries).
- **Repetitions:** 3 full experiment runs (`-nc`), so each system × concurrency cell has 3 independent measurements.
- **Loading:** 2 pods, 1 thread; post-load step set indexes + constraints and recomputed statistics.
- **Resources (fixed for both SUTs):** 16 CPU request/limit, 64 GiB RAM request/limit, 10 GiB ephemeral storage.
- **Placement (fixed):** SUT on cl-worker21, loading on cl-worker17, benchmarking on cl-worker19.
- **Observation:** SUT monitoring enabled (sidecar); cluster/app monitoring off.
- **Controls:** same query parameters across systems, same placement, same resource envelope, same tuning; bexhoma 0.10.8.

What changed: the SUT (PostgreSQL vs PgDuckDB) and the concurrency level (1 vs 2). What stayed fixed: workload, scale, tuning, resources, placement, and repetitions.

## Validity

The index frontmatter reports `overall_status: passed: 7, failed: 4, skipped: 1`.

**Failed (4) — all monitoring-CPU checks:**
- Loading phase: SUT deployment contains 0 or NaN in CPU [CPUs]
- Loading phase: component loader contains 0 or NaN in CPU [CPUs]
- Execution phase: SUT deployment contains 0 or NaN in CPU [CPUs]
- Execution phase: component benchmarker contains 0 or NaN in CPU [CPUs]

The Monitoring section confirms the sidecar recorded **0.00 CPUs / 0.00 Gb RAM** for every component in both phases. **Scope of impact:** resource-consumption metrics (CPU/RAM) are absent and must not be quoted. This does **not** touch the performance metrics.

**Passed (7):** No SUT container restarts; Geo Times [s] contains no 0/NaN; Power@Size [~Q/h] contains no 0/NaN; Throughput@Size contains no 0/NaN; No SQL errors; No SQL warnings; Workflow as planned.

**Skipped (1):** Loading phase data-generator CPU check (data pre-existing) — a skip never invalidates.

**Verdict on trustworthiness:** The run is sound for the questions asked. Correctness (no SQL errors/warnings), completeness of the three headline metrics, workflow fidelity, and SUT stability all passed. The only void area is resource monitoring, which is not needed to answer the system-choice or concurrency questions.

## Results

All figures from `report/index.md` (Key Metrics) and `report/execution.md` (Per Phase, Latency of Timer Execution [ms]).

**Headline metrics, single analyst (client 1, 1 pod), 3 runs:**

| System | Geo Times [s] | Power@Size [~Q/h] | Throughput@Size |
|---|---|---|---|
| PostgreSQL | 0.39 / 0.39 / 0.39 | 9297 / 9184 / 9311 | 2400 / 2329 / 2475 |
| PgDuckDB | 1.02 / 1.05 / 1.06 | 3516 / 3431 / 3388 | 1440 / 1366 / 1366 |

**Headline metrics, two analysts (client 2, 2 pods), 3 runs:**

| System | Geo Times [s] | Power@Size [~Q/h] | Throughput@Size |
|---|---|---|---|
| PostgreSQL | 0.39 / 0.40 / 0.39 | 9218 / 8912 / 9132 | 5110 / 4659 / 5110 |
| PgDuckDB | 1.06 / 1.06 / 1.08 | 3396 / 3395 / 3318 | 2731 / 2685 / 2640 |

**Per-query latency (single analyst, run 1, ms) — PostgreSQL vs PgDuckDB:** PostgreSQL is faster on 18 of 22 queries. PgDuckDB wins only Q1 (1549 vs 1957), Q13 (488 vs 1009), Q14 (919 vs 2200), and Q18 (1033 vs 3129). PostgreSQL's largest margins: Q21 (575 vs 3665), Q2 (202 vs 560), Q4 (178 vs 1311), Q19 (62 vs 986), Q20 (132 vs 1276).

**Concurrency scaling (mean Throughput@Size across 3 runs):**
- PostgreSQL: ~2401 (1 analyst) → ~4959 (2 analysts) = **2.07×** for 2× concurrency.
- PgDuckDB: ~1390 (1 analyst) → ~2685 (2 analysts) = **1.93×** for 2× concurrency.

Both scale near-linearly; PostgreSQL keeps its lead at both concurrency levels.

## Interpretation

**System choice (settled):** PostgreSQL is the correct recommendation for a 1 GB analytical reporting workload at 16c/64GiB. It beats PgDuckDB (forced DuckDB) on all three headline metrics — roughly 2.6× lower Geo Times, ~2.7× higher Power@Size, and ~1.7× higher Throughput@Size — and wins 18 of 22 individual queries. The hypothesis that PgDuckDB would win is **refuted** by the evidence.

**Concurrency robustness (settled):** The recommendation holds under concurrent analysts. At 2 analysts PostgreSQL still leads on every metric (Geo Times ~0.39–0.40s vs ~1.06–1.08s; Power@Size ~8911–9218 vs ~3318–3396 ~Q/h; Throughput@Size ~4659–5110 vs ~2640–2731, a ~1.85× lead). Both systems scale near-linearly with concurrency, and PostgreSQL preserves its ranking. The recommendation is concurrency-robust.

**Evidence vs mechanism:** The evidence establishes *that* PostgreSQL is faster and that the ranking is stable across 1→2 analysts. The *why* is inference, not measured here: PostgreSQL's per-query wins on join/aggregate-heavy TPC-H queries (Q2, Q4, Q21) are consistent with its tuned row-store + parallel workers handling this small, cache-resident dataset well, while the forced-DuckDB path in PgDuckDB appears to carry overhead on most queries (though it does win the four most scan/aggregate-heavy ones, Q1/Q13/Q14/Q18). Because resource monitoring failed, no CPU/RAM mechanism claim can be made from this run.

## Follow-up experiment

No completed follow-up is available in this chain. The single experiment (code `1787558149`) is the only run in the handoff; no prior-run follow-up is recorded.

## Final verdict

**Choose PostgreSQL** for a 1 GB analytical reporting workload under 16 CPU cores / 64 GiB RAM, and **the recommendation remains valid with concurrent analysts.** At TPC-H SF=1, PostgreSQL beats PgDuckDB (forced DuckDB) on Geo Times (~0.39s vs ~1.02–1.06s), Power@Size (~9184–9311 vs ~3388–3516 ~Q/h), and Throughput@Size (~2329–2475 vs ~1365–1440) at 1 analyst, and preserves that lead at 2 analysts (Throughput@Size ~4659–5110 vs ~2640–2731). Both scale near-linearly (PostgreSQL 2.07×, PgDuckDB 1.93× for 2× concurrency).

**Remaining limitations / unresolved questions:**
- **Resource-consumption metrics are unavailable** — all four monitoring-CPU checks failed (sidecar recorded 0.00 CPUs / 0.00 Gb RAM), so no CPU/RAM efficiency comparison can be drawn. If the decision hinges on resource footprint, a re-run with working monitoring is needed.
- **Concurrency tested only up to 2 analysts.** The "remains valid" claim is established for 1→2; behavior at higher concurrency (e.g., 4–8 analysts) is not measured.
- **Single scale point (SF=1).** The conclusion is specific to the ~1 GB workload; it is not extrapolated to larger datasets.
- **No cross-experiment comparison** was performed (per contract, comparisons are valid only within this experiment code).



Submitted successfully.

## Experiment code: `1787562545`

**What the run will settle:**

Whether PostgreSQL's lead over PgDuckDB (forced DuckDB) on the 1 GB TPC-H workload **persists at 4 concurrent analysts** — the point where PostgreSQL's parallel-worker demand (2 per gather × 4 queries = 8) exceeds the `analytical-ssd` profile's `max_parallel_workers=4` cap — or whether the gap narrows materially / the ranking flips.

**Design (all controls held fixed from the original `1787558149`):**
- **Only change:** `rounds` extended from `[1, 2]` → `[1, 2, 4]` (the concurrency sweep).
- **Fixed:** TPC-H SF=1, 300 s timeout, 2 query repeats, 3 repetitions; PostgreSQL vs PgDuckDB (`duckdb_force_execution: true`), both on `analytical-ssd`; 16 CPU / 64 GiB / 10 GiB; placement SUT=cl-worker21, loading=cl-worker17, benchmarking=cl-worker19; SUT monitoring on.
- **Scale:** 18 runs (2 systems × 3 rounds × 3 reps) — proportionate to the original 12-run design.

**Observable discriminator:** per-system Throughput@Size and Geo Times at the 4-analyst round.
- If PostgreSQL retains its ~1.85× throughput lead and near-linear scaling → the recommendation is **concurrency-robust beyond 2 analysts**.
- If the lead narrows materially or the ranking flips → the PostgreSQL recommendation is **valid only up to 2 concurrent analysts**.

The 1- and 2-analyst rounds are re-run as in-experiment controls, so the 4-analyst result is directly comparable within this single experiment code.
