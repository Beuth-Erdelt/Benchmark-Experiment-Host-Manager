# Catalog Input Contract

A pre-build reference for an agent (or human) that needs to know, **before
writing an `experiment.yml`**, exactly what it may legally contain — which
workloads and systems exist, which parameters/knobs each takes, and which
three header fields are required — without reading any source code.

Mirrors [`AgentResultContract.md`](AgentResultContract.md)'s role on the
output side: that file tells an agent what it'll get back, this one tells it
what it's allowed to ask for. Everything below is read directly from
`contracts/contract_catalog.yml` itself — no other file is needed to know
the current shape of a valid `experiment.yml`.

```yaml
catalog_contract_version: "1.1.0"   # == bexhoma.spec.CATALOG_CONTRACT_VERSION

catalog_concepts:                    # vocabulary used throughout this file's own fields
  workloads:      {semantics: "what to run: params, loading behavior, physical-design semantics"}
  systems:        {semantics: "what to run it on: server knobs, physical-design support, profiles"}
  physical_design: {semantics: "a system's CAPABILITY only (indexes/constraints/statistics/storage_format) --
                                 whether it's actually applied is a separate per-experiment SELECTION,
                                 via loading.post_load / systems[].post_load"}
  derive:         {semantics: "arithmetic expression scaling a profile knob with the experiment's own
                                resource limits -- only +,-,*,/ over memory_limit/cpu_limit/storage_class/scaling_factor,
                                no functions/conditionals/string ops"}
  extends:        {semantics: "systems.<name>.extends: BaseName merges BaseName's knobs:/profiles: in
                                (this system's own entries of the same name win); every OTHER top-level
                                key (physical_design, deployment, image, arg_style, ...) is NOT merged --
                                e.g. PgDuckDB.extends: PostgreSQL still needs its own physical_design: block"}
  profile_ref:    {semantics: "systems.<name>.profiles.<p>.ref: 'System.profiles.name' resolves to that
                                OTHER system's profile object directly, for profile parity"}
  requires:       {semantics: "a profile's requires: {storage_class: [...]} lists which resources.storage_class
                                values an experiment.yml using it may set; null means 'unset' is also legal;
                                a profile without requires: imposes no constraint"}
  arg_style:      {semantics: "how a resolved knob is applied -- pg-guc (default): a --set ...GUC patch;
                                env-var: via the knob's own env_var name instead; a knob may override its
                                system's default"}
  knob_status:    {semantics: "a knob with status: reference-only exists in the DBMS but is commented out
                                in the shipped k8s template -- still legal to set via profile/override,
                                just not active by default. fixed: true (separate) marks a knob that isn't
                                mechanically blocked but has no other legal value in practice for this pairing"}
  sut_isolation:  {semantics: "the default situation is one system-under-test at a time, not several at once:
                                every systems[] entry (crossed with any resources: sweep) is benchmarked on
                                its own, next SUT started only after the previous is torn down. Co-located
                                SUTs interfere (shared node CPU/memory-bandwidth/disk/network), so a
                                side-by-side run would measure interference, not the discriminates: factor.
                                Enforced by two independent caps, both default 1: top-level max_sut (-ms,
                                cluster-wide) and max_sut_experiment (-mse, this experiment only). Set
                                either to 0 (no limit) or N>1 for parallel SUTs -- only for SUTs on
                                separate nodes. Omitting them keeps the serial default.
                                Parallel loader pods / benchmarker clients run within one SUT and are exempt"}

experiment_schema:
  required_header_fields: [title, hypothesis, discriminates]   # validate_experiment() rejects a missing/empty one before anything else resolves
  optional_header_fields:
    follow_up_of: "experiment_code (contract_result.yml's structure.experiment_code) of a prior run this
                    one follows up on -- structured lineage instead of prose in hypothesis; bookkeeping
                    only today, see known_gaps below"
  top_level_shape:            # every field below is a SIBLING at the top of experiment.yml
    mode:       {type: enum, values: [run, profiling, start, load, empty, summary], default: run}
    title:      {type: str, required: true}
    hypothesis: {type: str, required: true}
    discriminates: {type: "list[str]", required: true, example: "[system, concurrency, memory]"}
    follow_up_of: {type: str, required: false}
    max_sut:            {type: int, default: 1, semantics: "max SUTs running at once CLUSTER-WIDE (-ms);
                          1 = one system at a time, 0 = no limit, N>1 = up to N -- see catalog_concepts.sut_isolation"}
    max_sut_experiment: {type: int, default: 1, semantics: "same, scoped to this experiment only (-mse);
                          independent of max_sut, both enforced together; 0 = no limit"}
    workload:   {type: object, fields: [name, params, rounds, repetitions]}
    loading:    {type: object, fields: [pods, threads, split, post_load],
                 pitfall: "must be a TOP-LEVEL sibling of workload:, NOT nested under it -- a
                           workload.loading block silently resolves to {} instead of erroring"}
    systems:    {type: list, item_fields: [name, profile, override, post_load],
                 semantics: "one resolved configuration per entry; benchmarked one at a time,
                             never concurrently -- see catalog_concepts.sut_isolation"}
    observe:    {type: object, fields: [monitoring_sut, monitoring_cluster, monitoring_app]}
    placement:  {type: object, fields: [sut, loading, benchmarking],
                 semantics: "each node named must exist, and not be tainted out, in environment.yml's nodes:"}
    resources:  {type: object, fields: [cpu, memory, storage, storage_class],
                 semantics: "cpu/memory: a single {request,limit} dict shared by every system, OR a list
                             to sweep every systems: entry against every list entry (one resolved
                             config per system*cell pair); cpu and memory sweep lists must share one length"}
  quantity_format:
    memory_and_storage: {binary: [Ki, Mi, Gi, Ti], decimal: [K, M, G, T], out_of_scope: [KB, MB, GB, TB], examples: ["32Gi", "512Mi"]}
    cpu: {semantics: "cores, or millicores with trailing m", examples: ["8", "0.5", "500m"]}

workloads:
  tpch:
    supports: [PostgreSQL, PgDuckDB]
    modes: [profiling, run, start, load, empty, summary]
    resource_profile: {cpu: high, memory: high, why: "multi-way hash joins + aggregation are CPU/RAM-bound; storage bandwidth matters less"}
    params:            # workload.params keys
      scaling_factor:      {type: int, unit: GB}
      timeout:              {type: int, unit: seconds}
      query_repeats:        {type: int, default: 1, min: 1}
      measure_datatransfer: {type: bool, default: false}
      active_queries:       {type: "list[int]", default: all, example: "[5,7,8,9,21] = multi-way joins"}
      recreate_parameter:   {type: bool, default: false}
      shuffle_queries:      {type: bool, default: false}
      refresh_streams:      {type: int, default: 0}
      refresh_stream_offset: {type: int, default: 0}
      store_explain:        {type: bool, default: false, when: "requires an 'explain' key in the DBMS connection's JDBC config"}
    loading:
      pods:   {type: int, min: 1, support: "works for every DBMS"}
      threads: {type: int, min: 1, support: "only honored by some loaders (e.g. MySQL); prefer pods"}
      split:  {type: int, default: 1}
      post_load:   # indexes/constraints/statistics are mutually independent -- all 8 combinations legal per system
        indexes:    {type: bool, default: false}
        constraints: {type: bool, default: false}
        statistics: {type: bool, default: false}
        storage_format: {type: enum, values: [heap], default: heap}
    rounds: {type: "list[int]", rule_of_thumb: "official sizing: floor(log(scaling_factor, 3)) + 2, e.g. SF=100 -> 6"}
    repetitions: {type: int, default: 1}
    produces:
      per_query: {metric: latency, unit: ms}
      summary:   {metrics: [Power@Size, Throughput@Size, Geo Times], unit: [Q/h, Q/h, s]}
      quality:   {metric: sql_errors_warnings}
      out_of_scope: {time_series: "no per-second signal like YCSB/Benchbase -- per-query/per-phase aggregates only"}

systems:
  PostgreSQL:
    image: postgres:18.3
    arg_style: pg-guc
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    knobs_active_by_default: [max_connections, max_worker_processes, max_parallel_workers,
      max_parallel_workers_per_gather, max_parallel_maintenance_workers, shared_buffers,
      effective_cache_size, work_mem, maintenance_work_mem, autovacuum, wal_level,
      max_wal_senders, max_wal_size, checkpoint_timeout, checkpoint_completion_target,
      lock_timeout, idle_in_transaction_session_timeout]
    knobs_reference_only: [effective_io_concurrency, io_method, random_page_cost, seq_page_cost,
      default_statistics_target, fsync, synchronous_commit, wal_compression]
    profiles:
      analytical-ssd:
        requires: {storage_class: [ssd, null]}
        why: "OLAP on node-local NVMe, sized from the experiment's memory limit"
        knobs: {random_page_cost: 1.1, effective_io_concurrency: 200, io_method: io_uring,
                 max_parallel_workers_per_gather: 2, max_parallel_workers: 4, max_worker_processes: 6}
        derive: {shared_buffers: "0.3125 * memory_limit", effective_cache_size: "0.75 * memory_limit",
                  work_mem: "0.015625 * memory_limit", maintenance_work_mem: "0.03125 * memory_limit"}
  PgDuckDB:
    why: "PostgreSQL + pg_duckdb extension, vectorized DuckDB execution engine alongside Postgres' own planner"
    extends: PostgreSQL   # every knob not listed below inherits unchanged
    image: pgduckdb/pgduckdb:18-v1.1.1
    arg_style: pg-guc
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap],
                       out_of_scope: "columnar (native `USING duckdb` tables) blocked upstream, github.com/duckdb/pg_duckdb#385"}
    knobs_own:
      shared_preload_libraries: {default: pg_duckdb, fixed: true}
      duckdb_force_execution:   {type: bool, default: false, arg_style: env-var, env_var: DUCKDB_FORCE_EXECUTION}
    profiles:
      analytical-ssd: {ref: "PostgreSQL.profiles.analytical-ssd"}   # identical knob values from the same memory/cpu limits
```

