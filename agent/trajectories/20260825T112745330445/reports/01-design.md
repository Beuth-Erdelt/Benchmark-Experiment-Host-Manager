

The experiment is submitted and running under code **1787650143**.

**What I designed:** A retry of the 10 GB TPC-H comparison between PostgreSQL and PgDuckDB with `duckdb_force_execution: true` (so every query goes through DuckDB's engine rather than pg_duckdb's cost-based routing, which would otherwise leave the extension idle and measure PostgreSQL against itself).

**How it answers the question:**
- **Fixed budget**: both systems get identical 16 CPU cores and 64 GiB RAM (request = limit), on the same node (cl-worker17, the only node with enough allocatable memory), with node-local storage — the only thing that varies is the system, plus the concurrency factor.
- **Comparable configuration**: both use the `analytical-ssd` profile (PgDuckDB's profile refs PostgreSQL's, so all derived knobs — shared_buffers, work_mem, effective_cache_size, parallelism settings — resolve identically from the same limits), and both get the same post-load treatment (ANALYZE statistics, heap storage, no indexes/constraints).
- **Design**: TPC-H SF=10, rounds of 1, 2, and 4 concurrent streams, 3 repetitions each, with result verification on — 18 runs total, a size that's runnable and gives 3 samples per (system, stream) cell to separate real differences from run-to-run variance.

The per-query latencies and per-phase summary metrics (Power@Size, Throughput@Size, Geo Times) at each stream level will show whether PostgreSQL stays ahead of forced-DuckDB PgDuckDB as concurrency rises, and whether the gap widens or narrows.
