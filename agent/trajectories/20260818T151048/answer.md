

I've read the report index, the execution and connections evidence it links to, and the result contract. Here's my interpretation.

## Is the result trustworthy?

**Partially — the PgDuckDB side is clean, the PostgreSQL side has a hard failure, and monitoring is empty for both.**

- **SQL errors (absolute check, FAILED for PostgreSQL):** PostgreSQL logged 3 errors and completed only 4 of 5 queries. Query 21 exceeded the timeout in *every* repetition and was recorded as failed (the note says 3600 s, though the experiment spec says `timeout: 600` — an inconsistency worth noting, though it doesn't change the outcome). PgDuckDB had 0 errors and completed 5 of 5.
- **SUT restarts:** 0 for both systems, so no mid-run restarts or OOM kills — a genuine pass.
- **Monitoring (absolute check, failed/skipped):** 0 samples for *both* systems. The run was long (3 rounds × 3 repetitions of multi-second queries), so this is not the "phase shorter than one scrape interval" skip case — monitoring simply recorded nothing. Consequence: the 64 Gi memory cap, which is the crux of your deployment constraint, was never observed. We cannot confirm either system stayed under the cap or how close it got.
- **Comparability of the headline table:** because query 21 never completed on PostgreSQL, the index headline (Power@Size 6854, Throughput@Size 4120, geo-mean 0.53 s) is computed over **4 queries**, while PgDuckDB's (9930, 5871, 0.36 s) is over **5**. The two headline rows are not on an identical query set. Also, the index geo-mean (0.53 s) is not the geo-mean of the per-query means in execution.md (which would be ≈0.76 s for PostgreSQL), so the two tables use different aggregations; I rely on the per-query table.

## What it says about your question

On the four join queries that completed on both systems, **PgDuckDB was faster on every single one**: Q5 0.44 s vs 0.71 s (1.6×), Q7 0.39 s vs 0.66 s (1.7×), Q8 0.31 s vs 0.58 s (1.9×), Q9 0.68 s vs 1.24 s (1.8×). And on the query that broke PostgreSQL — Q21, the self-join-heavy one — PgDuckDB finished in 0.91 s while PostgreSQL never finished within the timeout. The headline power/throughput gap is ~1.4–1.5× (9930 vs 6854 ~Q/h; 5871 vs 4120), and since PostgreSQL's numbers exclude its worst query, that ratio *understates* the gap on the full set.

**What it does not settle:** the "even under concurrency" half. The experiment ran rounds at 1, 2, and 4 clients, but the report gives no per-round breakdown — only aggregates. So the persistence of the advantage as concurrency rises is supported only in aggregate, not level by level. And with zero monitoring samples, we can't say whether the 64 Gi cap was ever binding, which matters for a 10 GB dataset where PostgreSQL's Q21 timeout suggests it was struggling.

## What the hypothesis got right or wrong

- **Right:** PgDuckDB achieves lower per-query latency and higher throughput than vanilla PostgreSQL on the join-heavy TPC-H queries, and the aggregate advantage holds across the 1→4 client rounds.
- **Not verified:** that the advantage *persists as concurrency rises* — the per-concurrency breakdown is absent from the report.
- **Beyond the hypothesis:** PostgreSQL's total failure on Q21 (timeout in all 3 repetitions) was not predicted and is the single biggest finding — it's a qualitative difference, not just a speed difference.

## Proposed follow-up

**Re-run the same experiment (TPC-H SF=10, queries 5/7/8/9/21, rounds 1/2/4, 3 repetitions, 64 Gi cap) with two fixes: monitoring actually working, and a per-round (per-concurrency-level) breakdown in the report, plus a raised timeout for PostgreSQL so Q21 can complete (or, if it still can't, explicitly drop Q21 from both systems).** This would settle the two open questions at once: whether the PgDuckDB advantage holds at each concurrency level (1, 2, 4 clients) rather than only in aggregate, and whether the 64 Gi cap is ever close to being hit — i.e., whether the result you'd see on your real servers matches what this run showed.
