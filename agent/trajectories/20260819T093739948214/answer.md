

The specification is written and validates cleanly (`valid: true`, environment checked, 48 runs). Note: a `submit` tool isn't exposed in my available function set (only `read_file`, `write_file`, `validate`), so I've stopped at the validated state — the file `inbox/pgduckdb-join-concurrency-mem-sweep.yml` is the exact spec to launch.

## What I designed and how it answers the question

**The comparison (Q1: is pg_duckdb better on joins, even under concurrency?)**
- Two systems: `PostgreSQL` (baseline) and `PgDuckDB`, both on the `analytical-ssd` profile so every knob resolves identically from the same resource limits.
- I set `duckdb_force_execution: true` on PgDuckDB. This is the critical control: the catalog warns that on heap tables pg_duckdb's cost-based routing normally keeps queries in PostgreSQL's own executor, which would make the experiment measure Postgres against Postgres. Forcing execution guarantees I'm actually testing DuckDB's engine.
- Workload is TPC-H at `scaling_factor: 1` (your 1GB dataset), restricted to `active_queries: [5, 7, 8, 9, 21]` — the catalog's named multi-way-join subset — so the "joins" claim is measured on joins, not the full 22-query mix.
- `rounds: [1, 2, 4, 8]` is the concurrency sweep, so I see the system-vs-system gap at each stream count, not just one point.

**The mechanism (Q2: memory starvation vs. thread contention?)**
- I sweep `resources.memory` at `32Gi` and `64Gi` — half and the full 64GB ceiling you gave — while holding `cpu` fixed at 16 cores. This is the catalog's `bounded_resources` rule for a user-given ceiling.
- The `analytical-ssd` profile *derives* `work_mem` and `shared_buffers` from `memory_limit`, so the two cells genuinely change per-query join memory (work_mem 512Mi vs 1Gi). That's what makes the sweep diagnostic:
  - **Memory starvation** → steeper throughput drop as streams rise *at 32Gi* than at 64Gi (less per-stream join memory → more hash-join spilling).
  - **Thread contention** → similar degradation at *both* memory levels (CPU is the constant bottleneck).
- `discriminates: [system, concurrency, memory]` names all three isolated factors.

**Fairness and rigor**
- `post_load: {statistics: true}` is shared by both systems so both planners have cardinality estimates (no per-system divergence, which the catalog forbids in one file).
- `repetitions: 3` (the catalog's minimum for any system-comparison conclusion) and `query_repeats: 3` give real variance and enough phase length for the monitoring warm-up.
- `observe` scrapes SUT + cluster metrics so the memory/CPU signal behind the throughput curve is directly visible.

**Fit to your cluster:** everything is pinned to `cl-worker36` (the only usable node — all others are tainted or excluded, and the templates pin there). No `ssd` storage class exists, so I left `storage_class` unset (the profile permits `null`) → node-local disk, with a 10Gi request. 64Gi fits the node's ~2TB RAM.

**Cost:** 2 systems × 2 memory cells × 4 rounds × 3 reps = **48 runs**, each 5 join queries × 3 repeats at SF=1 — a decisive but bounded design.

The one follow-up I'd reserve (you allow one) is a CPU sweep at fixed 64Gi memory, to directly confirm the thread-contention arm if the memory sweep is inconclusive.
