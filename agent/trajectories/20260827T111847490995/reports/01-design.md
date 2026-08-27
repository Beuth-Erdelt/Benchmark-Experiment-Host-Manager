

**Experiment submitted as `1787822388`.**

I designed a 2-system × 2-concurrency × 3-repetition TPC-H experiment (12 benchmark phases) that directly answers both parts of the question:

- **SF2 persistence**: The full 22-query TPC-H workload runs at `scaling_factor: 2` on `PostgreSQL` and `PgDuckDB` with `duckdb_force_execution: true` (per the catalog's guidance, required whenever comparing PgDuckDB's execution engine against another system — otherwise pg_duckdb's cost-based routing would keep queries in Postgres and the comparison would be meaningless).
- **Ranking stability across concurrency**: `rounds: [1, 2]` sweeps one to two concurrent query streams, with `repetitions: 3` (the catalog's minimum for any system-comparison claim) to separate real differences from run-to-run variance.
- **Identical limits**: Both systems share one resource cell — 16 CPU request/limit and 64 GiB memory request/limit — and both use the `analytical-ssd` profile (PgDuckDB's profile references PostgreSQL's, so they resolve to identical knobs derived from the same limits). Physical design stays at shared defaults for both, so system and concurrency are the only varying factors.
- **Environment fit**: All pods pinned to `cl-worker36` (the only usable node), node-local storage (the profile permits `ssd` or unset; no `ssd` class exists here), 4 loader pods with a 60-minute load deadline for SF2.

The per-phase Geo Times / Throughput@Size summary metrics will show whether PostgreSQL's SF1 advantage holds at SF2 and whether the ranking flips or holds between 1 and 2 streams.
