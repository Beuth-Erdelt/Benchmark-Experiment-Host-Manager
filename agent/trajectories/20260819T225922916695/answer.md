

Submitted as experiment **1787173293**.

**What I designed:** A two-arm comparison on the same system (PgDuckDB) that isolates exactly one factor — pg_duckdb's `duckdb_force_execution` knob. Arm A forces every query through the DuckDB executor (`duckdb_force_execution: true`); arm B leaves cost-based routing at its default (`duckdb_force_execution: false`). Both arms share the identical `analytical-ssd` profile, so the only thing that varies is the routing choice.

**How it answers the question:**
- **Overall recommendation:** The summary metrics (Power@Size, Throughput@Size, Geo Times) per round give the headline comparison between forced vs. routed execution.
- **Consistency across query shapes:** `active_queries` defaults to all 22 TPC-H queries, and the workload produces per-query latency, so I can see whether the winner flips on individual queries (e.g., a join-heavy query favoring DuckDB while a simple one favors the Postgres executor).
- **Concurrency:** `rounds: [1, 8]` covers both requested stream counts, so I can check whether the recommendation holds at 1 and 8 concurrent streams.
- **Controls:** 16 CPU / 64 GiB RAM fixed at the user's ceiling (memory pressure isn't a plausible rival explanation at SF=1, so I kept it fixed rather than sweeping); `repetitions: 3` for run-to-run variance; `statistics: true` so the planner has cardinality estimates; all pods pinned to the only usable node, `cl-worker36`.

The design expands to 12 runs (2 systems × 2 rounds × 3 repetitions), which is small enough to run and large enough to draw a conclusion.