---

## `catalog.yaml` is not a separate file you need to build

`contracts/contract_catalog.yml` above is not an abstract schema requiring a
separately instantiated `catalog.yaml` — it already **is** the concrete
catalog data (`systems: [PostgreSQL, PgDuckDB]`, `workloads: [tpch]`).
`validate_experiment.py`'s own `-c` default points straight at it. The name
`catalog.yaml` elsewhere in the codebase (`experiment.py`'s sibling-file
lookup, `Design-Yaml-Experiment-Entry-Script.md`'s `catalog:` provenance
pointer) just names wherever a *working copy* of this same file happens to
live — nobody in this repo has ever populated a different one. See
[`AgentWorkflow.md`](AgentWorkflow.md) for the full build → validate → run →
answer loop this contract is step 2–3 of, including why `environment.yml` (a
live cluster snapshot, not a contract) is a genuinely separate third input.

## Minimal example

```bash
python validate_experiment.py experiment.yml
#   OK    resolves against catalog
#   command: python tpch.py run -dbms PostgreSQL PgDuckDB -sf 10 -t 300 -xqr 3 ...
```

See [`dev/catalog/experiment.yml`](../dev/catalog/experiment.yml) for the
maintained, real, runnable `experiment.yml` this resolves — a two-system
(`PostgreSQL` vs. `PgDuckDB`) `analytical-ssd`-profile sweep across
concurrency (1→16) and memory (64Gi→32Gi), with `discriminates: [system,
concurrency, memory]`. Both systems (× every swept cell) resolve into one
command, but bexhoma benchmarks them **one SUT at a time** — `max_sut` and
`max_sut_experiment` both default to `1` — so the two never contend for the
same node. Set either to `0` (no limit) or `N` in the experiment.yml to
allow parallel SUTs; see `catalog_concepts.sut_isolation`.

