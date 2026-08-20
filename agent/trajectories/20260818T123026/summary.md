

The specification validated on the first check. Here's what I designed and why it answers the question:

**Experiment: pg_duckdb vs PostgreSQL on TPC-H join queries under concurrency (SF10, 64Gi)**

- **Workload:** TPC-H at `scaling_factor: 10` (your 10GB dataset), restricted to the join-heavy queries `[5, 7, 8, 9, 21]` so the comparison is about joins, not the full 22-query suite.
- **Concurrency:** `rounds: [1, 2, 4]` — a parallel-client sweep from serial up to 4 concurrent streams, which is the TPC-H rule-of-thumb concurrency for SF10 (floor(log₃(10))+2 = 4). This directly tests "even under concurrency" by showing the system comparison at each level.
- **Systems:** PostgreSQL and PgDuckDB, both on the `analytical-ssd` profile (PgDuckDB's profile refs PostgreSQL's, so both resolve identical knob values from the same limits). PgDuckDB runs with its default cost-based routing — no forced execution — so you're comparing the system as you'd actually deploy it.
- **Your hardware constraint:** memory capped at `64Gi` (matching your 64GB servers), 16 CPU, 30Gi node-local storage (no PVC, per the profile's storage requirement). The profile's derived knobs scale from that limit (e.g., shared_buffers 20Gi, effective_cache_size 48Gi), so the 10GB dataset is memory-resident, as on your servers.
- **Fairness:** everything else is held equal — same node (cl-worker21, pinned for SUT, loader, and benchmarker), same resources, same post-load physical design (ANALYZE/statistics enabled on both so both planners have estimates; no indexes, since TPC-H joins are scan-bound).
- **Cost:** 6 benchmark runs (2 systems × 3 rounds), a quick, decisive comparison.

The results will give per-query latency and summary throughput (Power@Size, Geo Times) per system per concurrency level, so you'll see both whether pg_duckdb wins on joins and whether that win holds or erodes as concurrency climbs.
