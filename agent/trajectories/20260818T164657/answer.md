

Designed experiment **1787064464**: a head-to-head of PostgreSQL vs PgDuckDB on the TPC-H multi-way join subset (Q5, Q7, Q8, Q9, Q21) at scale factor 10 (the 10GB dataset), sweeping concurrency from 1 to 4 parallel client streams (the catalog's rule-of-thumb max for SF10) with 3 repetitions for statistical confidence.

How it answers the question:
- **Joins**: `active_queries` is restricted to the five multi-way join queries, so the per-query latency and summary metrics isolate join performance.
- **Concurrency**: the `rounds: [1, 2, 4]` sweep shows whether any pg_duckdb advantage holds or erodes as parallel streams grow — the "even under concurrency" part.
- **Your 64GB RAM cap**: both containers are hard-limited to 64Gi memory (16 CPUs), so the comparison reflects your server constraint rather than the 2TB node; SUT monitoring is on to confirm memory headroom.
- **Fairness**: both systems use the same `analytical-ssd` profile (PgDuckDB's refs PostgreSQL's, so knobs resolve identically from the same limits), the same node-local storage, the same 100Gi volume, and a shared post-load step with ANALYZE statistics; pg_duckdb's cost-based routing is left at its default so the comparison is of the systems as deployed.

The result will be 18 benchmark runs (2 systems × 3 concurrency levels × 3 reps), each producing per-query latencies and Power@Size/Geo Times summaries — enough to say whether pg_duckdb wins on joins and whether that win survives concurrency.
