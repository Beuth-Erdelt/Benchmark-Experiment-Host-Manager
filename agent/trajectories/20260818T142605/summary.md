

Validation passed on the first try. Here's what I designed:

**Experiment**: `inbox/pgduckdb-joins-concurrency.yml` — a head-to-head of **PostgreSQL vs PgDuckDB** on the TPC-H **multi-way join queries (5, 7, 8, 9, 21)** at **scale factor 10** (your 10GB dataset), with a **concurrency sweep of 1, 2, 4 parallel clients** (4 is the catalog's rule-of-thumb max for SF=10) and **3 repetitions** per cell, so the design expands to **18 runs** — a size that's actually runnable.

**How it answers the question**:
- The only varying factors are `system` and `concurrency` (both declared in `discriminates`). Everything else is held equal: both systems use the `analytical-ssd` profile (PgDuckDB's is a direct `ref` to PostgreSQL's, so they resolve identical memory-derived knobs like `shared_buffers`/`work_mem` from the same limits), the same shared `post_load` (ANALYZE on, no indexes, heap storage — both systems support it), and identical 16 CPU / 64Gi memory / 50Gi node-local storage requests.
- The **64Gi memory cap** mirrors your "at most 64GB of RAM" servers, so the result transfers to your hardware rather than the 2TB node it runs on.
- PgDuckDB runs with its **default cost-based routing** (not forced execution), which is the honest "is pg_duckdb better" comparison as the system actually ships.
- `verify_result: true` sanity-checks that pg_duckdb's join results are correct, and SUT/cluster monitoring is enabled to catch memory pressure at 4-way concurrency.

The per-query latencies and summary metrics (Geo Times, Throughput@Size) per system × round will directly show whether pg_duckdb's join advantage holds or erodes as concurrency climbs. A natural follow-up, if the default-routing result is ambiguous, would be re-running with `duckdb_force_execution: true` to isolate the DuckDB engine itself.
