

Submitted as experiment **1787510676**.

## What I designed

A single decisive benchmark on the only analytical workload in the catalog, **TPC-H at scale factor 1 (1 GB)**, comparing the two systems that can run it: **PostgreSQL** and **PgDuckDB**.

- **Factor under test (system):** the only thing that varies between the two systems is the execution engine. I set `duckdb_force_execution: true` on PgDuckDB — the catalog warns that without it, pg_duckdb's cost-based routing keeps queries in Postgres' own executor and you'd be "measuring PostgreSQL against PostgreSQL." Both systems use the `analytical-ssd` profile (PgDuckDB's is a `ref` to PostgreSQL's), so they resolve identical Postgres-side knobs from the same limits.
- **Concurrency factor:** `rounds: [1, 2]` — one round with a single analyst stream, one with two concurrent streams — directly answering "does the recommendation hold when multiple analysts run reports concurrently."
- **Controls held equal:** identical heap tables, `statistics: true` (ANALYZE) for both, no indexes/constraints (so neither system gets a physical-design advantage), same 16 CPU / 64 GiB resource cell, same node (`cl-worker36`, the only usable node), and `verify_result: true` so a "faster" system that returns wrong rows is caught.
- **Repetitions:** 3, the catalog's minimum for any system-comparison claim, so run-to-run variance can't masquerade as a real difference.
- **Run budget:** 2 systems × 1 resource cell × 2 rounds × 3 reps = **12 runs**, well under the 24 cap.

**Why one resource cell, not a sweep:** the ceiling is 16 CPU / 64 GiB, but the working set is 1 GB — memory pressure is not a plausible rival explanation for a system or concurrency effect at this size, so per the catalog's `bounded_resources` rule I fixed the cell at the ceiling rather than paying for a half-ceiling cell.

## How it answers the question

The summary metrics (Power@Size, Throughput@Size, Geo Times) plus per-query latency, broken out by system and by round, give a single-analyst ranking (round 1) and a concurrent-analyst ranking (round 2). If the winner at round 1 is also the winner at round 2, the recommendation is robust to concurrency; if the ranking flips, the recommendation is conditional on analyst load.

## Recommendation (to be confirmed by the results)

The design is built to confirm or refute the hypothesis that **PgDuckDB (DuckDB engine forced) is the system to deploy** for this 1 GB analytical workload, with the round-2 data telling us whether that holds under concurrent analysts.

## Limitations

- **Concurrency is only tested at 2 streams.** The TPC-H rule of thumb for SF=1 suggests a max of ~2–3 concurrent streams, so 2 is a reasonable "multiple analysts" point, but it does not characterize behavior at higher load (e.g., 4–8 analysts), where memory division and worker contention could change the ranking.
- **Single resource cell at the ceiling.** I did not sweep a half-ceiling (8 CPU / 32 GiB) cell, so I cannot separate a genuine engine advantage from one that only appears when resources are tight.
- **Heap-only, no columnar storage.** PgDuckDB's native columnar (`USING duckdb`) tables are explicitly out of scope in this deployment, so this measures the extension over heap tables, not its best-case columnar path.
- **SF=1 only.** The 1 GB size is the stated workload, but the ranking could differ at larger scale factors where cache behavior and parallelism matter more.
- **One node, one storage path.** Everything runs on `cl-worker36` with node-local storage (no `ssd` storage class exists in this environment), so results reflect that node's local disk and are not a multi-node or network-storage story.

**Planned follow-up (evidence-driven, 1 slot):** if the two systems are close at round 1 but diverge at round 2 — or if the winner is memory-sensitive — I would add a half-ceiling resource cell (8 CPU / 32 GiB) to test whether the ranking is driven by resource pressure rather than the engine, keeping the design within the 24-run budget.
