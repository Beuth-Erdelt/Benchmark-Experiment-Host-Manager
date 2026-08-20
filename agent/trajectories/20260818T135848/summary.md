

The specification validated on the first attempt. Here's what I designed and why it answers the question:

**Experiment:** `inbox/pgduckdb-joins-concurrency.yml` — a head-to-head of **PostgreSQL vs PgDuckDB** on the TPC-H workload, expanded to **6 benchmark runs** (2 systems × 3 concurrency rounds), which is a small, runnable design.

**How it maps to your question:**
- **Joins:** `active_queries: [5, 7, 8, 9, 21]` — the catalog's multi-way-join subset, so the comparison is about join performance, not the full 22-query suite.
- **10GB dataset:** `scaling_factor: 10`.
- **64GB RAM cap:** both systems get an identical `memory: 64Gi` request/limit, and the shared `analytical-ssd` profile derives all memory knobs (shared_buffers, work_mem, etc.) from that same limit, so the two systems are tuned to the same budget.
- **"Even under concurrency":** `rounds: [1, 2, 4]` sweeps parallel clients from serial up to the TPC-H rule-of-thumb maximum for SF=10 (floor(log₃(10))+2 = 4), so you get the system effect at each concurrency level — the answer can flip between rounds, and the per-round summary metrics (Power@Size, Throughput@Size, Geo Times) plus per-query latencies will show exactly where.

**Fairness controls:** the only varying factor is the system. Both use the same profile (PgDuckDB's `analytical-ssd` refs PostgreSQL's, so knob values resolve identically), the same 8 CPU / 64GiB / 50Gi node-local storage limits, the same node (pinned to cl-worker27, which has ample CPU/RAM/disk), the same post-load step (ANALYZE statistics only — no indexes or constraints, which don't help scan-heavy joins and would add load-time asymmetry), and PgDuckDB runs with its default cost-based routing, i.e., the configuration you'd actually deploy. `query_repeats: 2` gives two samples per query for statistical stability and keeps rounds long enough for SUT monitoring to warm up.

If the results are close, the one allowed follow-up could re-run with `duckdb_force_execution: true` on PgDuckDB to isolate the DuckDB engine itself from its cost-based router.
