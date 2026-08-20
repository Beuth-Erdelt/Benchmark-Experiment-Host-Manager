

I have what I need from the index (tier 1) and the execution provenance. Let me note the validity picture before interpreting, since the Tests table and Monitoring section in `index.md` are decisive here.

## Is the result trustworthy?

Partially. The run is **sound for performance, void for resource consumption**:

- **Valid:** `Workflow as planned` passed, `No SUT container restarts` passed, `No SQL warnings` passed, and all three headline columns (`Geo Times [s]`, `Power@Size [~Q/h]`, `Throughput@Size`) passed the "no 0 or NaN" check. So the timing/throughput numbers are complete and the sweep ran as designed (index.md, Tests table).
- **Void — monitoring:** Four monitoring tests **failed** (`Loading`/`Execution` × `SUT deployment` and `benchmarker` "contains 0 or NaN in CPU"), and the index.md Monitoring section shows every peak at **0.00 CPUs, 0.00 Gb RAM**. Monitoring recorded nothing, so **no CPU or RAM figure in this report can be believed**. This directly matters because your mechanism question (memory vs. threads) is exactly what monitoring was supposed to show.
- **Scoped — SQL errors:** 3 queries errored (index.md Health Summary; `SQL errors` row failed). Per the contract this voids the *per-query* metrics for those specific queries only. I could not read the Errors subsection to name them — `execution.md` is 194 KB and the read returns only the first 24 KB, which is entirely the provenance link list, so the Errors/Per-Phase tables sit past the truncation. It does not affect the system-level comparison below (a 4–7× gap is not moved by 3 errored queries out of ~1,200 executions per configuration).

## What it says about your question

**1. Is pg_duckdb better on joins, even under concurrency? No — clearly not.** From index.md Key Metrics (`Geo Times [s]`, geometric mean query time, across all 3 runs):

| Concurrency | PostgreSQL (32/64 Gi) | PgDuckDB (32/64 Gi) |
|---|---|---|
| 1 stream | 0.20–0.24 | 0.96–1.10 |
| 2 streams | 0.22–0.24 | 0.97–1.15 |
| 4 streams | 0.26–0.30 | 1.39–1.46 |
| 8 streams | 0.34–0.37 | 1.47–1.57 |

PostgreSQL is **~4–5× faster at 1 stream and ~4× faster at 8 streams**, and it stays faster at every concurrency level, both memory limits, and all 3 repetitions. On these multi-way TPC-H joins (Q5/7/8/9/21, SF=1) with DuckDB execution forced, PgDuckDB does not come close.

**2. Memory starvation or thread contention? Not memory starvation; consistent with thread/CPU contention — but the confirmation is indirect.** The experiment's built-in discriminator was the 32 Gi vs 64 Gi pair. At 8 streams the two are essentially identical for both systems:
- PostgreSQL: 32 Gi = 0.36/0.36/0.36 vs 64 Gi = 0.35/0.37/0.34
- PgDuckDB: 32 Gi = 1.53/1.57/1.47 vs 64 Gi = 1.54/1.55/1.55

If degradation were per-stream memory starvation, the 32 Gi column would be markedly worse than 64 Gi. It is not — so **memory is not the binding constraint**. The per-stream degradation itself is real but modest and symmetric: per-query latency rises ~1.5× from 1→8 streams for both systems (PG 0.23→0.36 s; PgDuck 1.0→1.5 s), and per-stream efficiency (`Power@Size`) drops ~30–40% (PG ~15,000→~10,000 ~Q/h; PgDuck ~3,500→~2,350 ~Q/h), again with no 32-vs-64 Gi split. That "same at both memory limits" signature is the thread/CPU-contention pattern, not the memory pattern.

**Caveat on the mechanism:** I can only *rule out* memory starvation and say the data is *consistent with* thread contention. I cannot *confirm* CPU saturation, because the monitoring that would show it recorded all zeros. (Minor confound: the 64 Gi configs also get larger `shared_buffers`/`work_mem`, so they're if anything more favorably tuned — yet show no speedup, which strengthens the "not memory" reading.)

## What the hypothesis got right / wrong

- **"PgDuckDB matches or beats PostgreSQL as streams scale 1→8"** — **wrong.** It is 4–5× slower throughout.
- **"Degradation is attributable to per-stream memory starvation (worse at 32 Gi than 64 Gi)"** — **wrong.** No 32-vs-64 Gi difference exists.
- **The implicit alternative — "degradation similar at both memory limits" (thread/CPU contention)** — **supported** by the data, though not positively confirmed due to the dead monitoring.

## What's missing

The one genuine gap is positive confirmation of the thread-contention mechanism: CPU-utilization data is void. If you want it nailed down rather than inferred, the clean follow-up is a **CPU-variation** run (e.g., 8 vs 16 CPU at a fixed 64 Gi) — if per-stream latency degradation at 8 streams gets worse at lower CPU, that confirms CPU/thread contention. I did not submit it, because your binary question is already answered by the 32/64 Gi result (not memory → of your two options, thread contention), and the broken monitoring would likely recur and still not yield CPU data. Say the word and I'll design and submit the CPU-variation follow-up.
