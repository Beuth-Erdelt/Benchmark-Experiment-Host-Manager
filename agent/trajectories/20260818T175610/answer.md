

I've read the report index, the result contract, and the execution evidence. Here's the interpretation.

## Trustworthiness

**The timing data is trustworthy; the resource-consumption data is not.** The Tests table in `report/index.md` shows 7 passed, 4 failed, 1 skipped. All four failures are monitoring checks — "SUT deployment contains 0 or NaN in CPU [CPUs]" (loading and execution) and the same for the loader and benchmarker — and the Monitoring section confirms every peak is 0.00 CPUs / 0.00 Gb RAM. So Prometheus recorded nothing, and no CPU/RAM figure from this run can be quoted. The one skipped test (data generator, data pre-existing) invalidates nothing per the contract.

Everything that matters for the performance question passed: no SUT container restarts, no SQL errors, no SQL warnings (i.e., both systems returned matching results for every query), "Workflow as planned" (the 1/2/4-pod sweep actually ran as intended, confirmed by `pod_count` in the Per Phase table of `report/execution.md`), and all three key-metric columns contain no 0/NaN. The queries demonstrably ran and produced correct results, so the run is sound for latency purposes.

## What it says about the question

**No — pg_duckdb is not better than PostgreSQL on these joins, and there is no advantage to persist under concurrency. The two systems are a statistical tie, with a slight edge to PostgreSQL on most queries.**

Geometric mean query time (Geo Times [s], `report/index.md` Key Metrics / `report/execution.md` Per Phase), across the 3 repetitions:

| Concurrency | PgDuckDB (runs 1–3) | PostgreSQL (runs 1–3) |
|---|---|---|
| 1 stream | 0.24 / 0.26 / 0.30 | 0.23 / 0.27 / 0.30 |
| 2 streams | 0.24 / 0.28 / 0.30 | 0.24 / 0.27 / 0.26 |
| 4 streams | 0.30 / 0.34 / 0.35 | 0.30 / 0.34 / 0.33 |

Both systems degrade in the same way as concurrency rises (roughly 0.24–0.27 s at 1 stream to 0.30–0.35 s at 4 streams) and stay within ~0.02 s of each other at every level.

Per-query means over all 21 connections per system (3 runs × 1/2/4 streams, from the Latency table in `report/execution.md`):

- Q5: PgDuckDB ~324 ms vs PostgreSQL ~313 ms
- Q7: PgDuckDB ~323 ms vs PostgreSQL ~288 ms
- Q8: PgDuckDB ~131 ms vs PostgreSQL ~122 ms
- Q9: PgDuckDB ~513 ms vs PostgreSQL ~573 ms (the only query where pg_duckdb is clearly ahead, ~10%)
- Q21: PgDuckDB ~416 ms vs PostgreSQL ~398 ms

PostgreSQL is faster or tied on 4 of the 5 join queries; pg_duckdb wins only Q9. (The Throughput@Size column differences, e.g. 14400 vs 9000 for phase `*-2-3`, are wall-clock artifacts of phase duration — 20 queries ÷ phase time — not per-query differences; the per-query latencies are comparable.)

The setup matches your constraints: SF=1 (1 GB), 64 Gi RAM and 16 CPU limits on both systems, identical tuning (shared_buffers 20480 MB, work_mem 1024 MB, etc.), so the comparison is apples-to-apples within this experiment code.

## What the hypothesis got right or wrong

The hypothesis — that pg_duckdb executes Q5/Q7/Q8/Q9/Q21 faster than native PostgreSQL and that the advantage persists from 1 to 4 concurrent streams — is **not supported**. It got the experimental framing right (the right queries, the right concurrency sweep, the right resource caps), but the predicted advantage does not exist in the data: the systems are indistinguishable at 1 stream and remain indistinguishable at 4. If anything, the point estimates lean slightly toward PostgreSQL.

## Follow-up experiment

Re-run the identical experiment with the concurrency sweep extended to **8 and 16 streams** (rounds [8, 16], same SF=1, same 16 CPU / 64 Gi caps, same tuning), and fix the monitoring scrape so CPU/RAM are actually recorded. Four streams is a modest load and the tie there is within noise; 8–16 streams is where pg_duckdb's architecture (one DuckDB engine per backend, limited cross-query parallelism) is most likely to diverge from PostgreSQL's parallel-query backends. This would settle whether the tie holds or breaks under genuinely heavy concurrency — the part of "even under concurrency" that this run did not fully exercise — and would simultaneously deliver the resource-consumption comparison this run's failed monitoring checks left missing.
