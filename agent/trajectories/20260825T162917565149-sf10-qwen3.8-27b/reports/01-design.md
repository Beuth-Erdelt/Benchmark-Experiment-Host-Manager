

Submitted as experiment **1787668255**.

**What I designed:** A retry of the failed 10 GB TPC-H comparison, structured as a clean two-system A/B test.

- **Hypothesis / factor:** Under a fixed 16 CPU / 64 GiB envelope, PostgreSQL stays the better choice than forced-DuckDB PgDuckDB for concurrent analytical reporting. The only thing that varies is the **system**; I also sweep **concurrency** via rounds [1, 2, 4] with 3 repetitions (18 runs total).
- **Forced-PgDuckDB:** `duckdb_force_execution: true` is set on the PgDuckDB entry so every query goes through DuckDB's engine rather than pg_duckdb's cost-based routing (which would otherwise leave the extension idle and measure PostgreSQL against itself).
- **Parity:** Both systems use the `analytical-ssd` profile — the catalog's `profile_ref` makes PgDuckDB's profile resolve to the exact same knobs as PostgreSQL's from the same memory/cpu limits, so the two are configured identically.
- **Preserved settings:** 4 loader pods, 1 thread, split 1, 120-min load timeout, shared post_load {indexes=false, constraints=false, statistics=true, storage_format=heap}, monitoring {sut=true, cluster=false, app=false}, 50Gi storage.
- **Storage class:** left unset (node-local) because the `analytical-ssd` profile requires `ssd` or null and the environment has no `ssd` class.
- **Placement (peak envelope validated):** SUT (16 CPU/64 GiB/50Gi) → cl-worker28; 4 loader pods → cl-worker29; benchmarker → cl-worker27. The benchmarker is the peak consumer — one pod per concurrent stream at 16 CPU/128 GiB each, so the worst round (4 streams) needs 64 CPU/512 GiB, which the ~1 TiB/256-CPU cl-worker27 hosts with headroom. Each component is pinned to a distinct node to avoid cross-contention.

The design validates against the catalog and environment and expands to a runnable 18-run experiment.