## Known gaps versus an idealized contract

- **Only one workload is translatable today.** `bexhoma/spec.py::build_argv()`
  dispatches by `experiment.workload.name` to that workload's own argv
  builder — only `tpch` has one
  (`bexhoma/experiments/tpch_catalog.py::build_tpch_argv()`). A catalog-driven
  `experiment.yml` naming `ycsb`, `hammerdb`, `benchbase`, or `tpcds` fails
  resolution with `SpecError: no argv builder implemented yet for workload
  '<name>'` — those workloads still run fine via their own entry scripts
  (`ycsb.py`, `hammerdb.py`, ...) directly, just not through this catalog
  contract yet.
- **Only two systems are in scope for `tpch`.** The full `tpch` workload
  (outside this contract) also supports `MonetDB`, `MySQL`, `MariaDB`,
  `DatabaseService`, `Citus`, `CedarDB` — trimmed to `PostgreSQL`/`PgDuckDB`
  for this prototype catalog (`workloads.tpch.out_of_scope.systems`).
- **No comparative/historical validity check reads `follow_up_of`.** It
  records intended lineage structurally, but nothing enforces or verifies
  that the named `experiment_code` exists or ran a comparable workload — see
  `contract_result.yml`'s `known_gaps.cross_experiment_comparison`.
- **`extends`/`profile_ref` don't imply capability parity.** A system that
  `extends:` another still needs its own explicit `physical_design:` block
  (that key is never merged) — see `catalog_concepts.extends.out_of_scope`.

## See also

- [`AgentWorkflow.md`](AgentWorkflow.md) — the end-to-end loop this contract
  is the input half of: question → contracts → `experiment.yml` → validate →
  run → answer.
- [`AgentResultContract.md`](AgentResultContract.md) — the output-side
  counterpart: what a completed run's result folder contains.
- `contracts/contract_catalog.yml` /
  `contracts/contract_catalog_comments.md` — the actual contract and its
  human-only rationale doc.
- [`validate_experiment.py`](../validate_experiment.py) — dry-run validates
  an `experiment.yml` against this contract without touching a cluster.
