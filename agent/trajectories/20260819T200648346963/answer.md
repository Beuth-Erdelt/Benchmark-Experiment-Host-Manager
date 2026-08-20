

I have what I need. The 3 SQL errors are all sporadic "Query cancelled" on PgDuckDB-32Gi (Q21 twice, Q9 once) — a weak signal of occasional memory pressure, not systematic. The Key Metrics table in the index already gives me the per-phase (per-round) numbers I need. Let me verify my reading of the concurrency degradation and the 32Gi-vs-64Gi comparison is complete before I answer.

The data is clear. Let me lay out what it means.

## Trustworthiness

The benchmark numbers themselves are sound. The three headline columns (Geo Times, Power@Size, Throughput@Size) all passed the "no 0 or NaN" check, the workflow ran as planned, there were no SUT container restarts, and no SQL warnings (result mismatches). So the timing/throughput figures are complete and internally consistent.

Two caveats scope what I can claim:
- **Monitoring is entirely broken.** All four monitoring tests failed, and every monitored component (SUT, loader, benchmarker) reads 0.00 CPUs / 0.00 Gb RAM in both the loading and execution phases. This is a cluster-wide monitoring failure, not something the spec can fix. Consequence: I have **no direct observation of memory or CPU usage**. I cannot confirm that the 32Gi limit was actually binding, nor that CPUs were saturated.
- **3 sporadic SQL errors**, all "Query cancelled" on PgDuckDB-32Gi (Q21 at runs 1-4 and 2-2, Q9 at run 3-4). These are 3 of ~1200 PgDuckDB query executions and only on the 32Gi config — a weak hint of occasional memory pressure, but not a systematic effect.

## What it says about the original question

**1. Is pg_duckdb better on joins under concurrency? No — decisively not.** PostgreSQL is faster at every concurrency level and in both memory configs. Using Power@Size (higher = better), averaged across the 3 repetitions:

| Round (streams) | PostgreSQL (32/64Gi) | PgDuckDB (32/64Gi) | PG advantage |
|---|---|---|---|
| 1 | ~15,500–16,000 | ~3,300–3,700 | ~4.5× |
| 2 | ~15,300–15,800 | ~3,100–3,700 | ~4.5× |
| 4 | ~12,700–13,800 | ~2,450–2,600 | ~5× |
| 8 | ~10,000–10,400 | ~2,300–2,450 | ~4.3× |

In per-query latency (Geo Times, lower = better) PostgreSQL holds ~0.22–0.37 s while PgDuckDB holds ~0.96–1.57 s. The gap is stable at roughly **4–5× in PostgreSQL's favor** from 1 to 8 streams. Forcing DuckDB execution did not close it.

**2. Memory starvation or thread contention?** The evidence points to **thread/CPU contention, not per-stream memory starvation** — but with an important weakness. The designed discriminator was "degradation markedly worse at 32Gi than 64Gi if memory-bound; similar at both if thread-bound." What I see is *similar* degradation at both limits:
- PostgreSQL Geo Times: 0.23 → 0.23 → 0.26 → 0.36 s (≈1.5× from 1 to 8 streams), essentially identical at 32Gi and 64Gi.
- PgDuckDB Geo Times: 1.01 → 1.15 → 1.39 → 1.53 s (≈1.5×), again essentially identical at 32Gi and 64Gi.
- Power@Size falls ~30–37% from round 1 to round 8 for **both** systems and **both** memory limits.

No configuration shows the "markedly worse at 32Gi" signature the memory-starvation branch predicted. That is consistent with thread/CPU contention (or generic concurrency overhead) rather than memory.

**The weakness:** for a 1 GB dataset, 32Gi is very likely *not* a binding constraint, so "no difference between 32Gi and 64Gi" is the expected result even if memory were the mechanism — the test simply never stressed memory hard enough to discriminate. And because monitoring is dead, I can't confirm either that 32Gi was binding or that CPUs were saturated. So the mechanism is *indicated* (thread contention) but not *proven*.

## What the hypothesis got right / wrong

The hypothesis is wrong on both counts:
- **"PgDuckDB matches or beats PostgreSQL"** — false. PostgreSQL is ~4–5× faster across the whole sweep.
- **"Degradation is memory starvation (worse at 32Gi) rather than thread contention (similar at both)"** — the data shows the *similar-at-both* pattern, i.e. the thread-contention branch, not the memory-starvation branch. So the mechanism attribution is also wrong (it is not memory starvation).

## Practical bottom line for your 64 GB / 1 GB-dataset servers

Memory is not your bottleneck. A 1 GB dataset across 8 concurrent streams is on the order of single-digit GB of working set — it fits comfortably in 64 GB (and even 32 GB). The ~1.5× per-query slowdown as you go from 1 to 8 streams is the cost of sharing CPUs/threads, not of running out of RAM. If you want to buy back throughput under concurrency, the lever is CPU (and how the engine schedules parallel work), not more RAM.

## On a follow-up

I'm **not** spending the follow-up. The headline question (pg_duckdb vs PostgreSQL on joins) is settled, and the mechanism question already points the right way for your actual deployment (1 GB data, 64 GB RAM → not memory-bound). A follow-up would only try to *prove* the thread-contention mechanism by forcing a binding memory limit (e.g. 8Gi vs 64Gi), but (a) the cluster-wide monitoring that would let me observe memory/CPU directly is broken and can't be fixed from a spec, and (b) a low enough limit to be binding risks OOM-killing the heavy join queries (Q9/Q21), which would invalidate the comparison rather than clarify it. The marginal value doesn't justify the risk. If you later want the mechanism nailed down, the clean fix is to repair the cluster monitoring first, then re-run with a deliberately binding memory limit so the 32/64Gi (or 8/64Gi) contrast is actually informative.

**Key numbers cited** (from `report/index.md` Key Metrics table): PostgreSQL Power@Size ≈ 15,993/16,077 (round 1) down to ≈ 10,122/10,398 (round 8) at 32/64Gi; PgDuckDB ≈ 3,572/3,355 (round 1) down to ≈ 2,350/2,345 (round 8); PostgreSQL Geo Times 0.22–0.37 s vs PgDuckDB 0.96–1.57 s. SQL errors: 3 "Query cancelled," all PgDuckDB-32Gi (`report/execution.md`, Errors subsection).
