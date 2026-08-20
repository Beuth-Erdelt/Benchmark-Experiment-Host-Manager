

The specification validated on the first attempt. Here's what I designed and how it answers the question:

**Design:** A head-to-head run of **PostgreSQL vs PgDuckDB** on **TPC-H at scale factor 10** (your 10GB dataset), restricted to the multi-way join queries **Q5, Q7, Q8, Q9, Q21** — the catalog's own join subset — so the measured latencies and summary metrics (Power@Size, Geo Times) speak directly to join performance rather than being diluted by scan-only queries.

**Concurrency:** Rounds sweep **1 → 2 → 4** parallel client streams. Four is the official TPC-H concurrency for SF=10 (floor(log₃(10))+2), so the sweep covers "no concurrency" through the workload's rated load, which is exactly the "even under concurrency" part of your question.

**Fairness (everything else held equal):** Both systems use the same `analytical-ssd` profile (PgDuckDB's is a ref to PostgreSQL's, so knob values resolve identically from the same resource limits), the same shared `post_load` (ANALYZE/statistics on, no indexes/constraints for either), the same 8 CPU / 32Gi memory / 50Gi storage cell, and the same query set. 32Gi sits comfortably under your 64GB server cap and comfortably holds the 10GB working set. I left `storage_class` unset (the profile permits it → node-local storage) and omitted placement, since no environment descriptor was available to name nodes or storage classes.

**Reliability:** `query_repeats: 3` gives three samples per query per round, `verify_result: true` sanity-checks that both engines return correct rows, and SUT monitoring is on to explain any divergence (e.g., memory pressure at 4 streams).

**Cost:** 6 benchmark runs (2 systems × 3 rounds), each ~15 query executions — a design that finishes in a reasonable window. The per-query latency breakdown plus per-phase summary metrics will show whether pg_duckdb wins on joins at concurrency 1 and whether that gap holds, shrinks, or inverts at 2 and 4 streams.
