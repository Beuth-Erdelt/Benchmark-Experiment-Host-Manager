

**Experiment submitted under code `1787175665`.**

**What I designed (initial experiment, forced-execution side):**
- **System:** a single `PgDuckDB` entry (satisfying the no-duplicate-names rule) with the `analytical-ssd` profile and `override: duckdb_force_execution: true`, so every query is pushed through DuckDB's vectorized executor.
- **Workload:** TPC-H, `scaling_factor: 1` (1 GB), all 22 queries, `rounds: [1, 8]` (1 and 8 concurrent streams), `repetitions: 3` (the catalog's minimum for any effect claim), `query_repeats: 2` for per-query latency stability.
- **Resources/placement:** 16 CPU cores and 64 GiB RAM exactly as specified, pinned to `cl-worker36` (the only usable node), node-local storage (no `ssd` class exists in this cluster, and the profile permits it).
- **Controls:** `post_load: statistics: true` so the planner has real estimates — this matters because the follow-up's cost-based routing will use them, and the follow-up must replicate this identically.

**How it answers the question:** this run produces the forced-execution arm — per-query latencies and summary metrics (Power@Size, Geo Times) at both concurrency levels. The one follow-up will be the byte-identical design with `duckdb_force_execution: false`, so the only thing that varies between the two experiments is the routing mode. Comparing them gives the overall recommendation (summary metrics at 1 and 8 streams) and, from the per-query latency rows, whether the verdict is consistent across query shapes or whether specific queries favor the opposite mode.
