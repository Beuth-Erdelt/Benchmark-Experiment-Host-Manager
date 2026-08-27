

Submitted as experiment **1787796951**.

**What I designed:** A TPC-H SF3 comparison of PostgreSQL vs PgDuckDB under identical 16 CPU / 64 GiB SUT limits, sweeping 1 and 2 concurrent query streams, with 3 repetitions (12 total runs).

**How it answers the question:**
- **Which system is faster** — the `system` factor isolates PostgreSQL vs PgDuckDB. I set `duckdb_force_execution: true` on PgDuckDB, which the catalog requires whenever comparing its engine against another system; otherwise pg_duckdb's cost-based routing would keep queries in Postgres' executor and we'd be measuring PostgreSQL against itself. Both systems use the same `analytical-ssd` profile (PgDuckDB's `ref:`s PostgreSQL's, so they resolve identical knobs from the same limits), the same node, and the full 22-query workload — so the only thing that varies is the system.
- **Ranking stability 1→2 streams** — the `concurrency` factor is the `rounds: [1, 2]` sweep. Comparing the per-phase Geo Times / Throughput@Size ranking at 1 stream vs 2 streams across the 3 repetitions shows whether the winner holds as concurrency doubles.
- **SF3 as requested** — it validated cleanly against the catalog and environment, so no fallback to SF1 was needed.

The 2640-minute figure in the estimate is a conservative worst-case deadline budget (22 queries × 600s × 12 runs), not a runtime prediction; real queries finish well before the per-query timeout.
