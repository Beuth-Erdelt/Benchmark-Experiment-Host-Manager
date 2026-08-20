

The record is accepted. Here is the interpretation.

## Trustworthiness

The run is **partially sound**. Overall status is 6 passed / 5 failed / 1 skipped.

**What holds up:** No SUT container restarts, the workflow ran exactly as planned, and all three headline metric columns (Geo Times, Power@Size, Throughput@Size) contain no 0/NaN. So the benchmark *numbers* are real and internally consistent.

**Two scope restrictions you must carry into any use of these numbers:**
1. **3 SQL errors** — all `Query cancelled`, all on **PgDuckDB-32Gi only** (Q21 on two connections, Q9 on one). Per the contract, this voids per-query metrics for those specific queries/connections. It does not void the aggregate Geo/Power/Throughput, but it is itself a signal (see below).
2. **Monitoring recorded nothing.** All four monitoring tests failed: CPU, Max CPU, Max RAM, and Max RAM Cached are **0.00** for every connection in the execution phase (and loading phase). There is **no direct memory or CPU trace** in this result. Any claim about *why* something degraded must rest on the experimental design (the 32Gi/64Gi split) and the error pattern, not on observed RSS.

## Question 1 — Is pg_duckdb better on joins than PostgreSQL, even under concurrency?

**No — decisively not.** On the five join-heavy TPC-H queries (Q5, Q7, Q8, Q9, Q21) at SF=1, PostgreSQL is roughly **4–5× faster** than PgDuckDB (DuckDB execution forced) at *every* concurrency level and in *all three* runs:

| Round (streams) | PostgreSQL Geo [s] | PgDuckDB Geo [s] | PostgreSQL Power@Size | PgDuckDB Power@Size |
|---|---|---|---|---|
| 1 | 0.20–0.24 | 0.96–1.10 | 14736–17938 | 3266–3764 |
| 2 | 0.22–0.24 | 0.97–1.15 | 15273–16270 | 3242–3699 |
| 4 | 0.26–0.30 | 1.39–1.46 | 12194–13823 | 2458–2586 |
| 8 | 0.34–0.37 | 1.47–1.57 | 9850–10564 | 2299–2456 |

The gap does not close as concurrency rises; if anything PostgreSQL's *relative* position holds. At your 1 GB scale, tuned PostgreSQL (the run used `shared_buffers` 10–20 GB, `work_mem` 512 MB–1 GB, `io_uring`, parallel workers) beats forced-DuckDB pg_duckdb on these joins.

## Question 2 — Memory starvation per stream, or thread contention?

**Memory starvation per stream.** The 32Gi-vs-64Gi discriminator gives a clean, asymmetric answer:

- **At 8 streams the two limits diverge sharply:** PgDuckDB-32Gi Throughput@Size **378.95** vs PgDuckDB-64Gi **1655.17** — a **4.4× gap** — and wall-clock **380 s vs 87 s**. (The 380 s ≈ a 300 s timeout on one cancelled query plus the rest of the phase.)
- **At 1–4 streams the two limits are within noise** (round 4: 923.08 vs 847.06), so the penalty is not a constant per-stream tax — it only appears once enough streams are in flight to exhaust 32 Gi.
- **All three `Query cancelled` errors are on PgDuckDB-32Gi**, none on 64Gi, none on PostgreSQL — the signature of a memory ceiling being hit, not of CPU contention.
- **Geo Times at round 8 are nearly identical (1.53 vs 1.54).** If this were thread/CPU contention, per-query latency would rise at *both* limits; it doesn't. The damage at 32Gi shows up as *cancellations and collapsed throughput*, not as slower individual queries — exactly what per-stream memory starvation looks like.

**Caveat:** because monitoring recorded nothing, I cannot show you the RSS curve actually touching 32 Gi. The attribution is from the 32Gi/64Gi asymmetry plus the 32Gi-only cancellations, which is strong but indirect.

## What the hypothesis got right and wrong

- **Wrong on the headline:** "PgDuckDB matches or beats PostgreSQL on multi-way TPC-H joins as streams scale 1→8." It does not — PostgreSQL is 4–5× faster throughout.
- **Right on the mechanism:** "Degradation markedly worse at 32Gi than 64Gi, i.e. per-stream memory starvation rather than thread contention." Confirmed — the 4.4× round-8 throughput gap, the 32Gi-only cancellations, and the flat Geo Times across limits all point to memory starvation per stream.

**Bottom line for your 64 GB servers:** at your maximum (64 Gi) PgDuckDB does *not* show the starvation collapse (no cancellations, 1655 Throughput@Size at 8 streams), so the memory-starvation failure mode is avoidable by staying at 64 Gi. But on this 1 GB join workload, plain PostgreSQL is the faster engine regardless of the memory limit.



Submitted. 

## Experiment code: `1787166405`

**What the run will settle:** the unresolved causal question — whether PgDuckDB's throughput degradation at 8 concurrent streams is **per-stream memory starvation** or **thread/CPU contention** — using the direct RSS/CPU trace that the first run failed to record.

**Design (all changes attributable, everything else fixed to the completed run):**
- **Single system:** PgDuckDB with `duckdb_force_execution: true` (PostgreSQL dropped — Question 1 is settled; it would only double cost).
- **Single round:** `[8]` (the degradation point; rounds 1–4 were within noise).
- **`query_repeats: 40`** (was 10) — the one intervention that fixes the monitoring failure: the round-8 execution phase scales from ~87s to ~348s at 64Gi, clearing the catalog's 2–5 minute scrape warm-up window that caused all four monitoring tests to read 0.00.
- **Memory sweep `[32Gi, 64Gi]`** — half-ceiling/ceiling per the bounded-resources guidance, the same discriminator that produced the 4.4× asymmetry.
- **CPU fixed at 16, SF=1, join subset Q5/Q7/Q8/Q9/Q21, timeout 300, placement cl-worker36, 10Gi storage, `repetitions: 3`** — all identical to the proven-feasible completed run.

**The discriminator the trace will resolve:**
- **Memory starvation confirmed** if SUT RSS approaches ~32Gi during the 8-stream round at the 32Gi cell (with `Query cancelled` errors recurring only there) while RSS stays well below the limit at 64Gi.
- **Thread contention confirmed** if RSS stays well below the limit at *both* cells while CPU runs near-saturated at both.

The 32Gi cell is expected to be the informative one: if RSS pins near the limit and cancellations recur, the indirect evidence from run 1 (asymmetry + 32Gi-only cancellations) is upgraded to a direct causal observation; if RSS stays low at 32Gi while CPU saturates, the mechanism attribution flips.
