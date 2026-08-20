

Submitted as experiment **1787125351**.

**What I designed:** A 2-system × 2-memory × 4-concurrency TPC-H experiment (48 runs, 3 repetitions each) on the only usable node, `cl-worker36`, with node-local storage.

- **Joins, not the whole suite:** TPC-H at SF=1 (your 1GB dataset), restricted to the multi-way join queries 5, 7, 8, 9, 21, so the comparison is squarely about join performance.
- **System factor:** PostgreSQL vs PgDuckDB with `duckdb_force_execution: true` — without it, pg_duckdb's cost-based routing would keep queries in the Postgres executor and you'd be measuring PostgreSQL against itself. Both use the same `analytical-ssd` profile (PgDuckDB's is a ref to PostgreSQL's, so knobs resolve identically from the same limits) and the same post-load (ANALYZE statistics on, no indexes), so everything except the engine is held equal.
- **Concurrency factor:** rounds sweep 1 → 2 → 4 → 8 parallel client streams, with 10 query repeats per round so each phase runs long enough for the SUT/cluster monitoring scrapes to clear their warm-up window.
- **The memory-vs-contention discriminator:** your 64GB ceiling becomes a two-cell memory sweep — 32Gi and 64Gi. Because the profile derives `work_mem` and `shared_buffers` from the memory limit, per-stream hash-join memory is 512Mi at 32Gi but 1Gi at 64Gi, while CPU is held fixed at 16 cores. If throughput degrades much more steeply with concurrency at 32Gi than at 64Gi, the degradation is per-stream memory starvation; if the degradation curves look similar at both limits, it's thread/CPU contention. SUT and cluster monitoring give you direct memory-usage evidence to confirm.

The summary metrics (Throughput@Size, Power@Size, Geo Times) per system/round/memory cell answer both questions: whether pg_duckdb leads on joins under concurrency, and which resource explains any degradation.
