

Submitted as experiment **1787578997**.

**What I designed:** A head-to-head comparison of PostgreSQL vs PgDuckDB on the 10 GB TPC-H workload, with PgDuckDB pinned to `duckdb_force_execution: true` so every query actually runs through the DuckDB engine (per the catalog, without this the extension idles and you'd be measuring Postgres against itself).

**How it answers the question:**
- **Factor under test (system):** the only thing that differs between the two systems is the engine — both use the same `analytical-ssd` profile (PgDuckDB's profile refs PostgreSQL's, so identical knobs derive from the same limits), the same shared `post_load: {statistics: true}`, and the same resource cell.
- **Concurrency:** `rounds: [1, 2, 4]` sweeps concurrent query streams, with 4 as the TPC-H rule-of-thumb max for SF=10 (floor(log₃10)+2), so "concurrent analytical reporting" is directly measured rather than assumed.
- **Fixed budget:** a single shared cell of 16 CPU / 64 GiB, exactly the operating point in the question. I deliberately did not sweep resources — 10 GB of data fits comfortably in 64 GiB, so resource pressure isn't a plausible rival explanation, and a single cell keeps the design decisive.
- **Reliability:** `repetitions: 3` (the catalog's minimum for any system-comparison conclusion) so run-to-run variance can be separated from a real difference.
- **Placement:** SUT, loader, and benchmarker pinned to three distinct high-memory nodes (cl-worker34/38/39) since most cluster nodes have only ~500 MiB RAM and would starve a 64 GiB pod.

The comparison will be made on the summary metrics (Power@Size, Throughput@Size, Geo Times) plus per-query latency, across the concurrency sweep. Total cost: 2 systems × 3 rounds × 3 reps = **18 runs**.
