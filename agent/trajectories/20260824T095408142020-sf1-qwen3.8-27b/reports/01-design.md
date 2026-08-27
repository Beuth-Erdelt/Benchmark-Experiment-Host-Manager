

Submitted as experiment **1787558149**.

**What I designed and how it answers the question:**

I built a 2-system, 2-concurrency-level TPC-H experiment at scale factor 1 (the 1 GB analytical reporting workload) under a fixed 16-core / 64 GiB budget, comparing the only two systems the catalog supports for TPC-H: **PostgreSQL** and **PgDuckDB**.

- **System factor:** Both run the identical `analytical-ssd` profile (PgDuckDB's profile refs PostgreSQL's, so every derived knob — shared_buffers, work_mem, effective_cache_size, parallelism — resolves to the same values from the same 64 GiB / 16-core limits). The one deliberate difference is `duckdb_force_execution: true` on PgDuckDB, which the catalog requires when comparing its engine against another system; without it, pg_duckdb's cost-based routing would keep queries in Postgres' own executor and I'd be measuring Postgres against itself.
- **Concurrency factor:** `rounds: [1, 2]` — one analyst versus two concurrent analysts (2 is the TPC-H rule-of-thumb stream count for SF=1). This directly tests whether the single-analyst recommendation holds under concurrent load.
- **Controls held equal:** same node-local storage (no `ssd` class exists in the environment, and the profile permits it), same `post_load: statistics: true` (ANALYZE) for both, no indexes (analytical = sequential scans), same 16c/64GiB cell, and 3 repetitions so a real difference is distinguishable from run-to-run variance.

The experiment produces per-query latency plus the summary metrics (Throughput@Size, Geo Times) per (system, round, repetition), so the results will show which system wins at 1 analyst, whether that ranking flips at 2 analysts, and how much each degrades under concurrency — answering both halves of the question in one 12-run design.
