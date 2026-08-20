

I designed a head-to-head TPC-H experiment (filed under code **1787064693**) that answers the question directly:

- **Join factor**: TPC-H at scale factor 10 (your 10GB dataset), restricted to the multi-way join queries Q5, Q7, Q8, Q9, Q21, with result verification on.
- **Concurrency factor**: a parallel-client sweep of 1, 2, and 4 concurrent streams — 4 being the TPC-H rule-of-thumb maximum for SF10 — so the results show whether any pg_duckdb advantage survives as concurrency rises.
- **System factor**: PostgreSQL vs PgDuckDB, both on the shared `analytical-ssd` profile (PgDuckDB's profile refs PostgreSQL's, so every knob resolves identically from the same limits), with ANALYZE run after load for both and no indexes/constraints, so the only things that vary are the system and the concurrency level.
- **Your hardware constraint**: both systems are capped at 64Gi memory and 16 cores on node-local storage, emulating your 64GB-RAM servers; SUT monitoring is on to confirm the cap is actually binding.
- **Statistical soundness**: 3 repetitions per (system, concurrency) cell, giving 18 benchmark runs total — enough to separate a real difference from run-to-run variance.

The per-query latencies and per-phase summary metrics (Geo Times, Throughput@Size) across the 2×3 grid will show whether pg_duckdb wins on joins at all, and whether that win persists or erodes under concurrency.
