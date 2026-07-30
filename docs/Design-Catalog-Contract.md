# Design (draft): Catalog Contract

> **Status: draft, partially prototyped.** This is a design proposal for
> [issue #764](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues/764).
> A working prototype now exists for the TPC-H/PostgreSQL/PgDuckDB slice —
> see "Near-term implementation scope" below for exactly what's built vs.
> still just designed. Not linked from `docs/index.rst` on purpose — it's a
> working note, not published documentation.
>
> This revision widens the catalog to bexhoma's **full** current surface
> area (all 6 workloads, all ~19 deployable systems) specifically to find
> where the two-axis schema breaks — see "Full surface audit" below.
> Full knob-level depth is only worked out for **TPC-H against PostgreSQL
> and PgDuckDB**, since that's the near-term implementation target; every
> other system is catalogued structurally (deployment shape, patch
> mechanism, physical-design capability) but not knob-by-knob. Expect
> continued churn.
>
> **The "Complete `catalog.yaml`" section below is the illustrative,
> all-systems design sketch — it is not the file that exists on disk.**
> The real, active contract lives at `contracts/contract_catalog.yml`
> (promoted out of `dev/catalog/` once it graduated from prototype to the
> input contract `bexhoma/spec.py` actually consumes) and is a trimmed
> subset (`tpch` + `PostgreSQL` + `PgDuckDB` only, and — per explicit
> instruction — without the `oltp-large-node`/`legacy-baseline` profiles the
> sketch below still shows). Treat the sketch as "does the schema
> generalize", and `contracts/contract_catalog.yml` as "what actually runs".
>
> `contracts/contract_catalog.yml` is consumed by `bexhoma/spec.py`
> (`validate_experiment()`, `build_argv()`), `validate_experiment.py`, and
> `experiment.py`'s catalog-driven dispatch. Its own header comment is
> deliberately self-contained (full experiment.yml shape, including the
> `resources:` quantity format) so an agent never needs to open this design
> doc, `spec.py`, or any other source just to build a valid experiment.yml
> — this doc instead carries the *why* behind those choices, the full
> all-systems breadth pass the trimmed contract was extracted from, and
> open questions.

## Problem

Bexhoma's only entry point today is CLI invocation of the per-workload entry
scripts (`tpch.py`, `ycsb.py`, `benchbase.py`, `hammerdb.py`, `tpcds.py`,
`hardware.py`). Tuning knobs for the system under test are passed as raw,
unvalidated K8s manifest patches:

```powershell
--set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=20GB
```

This works, but has no notion of *why* a value was chosen, no reuse across
DBMS variants that share configuration (e.g. PgDuckDB reuses PostgreSQL's DDL
today via `config.path_experiment_docker = 'PostgreSQL'` in `tpch.py`, but
its `--set` block has to be hand-duplicated in full), and nothing stops a
value from being nonsensical for the workload or unsupported by the system.
Issue #764 asks for a **catalog contract**: a document an off-the-shelf LLM
agent can read, alongside `environment.yml`, to construct a valid experiment
without prior context.

## Two axes, one file

The catalog has two axes — **what to run** (workload) and **what to run it
on** (system) — kept in a single `catalog.yaml` rather than split across
files. One file matches the acceptance criterion ("agent needs only this
document plus `environment.yml`") more literally, and keeps `supports:`
cross-references (workload → system) checkable within one document at
load time. The trade-off — one file accumulates merge-conflict surface as
workloads/DBMS variants grow — is deferred; splitting later is non-breaking
since both axes keep the same top-level keys. The audit below adds a third
top-level key, `tools:`, for things that are neither a workload-on-a-system
pair nor patchable server config (see §Hardware).

## Full surface audit

Everything below is grounded in the actual entry scripts, `k8s/deploymenttemplate-*.yml`
files, `docs/DBMS.md`, and the various `docs/Example-*.md` pages — not
invented. Citations are file:line where useful.

### Workload axis: 6 entry scripts, not uniform

| | tpch | tpcds | ycsb | benchbase | hammerdb | hardware |
|---|---|---|---|---|---|---|
| `mode` choices | profiling,run,start,load,empty,summary | same | run,start,load,summary | run,start,load (**no summary**) | run,start,load,summary | run,start,summary (**no load**) |
| `-dbms` choices | PostgreSQL, MonetDB, MySQL, MariaDB, DatabaseService, Citus, CedarDB, PgDuckDB | PostgreSQL, MonetDB, MySQL, MariaDB | PostgreSQL, MySQL, MariaDB, YugabyteDB, CockroachDB, TiDB, DatabaseService, PGBouncer, Redis, Citus, CedarDB, Dragonfly | PostgreSQL, MySQL, MariaDB, YugabyteDB, CockroachDB, TiDB, DatabaseService, Citus, PGBouncer, CedarDB | PostgreSQL, MySQL, MariaDB, Citus | `Hardware` only — not an engine selector |
| Loading scales with `-nlp`/`-nlt`? | yes | yes | yes | pods fixed to 1 in the sweep loop | **`-nlp` parsed but ignored, hardcoded to 1** | no loading phase at all |
| Workload-variant flag | none (`-xaq` restricts query subset) | none | `-xwl` {a,b,c,d,e,f} | `-xbt` {tpcc,twitter,chbenchmark,ycsb} (+`-xwl` only when `-xbt ycsb`, note extra `c2` choice not in ycsb's own `-xwl`) | none (TPC-C only) | `-xht` {fio,sysbench,sockperf,netperf} |
| Refresh/secondary stream | `-xrs`/`-xrso` (RF1/RF2) | none | none | none | none |

Confirmed: `mixed.py` (`bexhoma/experiments/mixed.py`, `MixedExperiment`) is
composition-only — no CLI, subclassed by every workload's experiment class.
Not a separate catalog entry.

**Same CLI-facing unit, different unit at the wire boundary — by design, not
a bug.** Each backend tool has its own native config format, and bexhoma
correctly converts a single user-facing CLI unit into whatever each tool
natively expects:

- `-xsd` (scaling-duration) is **minutes** at the CLI in both hammerdb.py
  and benchbase.py — same help text, same user-facing contract. Internally:
  hammerdb.py passes it straight through (`HAMMERDB_DURATION=str(SD)`)
  because HammerDB's own `diset tpcc ... duration` interface genuinely wants
  minutes (`images/hammerdb/benchmarker/README.md:49`: *"Duration in minutes
  before the second transaction count is taken"*). benchbase.py converts to
  seconds (`SD=int(args.scaling_duration)*60`) because Benchbase's own XML
  `BENCHBASE_TIME` field genuinely wants seconds
  (`images/benchbase/README.md:77`: *"Benchmark duration in seconds.
  Substituted into the XML config"*). Both scripts get this right — the
  catalog's job is to document the **CLI-facing** unit (minutes, consistent
  across both), not to flag the internal conversion as a discrepancy.
- `-xli` (logging-interval) likely follows the same pattern: Benchbase's own
  `--interval-monitor` flag genuinely wants milliseconds
  (`images/benchbase/README.md:81`), matching benchbase.py's
  `BENCHBASE_STATUS_INTERVAL`, while YCSB's own `status.interval` property
  genuinely wants seconds (`images/ycsb/generator/README.md:48`), matching
  ycsb.py's `YCSB_STATUS_INTERVAL`. One narrower loose end here worth a
  maintainer's confirmation, not a catalog concern: benchbase.py's own help
  text already says "milliseconds" (`benchbase.py:39`) yet the code still
  multiplies the parsed value by 1000 (`scaling_logging=int(...)＊1000  #
  adjust unit to miliseconds`, `benchbase.py:94`) — that reads like the
  help string is stale (the intended CLI-facing input is seconds, for
  consistency with ycsb's own `-xli`) rather than like a functional bug,
  since the multiplication only makes sense if the input isn't ms yet.
- `-nbt` in `hardware.py` is overloaded three ways depending on `-xht`: fio
  `numjobs`, sysbench `--threads`, netperf concurrent-instance count — same
  flag, three tool-specific meanings, same pattern as above (one CLI-facing
  parameter, converted per backend).
- HammerDB's `-xii`/`-xic`/`-xis`-shaped flags don't exist; instead `-xdt`
  and `-xqr` are parsed (inherited from the shared code path) but appear
  vestigial — HammerDB's evaluator has no per-query-repeat or
  data-transfer concept to feed them.
- `tpcds.py` accepts `-xcol` (init_columns) but has no Citus branch wired up
  — the flag is parsed and silently inert for every TPC-DS invocation.

**Consequence for the catalog schema:** every workload `params` entry still
needs an explicit `unit:` field — but it documents the single **CLI-facing**
unit (e.g. "minutes" for `duration`, consistent across hammerdb and
benchbase), not a per-backend wire format. The per-tool conversion
(minutes→minutes for HammerDB, minutes→seconds for Benchbase) is bexhoma's
existing, correct implementation detail and stays out of the catalog
entirely — an agent constructing an `experiment.yaml` only ever needs to
know the one CLI-facing number to write.

### System axis: patch mechanism is not uniform

The existing `--set deployment[NAME].container[dbms].KNOB=VALUE` passthrough
(`bexhoma/configurations/manifest.py:36-63`, `ensure_arg_pairs()`) only
works for the literal two-element `["-c", "key=value"]` argument shape
Postgres-family images use. This is a load-bearing finding: a `knobs:`
catalog entry is not automatically actionable just because it exists.

| Patch mechanism (`arg_style`) | Systems | Patchable via today's `--set`? |
|---|---|---|
| `pg-guc` (`-c key=value` pairs in `args:`) | PostgreSQL, PgDuckDB, Citus | yes |
| `flag-equals` (`--key=value`, no `-c` prefix) | MySQL, MariaDB, Redis | **no** — `ensure_arg_pairs()` would append a spurious `-c key=value` instead of editing the real flag |
| `command-string` (knob baked into a shell `command:` block) | CockroachDB (`--cache`/`--max-sql-memory` derived from `$MEMORY_LIMIT_MIB` at container start), TiDB, Dragonfly (`--admin_port`, `--maxmemory`) | **no** — unreachable by any `args:`-patching mechanism |
| `helm-values` | YugabyteDB (`gflags.tserver.*`, `resource.*` in a Helm `values.yaml`, entirely outside bexhoma's manifest pipeline) | **no** — different tool entirely |
| `none` (no tunables exposed) | CedarDB, MonetDB | n/a |

This forces a schema field: every `systems.<name>` entry needs
`arg_style:` and, per knob, an honest `patchable: true/false` (or it's
implied by `arg_style` at the system level, with per-knob overrides for the
`duckdb_force_execution`-style exception below).

### Deployment/name irregularities

- MonetDB's real Deployment name is `bexhoma-sut-monetdb` — it's the one
  system that breaks the `bexhoma-deployment-<key>` convention every other
  template follows (`docs/DBMS.md:121-122` states the convention; MonetDB
  violates its own docs). This is exactly why `deployment:` must be an
  explicit literal field per catalog entry, never derived from a naming
  rule.
- Citus, CockroachDB, TiDB are **multi-component**: a coordinator/SQL-layer
  Deployment plus one or more worker StatefulSets (Citus: `bexhoma-worker`,
  6 replicas; CockroachDB: `bexhoma-worker`, 3 replicas, the
  `bexhoma-deployment-cockroachdb` Deployment is a no-op placeholder; TiDB:
  three components — `bexhoma-pd`, `bexhoma-tikv` StatefulSets plus
  `bexhoma-deployment-tidb`). A single `deployment:` string is not enough
  for these — see `topology:` below.
- YugabyteDB is the most irregular case in the whole catalog: its
  `deploymenttemplate-YugabyteDB.yml` Deployment (image `postgres:15.0`) is
  a **placeholder** so bexhoma's generic lifecycle code has something to
  create a PVC/Service/bookkeeping object against. The real engine is
  installed by a **Helm chart** (`deploymenttemplate-YugabyteDB-values.yml`
  is a Helm `values.yaml`, not a k8s manifest), and `ycsb.py:419-452`
  manually patches `config.deployment_infos['statefulset']` for
  `yb-master`/`yb-tserver` after the fact
  (`bexhoma/old_configurations.py:11`: *"handled outside of bexhoma with the
  official helm chart"*). This needs a `deployment_kind: helm-external`
  concept the current draft doesn't have.
- DatabaseService is the other irregular case: *"Bexhoma does neither start
  nor stop the DBMS... does not know what resides inside"*
  (`docs/Example-CloudDatabase.md:8-14`), but it still deploys a real
  do-nothing `bexhoma-deployment-postgres` pod purely so the experiment has
  something to attach status bookkeeping to — the actual JDBC `url` is
  hardcoded to an external DNS name (`docs/DBMS.md:788-805`). Needs
  `deployment_kind: endpoint`, with `image`/`knobs`/`monitor` all optional
  and a `connection:` field instead.

### Non-DBMS and composite shapes that don't fit "system = one Deployment with knobs"

1. **Hardware benchmarking** (`hardware.py`) — no DBMS at all. `bexhoma/experiments/hardware.py:52-58`
   sets `self.loading_deactivated = True` unconditionally, with the comment
   *"Hardware has no loading phase in any mode."* The four tools
   (fio/sysbench/sockperf/netperf) sweep their own tool-specific parameters,
   not server GUCs, and there's no indexes/constraints/statistics concept.
   **Verdict: doesn't belong under `systems:` or `workloads:` — it gets its
   own top-level `tools:` key** (see catalog below), which is why the
   catalog gained a third top-level section in this revision.

2. **Redis / Dragonfly** — real systems, but categorically no SQL layer:
   *"Redis does not have dedicated DDL scripts; YCSB manages
   table/key-space creation directly via the Redis wire protocol"*
   (`docs/DBMS.md:774`). No `physical_design` concept applies at all (not
   even `false` — the concept is absent, not unsupported). Only YCSB targets
   them (`supports: [ycsb]`), never TPC-H/TPC-DS/Benchbase/HammerDB.
   **Verdict: `physical_design` must be nullable/absent, not just
   false-valued, and a system's presence in a workload's `supports:` list is
   the only gate — no implicit "every system supports every workload".**

3. **PGBouncer** — models as *one component of a two-component system*, not
   two independent `systems:` entries composed together: the JDBC URL points
   at the pooler port while `datadir`/`logfile` still describe the
   underlying PostgreSQL paths (`docs/DBMS.md:336-373`). `ycsb.py:275-305`
   builds a dedicated `configurations.default(docker='PGBouncer', ...)`
   with its own knob namespace (`MAX_CLIENT_CONN`, pool replica count)
   layered on top of the real PostgreSQL SUT.
   **Verdict: `systems:` entries need an optional secondary
   `pool_component:` block (own image, own knobs, own replica count) rather
   than a generic multi-entry composition.**

4. **Multi-Tenant** — not a system-shape problem at all: one engine, N
   tenants sharing the same Deployment, via global `-mtn`/`-mtb` flags
   (`bexhoma/cli_args.py:111-112`, tenancy granularity `schema`/`database`/
   `container`). **Verdict: fits the existing schema; needs a cross-cutting
   experiment-level `tenancy: {num_tenants, tenant_by}` block, orthogonal to
   any one system's knobs** — same pattern as `observe:`.

5. **Citus / CockroachDB / TiDB topology** — worker/shard/replica counts
   (`-nw`/`-nwr`/`-nws`) are a **third axis**, distinct from both `knobs`
   (server GUCs) and `physical_design` (indexes/constraints/statistics):
   cluster shape, not tunable server parameters.
   **Verdict: add a `topology: {num_workers, replicas, shards,
   attach_worker}` block to `systems:` entries that have it** —
   `attach_worker` documents how the coordinator learns about workers (a
   `master_add_node(...)` SQL call for Citus; `""`/none for CockroachDB,
   which auto-discovers cluster members per `docs/DBMS.md:607`).

### Two dormant hand-tuned PostgreSQL profiles found, unused in code

`k8s/deploymenttemplate-PostgreSQL-args.yml` and `-old.yml` exist, are
never referenced by any entry script (confirmed via grep across all `.py`
files), and are exactly the shape of a catalog `profiles:` entry — expert
tuning choices sitting in the repo with no name and no way to select them
today:

- **`-args.yml`** — large-node OLTP: `max_connections=3000`,
  `shared_buffers=256GB`, `work_mem=32GB`, `checkpoint_timeout=12h`,
  `fsync=on`, `wal_compression=on`, `synchronous_commit=on`.
- **`-old.yml`** — older baseline (`postgres:16.1`):
  `random_page_cost=60`, `synchronous_commit=off`.

An earlier revision of this doc turned both into named profiles
(`oltp-large-node`, `legacy-baseline`) purely by transcribing what was
already sitting unused in the repo. Per explicit instruction, the catalog
now only references the shipped baseline (`deploymenttemplate-PostgreSQL.yml`)
— neither variant template is used anywhere, in the catalog sketch below or
in `contracts/contract_catalog.yml`. Noted here only as a finding from the
audit, not as something implemented.

### `docs/DBMS.md` is stale in places — verify against templates, not prose

`docs/DBMS.md:292` claims PostgreSQL's "only active argument is
`max_connections=640`" — the live template has **17** active knobs, not 1.
The doc has **no section for CedarDB or PgDuckDB at all**, despite both
being live `-dbms` choices — i.e. the two systems this project is about to
implement first are the two least-documented in the repo. Treat `DBMS.md`
prose (the `why:` framing) as reusable, but verify every default/count
against the live `k8s/deploymenttemplate-*.yml` before it goes in the
catalog.

## Schema extensions this audit forces

Consolidating the above into concrete additions to what was originally
proposed:

1. `systems.<name>.arg_style`: `pg-guc | flag-equals | command-string |
   helm-values | none` — declares whether `knobs:` are reachable through
   the existing `--set` mechanism at all.
2. `systems.<name>.deployment_kind`: `managed` (default) | `helm-external`
   (YugabyteDB) | `endpoint` (DatabaseService) — governs whether
   `image`/`knobs`/`monitor` are meaningful or replaced by a
   `connection:` field.
3. A knob can override its system's `arg_style` individually — e.g.
   PgDuckDB is `arg_style: pg-guc` overall, but `duckdb_force_execution`
   specifically is `arg_style: env-var` (routes through bexhoma's existing
   `sut_parameters` mechanism, not `patch_dbms_args()`).
4. `systems.<name>.pool_component`: optional block (`deployment`, `image`,
   `knobs`, `replicas`) for sidecar/pooler components (PGBouncer).
5. `systems.<name>.topology`: optional block (`num_workers`, `replicas`,
   `shards`, `attach_worker`) for coordinator+worker systems (Citus,
   CockroachDB, TiDB).
6. `systems.<name>.physical_design` is **absent** (not `false`) for systems
   with no DDL concept at all (Redis, Dragonfly) — the workload's
   `supports:` list is what actually gates applicability, physical_design
   only refines *which* post-load steps a supported system honors.
7. `workloads.<name>.params.<key>.unit` is mandatory whenever a numeric
   parameter's meaning depends on it — it documents the CLI-facing unit an
   agent writes into `experiment.yaml` (e.g. `duration: {unit: minutes}`),
   which stays constant across workloads even when bexhoma converts it to a
   different unit per backend tool internally (see `-xsd`/`-xli` above).
8. New top-level `tools:` key for non-DBMS, non-workload benchmarks
   (hardware) — forcing hardware into `systems:`/`workloads:` would be
   worse than a third top-level key with a different internal shape.
9. Experiment-level (not catalog-level) `tenancy:` block, same pattern as
   the already-planned `observe:` block — cross-cutting concerns don't all
   need catalog entries.
10. `workloads.<name>.produces` (and `tools.<name>.produces`) documents what
    an experiment against this workload actually yields, so an agent can
    tell up front whether a hypothesis is even answerable — e.g. "which
    query is the bottleneck" needs `per_query`, but YCSB/Benchbase only ever
    produce `per_operation`/whole-workload `summary` plus a `time_series`,
    never a per-query breakdown, because neither tool has a query concept.
    Grounded in what each `evaluators/*.py` class actually exposes, not the
    workload's *parameters* (`params`/`loading`/`rounds` document what you
    can configure; `produces` documents what you get back). Shapes seen so
    far: `per_query` (tpch/tpcds, one row per query), `per_operation`
    (ycsb, one row per op type: READ/UPDATE/INSERT/SCAN/...),
    `per_procedure` (hammerdb, NEWORD only, and only when
    `record_latency_profile` is set), `summary` (one row per phase,
    every workload has this), `time_series` (ycsb/benchbase only — a
    running per-second signal DBMSBenchmarker/HammerDB don't produce), and
    `quality` (tpch/tpcds SQL error/warning counts, recorded as pass/fail
    tests rather than performance data). A workload lacking a shape omits
    the key rather than setting it to `false` — same "absent, not false"
    idiom point 6 already established for `physical_design`.

## Complete `catalog.yaml` (breadth pass)

Full parameter breadth for every workload; full knob depth only for
PostgreSQL and PgDuckDB (the near-term implementation target). Every other
system is structural: deployment shape, patch mechanism, physical-design
capability — enough to prove the schema fits, not a tuning reference yet.

```yaml
workloads:
  tpch:
    why: "star-schema OLAP: 22 queries, multi-way joins, official TPC-H"
    supports: [PostgreSQL, MonetDB, MySQL, MariaDB, DatabaseService, Citus, CedarDB, PgDuckDB]
    modes: [profiling, run, start, load, empty, summary]
    params:
      scaling_factor:        {type: int, unit: GB, why: "TPC-H scale factor, controls DB size"}
      timeout:                {type: int, unit: seconds, why: "per-query timeout"}
      query_repeats:          {type: int, default: 1, why: "repeat each query N times per round"}
      verify_result:          {type: bool, default: false, why: "validate result rows meet basic sanity checks"}
      measure_datatransfer:   {type: bool, default: false, why: "additionally record bytes transferred per query"}
      active_queries:         {type: list[int], default: all, why: "restrict to a query subset, e.g. 5,7,8,9,21 = multi-way joins"}
      recreate_parameter:     {type: bool, default: false, why: "regenerate random query parameters for each stream"}
      shuffle_queries:        {type: bool, default: false, why: "shuffle query execution order independently per stream"}
      limit_import_table:     {type: str, default: "", why: "import only this table (partial re-loads)"}
      refresh_streams:        {type: int, default: 0, why: "number of RF1/RF2 refresh-stream pairs run parallel to query streams"}
      refresh_stream_offset:  {type: int, default: 0, why: "starting OFFSET+1 for the refresh stream"}
      verbose_explain:        {type: bool, default: false, why: "run and print configured EXPLAIN statements after each benchmark query (requires an 'explain' key in the DBMS connection's JDBC config)"}
    loading:
      pods:    {type: int, min: 1, why: "number of parallel loader pods"}
      threads: {type: int, min: 1, why: "loader threads, split across pods"}
      split:   {type: int, default: 1, why: "number of parallel loader batches"}
      post_load:
        indexes:        {type: bool, default: false, why: "create indexes on all tables after loading"}
        constraints:    {type: bool, default: false, why: "add PK/FK constraints after loading"}
        statistics:     {type: bool, default: false, why: "run ANALYZE after loading"}
        storage_format: {type: enum, values: [heap, columnar], default: heap, why: "Citus only: switch to native columnar table storage"}
    rounds:       {type: list[int], why: "comma-separated parallel-client sweep, one benchmarking round per entry"}
    repetitions:  {type: int, default: 1, why: "how many times the whole round list repeats"}
    system_specific:
      PgDuckDB:
        duckdb_force_execution: {type: bool, default: false, why: "force every query through DuckDB's execution engine rather than pg_duckdb's own cost-based routing"}
    produces:
      per_query: {metric: latency, unit: ms, why: "DbmsBenchmarkerEvaluator.get_query_latencies(), one row per active query"}
      summary:   {metrics: [Power@Size, Throughput@Size, "Geo Times"], why: "get_summary_benchmark_per_phase(), geo-mean across queries — the level comparisons are actually made on"}
      quality:   {metric: sql_errors_warnings, why: "get_total_errors()/get_total_warnings(), pass/fail tests, not a performance metric"}
      # no time_series — DBMSBenchmarker has no running per-second signal

  tpcds:
    why: "star-schema OLAP, larger/more complex query set than TPC-H"
    supports: [PostgreSQL, MonetDB, MySQL, MariaDB]
    modes: [profiling, run, start, load, empty, summary]
    params:
      # identical to tpch's params minus refresh_streams/refresh_stream_offset
      scaling_factor: {type: int, unit: GB}
      timeout:        {type: int, unit: seconds}
      query_repeats:  {type: int, default: 1}
      verify_result:  {type: bool, default: false}
      measure_datatransfer: {type: bool, default: false}
      active_queries: {type: list[int], default: all}
      recreate_parameter: {type: bool, default: false}
      shuffle_queries: {type: bool, default: false}
      limit_import_table: {type: str, default: ""}
    loading:
      pods: {type: int}
      threads: {type: int}
      split: {type: int, default: 1}
      post_load:
        indexes: {type: bool, default: false}
        constraints: {type: bool, default: false}
        statistics: {type: bool, default: false}
        storage_format:
          type: enum
          values: [heap]     # NOTE: parsed (-xcol) but inert — no Citus branch wired into tpcds.py
          status: "flag exists, has no effect for this workload today"
    rounds: {type: list[int]}
    repetitions: {type: int, default: 1}
    produces:
      per_query: {metric: latency, unit: ms, why: "same DbmsBenchmarkerEvaluator as tpch, one row per active query"}
      summary:   {metrics: [Power@Size, Throughput@Size, "Geo Times"], why: "get_summary_benchmark_per_phase()"}
      quality:   {metric: sql_errors_warnings, why: "get_total_errors()/get_total_warnings()"}
      # no time_series — same evaluator/limitation as tpch

  ycsb:
    why: "key-value / simple-schema workload, 6 access-pattern mixes"
    supports: [PostgreSQL, MySQL, MariaDB, YugabyteDB, CockroachDB, TiDB, DatabaseService, PGBouncer, Redis, Citus, CedarDB, Dragonfly]
    modes: [run, start, load, summary]
    workload_variant:
      type: enum
      values: [a, b, c, d, e, f]
      why: "a=read-heavy 50/50, b=read-mostly, c=read-only, d=read-latest, e=scan, f=read-modify-write"
    params:
      operations_millions: {type: int, default: null, why: "total op count in millions; overrides scale-factor-derived op count"}
      target_base:          {type: int, default: 16384, why: "base ops/sec target; multiplied by per-phase factors below"}
      loading_target_factors:      {type: list[float], default: "1", why: "multipliers on target_base for the loading phase"}
      benchmarking_target_factors: {type: list[float], default: "1", why: "multipliers on target_base for the benchmarking phase"}
      batchsize:             {type: int, default: null, why: "insert batch size"}
      logging_interval:      {type: int, unit: seconds, default: 10}
      insert_order:          {type: enum, values: [hashed, ordered], default: hashed}
      max_execution_time:    {type: int, unit: seconds, default: 0, why: "cap on benchmarking phase only (0=no limit); loading always runs to completion"}
    loading: {pods: {type: int}, threads: {type: int}}
    pooling:    # only meaningful when systems.<name>.pool_component is present (PGBouncer)
      pods:    {type: list[int]}
      max_in:  {type: list[int]}
      max_out: {type: list[int]}
    system_specific:
      TiDB:
        sut_replicas: {type: int, default: 1}
        pd_nodes:     {type: int, default: 3, why: "keep odd"}
    rounds: {type: list[int]}
    repetitions: {type: int, default: 1}
    produces:
      per_operation: {metrics: [throughput, latency_avg, latency_p95, latency_p99], unit: "ops/sec | us", why: "one row per YCSB op type (READ/UPDATE/INSERT/SCAN/READ-MODIFY-WRITE/...), get_summary_benchmark_per_phase()"}
      time_series:   {metric: current_ops_per_sec, unit: ops/s, interval: 1s, why: "per-second throughput, both benchmarking and loading phases, get_*_logs_timeseries_df_*()"}
      # no per_query — YCSB has no query concept, only op-type buckets

  benchbase:
    why: "Java driver bundling multiple OLTP/hybrid suites behind one loader"
    supports: [PostgreSQL, MySQL, MariaDB, YugabyteDB, CockroachDB, TiDB, DatabaseService, Citus, PGBouncer, CedarDB]
    modes: [run, start, load]     # no summary mode
    benchmark_type:
      type: enum
      values: [tpcc, twitter, chbenchmark, ycsb]
      default: tpcc
      why: "tpcc=TPC-C; twitter=Twitter workload; chbenchmark=hybrid TPC-C/TPC-H; ycsb=YCSB-under-Benchbase"
    params:
      workload:              {type: enum, values: [a,b,c,d,e,f,c2], why: "YCSB workload letter, only used when benchmark_type=ycsb"}
      duration:               {type: int, unit: minutes, default: 5, why: "converted to seconds internally — Benchbase's own BENCHBASE_TIME field natively wants seconds"}
      logging_interval:       {type: int, unit: milliseconds, default: 0, why: "0=disabled"}
      keying_and_think_time:  {type: bool, default: false, why: "simulate TPC-C keying/think times between transactions"}
      new_connection_per_txn: {type: bool, default: false}
      insert_batchsize:       {type: int, default: 128}
      target_base:            {type: int, default: 1024}
      benchmarking_target_factors: {type: list[float], default: "1"}
    pooling: {pods: {type: list[int]}, max_in: {type: list[int]}, max_out: {type: list[int]}}
    system_specific:
      TiDB:
        sut_replicas: {type: int, default: 1}
        pd_nodes:     {type: int, default: 3}
    rounds: {type: list[int]}
    repetitions: {type: int, default: 1}
    note: "num_worker defaults to 1 for this workload (base-parser default is 0) — a per-script default override to be aware of"
    produces:
      summary:     {metrics: [Throughput, Goodput, "Latency Distribution (min/25/50/75/90/95/99/max/avg)"], unit: "req/s | us", why: "get_summary_benchmark_per_phase()"}
      time_series: {metric: throughput, unit: txn/s, why: "per-second INFO-log throughput parse, get_benchmark_logs_timeseries_df_*()"}
      # no per_query — Benchbase reports whole-workload throughput/latency only, not per-transaction-type

  hammerdb:
    why: "Tcl-driven TPC-C implementation; loading phase does not scale"
    supports: [PostgreSQL, MySQL, MariaDB, Citus]
    modes: [run, start, load, summary]
    params:
      rampup:                {type: int, unit: minutes, default: 2, why: "ramp-up period before measurements begin"}
      duration:               {type: int, unit: minutes, default: 5, why: "passed straight through — HammerDB's own diset duration interface natively wants minutes"}
      record_latency_profile: {type: bool, default: false, why: "per-transaction TIMEPROFILE; drives p95/p99 evaluator columns"}
      keying_and_think_time:  {type: bool, default: false, why: "gates efficiency calc (vusers==scaling_factor*10)"}
    loading:
      pods: {type: int, status: "parsed but ignored — always 1 pod; only threads actually scales"}
      threads: {type: int}
    fixed_credentials:
      Citus: {user: postgres, password: password1234, why: "hardcoded, not exposed as a flag — do not imply it's configurable"}
    rounds: {type: list[int]}
    repetitions: {type: int, default: 1}
    produces:
      summary:       {metrics: [NOPM, TPM, efficiency], why: "get_summary_benchmark_per_phase(); efficiency only meaningful when keying_and_think_time is set and vusers==10*scaling_factor, else 0"}
      per_procedure: {metric: latency, unit: ms, why: "CALLS/MIN/AVG/MAX/TOTAL/P50/P95/P99 for the NEWORD procedure only, present when record_latency_profile is set — absent otherwise"}
      # no time_series — HammerDB logs one TEST RESULT line per iteration, not a running signal

tools:
  hardware:
    why: "microbenchmarks a node directly — disk I/O, CPU/memory, network; no DBMS, no loading phase"
    modes: [run, start, summary]
    tool:
      type: enum
      values: [fio, sysbench, sockperf, netperf]
    params_by_tool:
      fio:      {rw: {values: [write, read, randwrite, randread, randrw]}, blocksize: {type: str}, iodepth: {type: list[int]}, engine: {values: [sync, libaio, io_uring]}, fsync: {type: list[int]}, fdatasync: {type: list[int]}, rwmixread: {type: list[int], why: "only meaningful when rw=randrw"}}
      sysbench: {threads: {type: int}}
      sockperf: {mode: {values: [pp, ul]}, protocol: {values: [tcp, udp]}, mps: {type: str, why: "'max' or a positive integer"}, msgsize: {type: list[int]}}
      netperf:  {protocol: {values: [tcp, udp]}, threads: {type: int}}
    note: "the shared 'threads-per-benchmarker' flag is overloaded: fio numjobs, sysbench --threads, netperf concurrency — same name, three tool-specific meanings"
    produces:
      summary_by_tool:
        fio:      {metrics: [read_iops, write_iops, read_bw_kbps, write_bw_kbps, "latency percentiles P01..P9999"], unit: "IOPS | KiB/s | ms"}
        sysbench: {metrics: [cpu_events_per_sec, cpu_lat_p95, memory_ops_per_sec, memory_throughput_mibps, memory_lat_p95], unit: "ops/s | MiB/s | ms"}
        sockperf: {metrics: [latency_avg, latency_p50, latency_p99, latency_p999, msg_rate, dropped_rate], unit: "ms | msg/s"}
        netperf:  {metrics: [transaction_rate, latency_avg, latency_p50, latency_p90, latency_p99, instances_failed], unit: "txn/s | ms"}
      why: "one shot-summary per pod/tool (HardwareEvaluator, images/hardware/benchmarker/*.sh); no per-query concept, no time-series"

systems:
  PostgreSQL:
    deployment: bexhoma-deployment-postgres
    image: postgres:18.3
    arg_style: pg-guc
    knobs:
      # active in the shipped template today
      max_connections:                 {type: int, default: 640}
      max_worker_processes:            {type: int, default: 16}
      max_parallel_workers:            {type: int, default: 16}
      max_parallel_workers_per_gather: {type: int, default: 8}
      max_parallel_maintenance_workers: {type: int, default: 4}
      shared_buffers:                  {type: memory, default: 16GB}
      effective_cache_size:            {type: memory, default: 40GB}
      work_mem:                        {type: memory, default: 512MB}
      maintenance_work_mem:            {type: memory, default: 2GB}
      autovacuum:                      {type: enum, values: [on, off], default: off}
      wal_level:                       {type: enum, values: [minimal, replica, logical], default: minimal}
      max_wal_senders:                 {type: int, default: 0}
      max_wal_size:                    {type: memory, default: 32GB}
      checkpoint_timeout:              {type: duration, default: 1h}
      checkpoint_completion_target:    {type: float, default: 1.0}
      lock_timeout:                    {type: duration, default: 30s}
      idle_in_transaction_session_timeout: {type: int, unit: ms, default: 30000}
      # known (commented reference in the template) but not active by default — legal to set via profile/override
      effective_io_concurrency: {type: int, status: reference-only}
      io_method:                 {type: enum, values: [sync, io_uring], status: reference-only}
      random_page_cost:          {type: float, status: reference-only}
      seq_page_cost:             {type: float, status: reference-only}
      default_statistics_target: {type: int, status: reference-only}
      fsync:                     {type: enum, values: [on, off], status: reference-only}
      synchronous_commit:        {type: enum, values: [on, off], status: reference-only}
      # + ~15 more reference-only knobs (autovacuum/WAL/lock tuning) — see k8s/deploymenttemplate-PostgreSQL.yml:115-225
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    profiles:
      analytical-ssd:
        why: "OLAP on node-local NVMe, sized from this experiment's memory limit"
        requires: {storage_class: [ssd, null]}  # null = ephemeral also accepted, see below
        knobs:
          random_page_cost: 1.1
          effective_io_concurrency: 200
          io_method: io_uring
          max_parallel_workers_per_gather: 2
          max_parallel_workers: 4
          max_worker_processes: 6
        derive:
          shared_buffers:       0.3125  * memory_limit
          effective_cache_size: 0.75    * memory_limit
          work_mem:              0.015625 * memory_limit
          maintenance_work_mem:  0.03125  * memory_limit
      # Two dormant, code-unreferenced templates (deploymenttemplate-PostgreSQL-args.yml,
      # -old.yml) were found during the audit and could become named profiles here
      # (large-node OLTP; an older postgres:16.1 baseline) — deliberately not added,
      # per instruction to reference only the shipped baseline template. See
      # "Two dormant hand-tuned PostgreSQL profiles found" above.

  PgDuckDB:
    extends: PostgreSQL       # formalizes tpch.py's own path_experiment_docker='PostgreSQL' DDL reuse
    deployment: bexhoma-deployment-pg-duck
    image: pgduckdb/pgduckdb:18-v1.1.1
    arg_style: pg-guc
    knobs:
      shared_preload_libraries: {type: str, default: pg_duckdb, fixed: true}
      # inherits PostgreSQL's 17 active knobs unchanged — PgDuckDB's template is a strict subset plus this one addition
      duckdb_force_execution:
        type: bool
        default: false
        arg_style: env-var          # NOT a -c GUC — routes through bexhoma's sut_parameters, not patch_dbms_args()
        env_var: DUCKDB_FORCE_EXECUTION
        why: "force every query through DuckDB execution rather than pg_duckdb's own cost-based routing"
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    # storage_format: columnar (native `USING duckdb` tables) is not usable yet — blocked upstream
    # (github.com/duckdb/pg_duckdb#385); experiments/tpch/PgDuckDB/ is orphaned, tpch.py currently
    # points PgDuckDB at experiments/tpch/PostgreSQL/ instead. Do not list columnar as supported yet.
    profiles:
      analytical-ssd: {ref: PostgreSQL.profiles.analytical-ssd}   # same profile object, both systems — this is what "parity" means

  CedarDB:
    deployment: bexhoma-deployment-cedardb
    image: cedardb/cedardb
    arg_style: none
    dialect: PostgreSQL        # wire/dialect reuse for query translation only — NOT DDL reuse (has its own DDL folder, unlike PgDuckDB)
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    note: "least-instrumented template in the catalog — no postStart/preStop/probes wired up; no docs/DBMS.md section exists yet"

  MySQL:
    deployment: bexhoma-deployment-mysql
    image: mysql:8.4.0
    arg_style: flag-equals    # NOT patchable via today's --set mechanism
    knobs_summary: "~19 active (innodb_buffer_pool_size, innodb_redo_log_capacity, innodb_io_capacity, innodb_flush_log_at_trx_commit, skip_log_bin, tmpdir, ...), ~12 reference-only — see k8s/deploymenttemplate-MySQL.yml"
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}

  MariaDB:
    extends: MySQL             # dialect reuse for query translation, confirmed in cluster.config('dialect': 'MySQL') — own image/template/DDL folder, no DDL reuse
    deployment: bexhoma-deployment-mariadb
    image: mariadb:11.4.7
    arg_style: flag-equals
    knobs_summary: "~14 active (innodb_buffer_pool_size, innodb_read/write_io_threads, innodb_flush_log_at_trx_commit, innodb_doublewrite, ...) — see k8s/deploymenttemplate-MariaDB.yml"
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}

  MonetDB:
    deployment: bexhoma-sut-monetdb   # breaks the bexhoma-deployment-<key> naming convention every other system follows
    image: monetdb/monetdb:Dec2025-SP3
    arg_style: none
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}

  Citus:
    deployment: bexhoma-deployment-citus
    image: citusdata/citus:13.2.0-alpine
    arg_style: pg-guc
    knobs_summary: "26 active -c pairs, same vocabulary as PostgreSQL — see k8s/deploymenttemplate-Citus.yml"
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap, columnar]}   # native citus_columnar, not the deprecated cstore_fdw
    topology:
      worker_component: {deployment: bexhoma-worker, kind: StatefulSet, default_replicas: 6}
      num_workers: {cli: -nw}
      replicas: {cli: -nwr}
      shards: {cli: -nws}
      attach_worker: "SELECT master_add_node('{worker}.{service_sut}', 5432)"

  CockroachDB:
    deployment: bexhoma-deployment-cockroachdb   # placeholder no-op container — NOT the real SUT
    arg_style: command-string    # --cache/--max-sql-memory derived from $MEMORY_LIMIT_MIB at container start — unreachable via --set
    image: cockroachdb/cockroach:v24.2.4
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    topology:
      worker_component: {deployment: bexhoma-worker, kind: StatefulSet, default_replicas: 3, note: "this StatefulSet, not the placeholder Deployment, is the real SUT"}
      attach_worker: null   # CockroachDB auto-discovers cluster members
    note: "has its own idempotent cluster-init Job (batch/v1)"

  TiDB:
    arg_style: command-string    # unreachable via --set
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    topology:
      pd_component:   {deployment: bexhoma-pd, kind: StatefulSet, image: pingcap/pd:v7.1.6, default_replicas: 3}
      tikv_component: {deployment: bexhoma-tikv, kind: StatefulSet, image: pingcap/tikv:v7.1.6, default_replicas: 3}
      sut_component:  {deployment: bexhoma-deployment-tidb, kind: Deployment, image: pingcap/tidb:v7.1.6}
    note: "elaborate init-container choreography (pd-init sizes --initial-cluster non-destructively, wait-for-pd on tikv); needs DAC_OVERRIDE capability for a yum-install workaround"

  YugabyteDB:
    deployment_kind: helm-external
    deployment: bexhoma-deployment-yugabytedb   # placeholder only (image postgres:15.0) — real engine is Helm-managed
    arg_style: helm-values
    knobs_summary: "gflags.tserver.ysql_enable_packed_row, ysql_max_connections, resource.master/tserver cpu/mem/replicas — see k8s/deploymenttemplate-YugabyteDB-values.yml (a Helm values.yaml, not a bexhoma k8s template)"
    physical_design: {indexes: true, constraints: true, statistics: true, storage_format: [heap]}
    topology:
      note: "yb-master/yb-tserver StatefulSets are created by Helm, not bexhoma; ycsb.py manually injects deployment_infos['statefulset'] entries after the fact to make monitoring/pod-discovery work"
    constraints: {max_sut_dbms: 1, why: "cluster-wide singleton — hardcoded, not exposed as a flag"}

  Redis:
    deployment: bexhoma-deployment-redis
    image: redis:8.6.1
    arg_style: flag-equals    # --maxclients, --io-threads — not -c prefixed, not patchable by ensure_arg_pairs() today
    physical_design: null     # not false — the concept doesn't apply; no DDL folder exists at all
    supports_workloads: [ycsb]

  Dragonfly:
    deployment: bexhoma-deployment-dragonfly
    image: docker.dragonflydb.io/dragonflydb/dragonfly:v1.37.0
    arg_style: command-string   # --admin_port/--maxmemory baked into a shell command: block — unreachable via --set
    physical_design: null
    supports_workloads: [ycsb]
    variants:
      DragonflyCluster: {extends: Dragonfly, adds: {worker_component: {deployment: bexhoma-worker, kind: StatefulSet}, init_job: cluster-init}, election: "ordinal-based master/replica via $POD_NAME"}
      DragonflyReplica: {extends: Dragonfly, adds: "same as DragonflyCluster, different replica topology"}

  PGBouncer:
    extends: PostgreSQL          # the SUT component genuinely is bexhoma-deployment-postgres
    pool_component:
      deployment: bexhoma-pool
      image: edoburu/pgbouncer:v1.25.1-p0
      knobs:
        max_client_conn:  {type: int}
        default_pool_size: {type: int}
        min_pool_size:     {type: int}
      replicas: {cli: pooling.pods}

  DatabaseService:
    deployment_kind: endpoint
    deployment: bexhoma-deployment-postgres   # do-nothing bookkeeping placeholder — not the real target
    arg_style: none
    connection:
      url: "fixed at deploy time to bexhoma-service.{namespace}.svc.cluster.local — bexhoma does not manage the real endpoint"
    monitor: unavailable
    physical_design: unknown   # bexhoma has no visibility into the real DBMS behind the endpoint
```

`Dummy` (busybox scaffold, `k8s/deploymenttemplate-Dummy.yml`) and the
infra-only templates (`bexhoma-dashboard`, `bexhoma-messagequeue`,
`bexhoma-prometheus`) are intentionally excluded — they're not benchmarkable
systems.

## Required header fields

Every experiment.yml must carry three top-level fields before anything
workload/system-specific: `title` (a short human-readable name), `hypothesis`
(what the experiment is testing, in prose), and `discriminates` (a list of
the factor(s) the experiment isolates — e.g. `[system]` when everything
else is held constant across the `systems:` entries). `validate_experiment()`
checks all three are present and non-empty before resolving anything else —
an experiment.yml that can't say what it's testing fails immediately,
rather than producing a technically-valid but purposeless run.

## Top-level shape

`mode`, `title`, `hypothesis`, `discriminates`, `workload`, `loading`,
`systems`, `observe`, `placement`, and `resources` are all siblings at the
top of the file. The one pitfall worth calling out explicitly: `loading:` is
**not** nested under `workload:`, even though it's workload-specific data.
`build_argv()` reads it as `experiment.get("loading", {})` off the top-level
dict, not off `workload_spec`, so a `workload.loading` block is not a schema
error — it resolves silently to `{}`, and the `-nlp`/`-nlt`/`-xii`/`-xic`/
`-xis`/`-xcol` flags it would have produced are just absent from the
translated command. See the worked example below for the correct shape.

## Worked example: TPC-H, PostgreSQL vs. PgDuckDB

This is now a real, runnable file — `dev/catalog/experiment.yml`, reproduced
here for reference (kept in sync manually; if they drift, the file on disk
is authoritative):

```yaml
mode: run

title: "TPC-H joins under concurrency and RAM pressure: PostgreSQL vs. PgDuckDB at SF10"
hypothesis: "pg_duckdb outperforms PostgreSQL on join-heavy TPC-H queries (Q5, Q7, Q8, Q9, Q21) at SF=10 under a matched analytical-ssd profile, and the advantage (if any) holds as concurrent client load increases from 1 to 16 and RAM tightens from 64Gi to 32Gi"
discriminates: [system, concurrency, memory]

workload:
  name: tpch
  params:
    scaling_factor: 10
    timeout: 1200
    query_repeats: 3
    verify_result: true
    active_queries: [5, 7, 8, 9, 21]
  rounds: [1, 2, 3, 4]
  repetitions: 3

loading:
  pods: 4
  threads: 4
  # shared default for every system below — indexes/stats matter directly for
  # join plan quality. Deliberately identical for both systems: this pair is
  # compared under a matched profile, so post_load is a "parity" input, same
  # as `profile: analytical-ssd` below. A systems[].post_load override (not
  # used here, on purpose) would let one experiment apply post_load to some
  # named systems and not others — see contract_catalog.yml's post_load comment.
  post_load: {indexes: true, constraints: true, statistics: true}

systems:
  - name: PostgreSQL
    profile: analytical-ssd
  - name: PgDuckDB
    profile: analytical-ssd
    override: {duckdb_force_execution: false}

observe: {monitoring_sut: true, monitoring_cluster: true, monitoring_app: true}

placement:
  sut: node-group-sut
  loading: node-group-load
  benchmarking: node-group-bm

resources:
  cpu: {request: 16, limit: 16}
  memory:
    - {request: 32Gi, limit: 32Gi}
    - {request: 64Gi, limit: 64Gi}
  storage: {size: 50Gi}
  storage_class: ssd  # one of the values the analytical-ssd profile's `requires.storage_class`
                       # allows ([ssd, null]) — anything else raises SpecError before any argv is produced
```

`resources.storage_class` is only constrained when a `profile:` declares
`requires: {storage_class: ...}`, as `analytical-ssd` does above.
`requires.storage_class` may be a single value or, as here, a list of
acceptable values — `resolve_system()` accepts the experiment's
`resources.storage_class` as long as it appears in that set. `null` in the
list means ephemeral is one of the accepted choices, alongside a specific
cluster-declared class. Leaving `resources.storage_class` unset is legal
for any system/profile without a `requires:` precondition (or one whose
list includes `null`, as here), and resolves to ephemeral storage: no
PersistentVolumeClaim is provisioned, the SUT instead gets whatever
node-local disk the scheduled node has attached — typically fast, since
there's no network-storage hop, but tied to that node's lifetime.
`resources.storage.size` still applies regardless.
`bexhoma/clusters.py::Kubernetes.get_available_storage_types()` documents
this as the CLI-facing contract (`-rst`/`--request-storage-type`): `None`/`''`
(ephemeral) and `'ramdisk'` (in-memory) are always valid, independent of the
cluster; any other value must be one of the cluster's actual declared
storage classes (`environment.yml`'s `storage_classes:`).

`duckdb_force_execution` in `override:` does **not** flow through the
`--set` path like `random_page_cost` etc. do. Per the catalog entry's
`arg_style: env-var`, `bexhoma/spec.py`'s `build_argv()` instead emits the
existing `-xdfe` CLI flag when the resolved value is true — `tpch.py`
already sets `config.sut_parameters['DUCKDB_FORCE_EXECUTION']` from that
flag itself (`tpch.py::run()`, in the `PgDuckDB` config block), so the
translator only needs to know the flag mapping, not reach into
`sut_parameters` directly. This is a concrete case of §"Schema extensions"
point 3: the resolver branches on each knob's own `arg_style`, not assuming
the whole system is uniform.

### Per-system `post_load` selection

The worked example above gives both systems the *same* `post_load` on
purpose (parity). To apply `indexes`/`constraints`/`statistics` to
`PostgreSQL` only, a `systems[].post_load` override replaces the shared
default for that one entry:

```yaml
loading:
  pods: 4
  threads: 4
  # no post_load here — nothing to default when every system sets its own

systems:
  - name: PostgreSQL
    profile: analytical-ssd
    post_load: {indexes: true, constraints: true, statistics: true}
  - name: PgDuckDB
    profile: analytical-ssd
    override: {duckdb_force_execution: false}
    # post_load omitted entirely -> resolves to {} (no top-level default to
    # fall back to), NOT to PostgreSQL's post_load -- each systems[] entry
    # resolves independently
```

This parses and validates (legality/support are both checked per system,
per "Validation ordering" above) and now translates: `PostgreSQL` and
`PgDuckDB` resolve to different effective post_load, so `build_argv()` emits
none of `-xii`/`-xic`/`-xis`/`-xcol` (a global flag can't represent a
divergent selection), and `bexhoma/spec.py::resolve_physical_design_overrides()`
instead resolves `{'PostgreSQL': 'Index_and_Constraints_and_Statistics',
'PgDuckDB': ''}` — one `initscripts` key per system (see `k8s-cluster.config`'s
`volumes.tpch.initscripts`). `experiment.py`'s catalog-driven dispatch attaches
this dict to the parsed `argparse.Namespace` as `physical_design_overrides`
before calling `tpch.run()` in-process; `tpch.py::run()` applies it right
after building every configuration, via the same per-configuration
`SutConfiguration.set_experiment(indexing=...)` override already used for
Citus/tenant special-casing (`tpch.py`'s PostgreSQL tenant-schema block and
Citus's `init_columns` block). This is a non-CLI channel — no new argparse
flag exists, and hand-typed
`python tpch.py ...` invocations never populate `physical_design_overrides`,
so their behavior is unchanged.

### Resource sweeps: `resources.memory`/`resources.cpu` as a list

`resources.memory` (and, independently, `resources.cpu`) may be a single
`{request, limit}` dict — shared by every system in `systems:`, no sweep,
exactly as above for `cpu` — or a list of them. A list crosses every
`systems:` entry against every list entry: two systems × two memory
entries resolves to four configurations (`PostgreSQL-32Gi`,
`PostgreSQL-64Gi`, `PgDuckDB-32Gi`, `PgDuckDB-64Gi`), each with its own
`derive:`d knob values (`shared_buffers` etc. computed from *that* cell's
`memory_limit`). This is the same "list = swept, scalar = shared" idiom
`workload.rounds` already uses for concurrency — see
`bexhoma/spec.py::build_argv()`'s `cpu_cells`/`memory_cells` handling.

Two things had to change below `spec.py` for this to actually run, not
just parse:

1. **`tpch.py`** parses `-rr`/`-lr`/`-rc`/`-lc` as comma-separated lists
   (`_resource_cells()`) and, for each DBMS already named in `-dbms`, loops
   over the resulting cells, calling `config.set_resources(...)` per cell —
   `SutConfiguration.set_resources()` already applied per-configuration
   resources correctly before this change; only the CLI/entry-script loop
   that calls it once per cell was missing. Each cell also gets its own
   `configuration=` name (`{docker}-{memory_request}`) and storage identity,
   so concurrent cells don't collide on the same PVC.
2. **The `--set` mechanism was experiment-global**, applied identically to
   every configuration matching a `deployment[NAME]` selector — two
   `PostgreSQL` cells would both receive whichever `shared_buffers` value
   was listed last. `SELECTOR_RE`
   (`bexhoma/experiments/base.py`) now accepts an optional
   `deployment[NAME]@CONFIG.container[...]` scope; `patch_dbms_args()`
   (`bexhoma/configurations/manifest.py`) silently skips any operation whose
   `@CONFIG` doesn't match its own `configuration` name. Unscoped `--set`
   (today's only form before this change) still applies to every matching
   configuration, so this is fully backward compatible.  `spec.py` predicts
   each cell's `{docker}-{memory_request}` name statically and emits one
   scoped `--set` per (system, cell, knob) triple.

This `--set @CONFIG` scoping is deliberately a thin CLI-layer bridge, not
the long-term mechanism: `resolve_system()`'s resolution (per-cell
`derive:` evaluation, `ResolvedSystem`/`ResolvedKnob`) is what stays
valuable if entry scripts ever parse `experiment.yml` directly instead of
being invoked via argv — at that point the resolved knobs could be handed
to `config.manifest.patch_dbms_args()` in-process, and the selector-string
scoping (and `build_argv()` itself) would no longer be needed.

## `derive:` expression language

Deliberately minimal: arithmetic over a fixed set of declared inputs
(`memory_limit`, `cpu_limit`, `storage_class`, `scaling_factor`). No
functions, no conditionals — richer than that and the catalog stops being
writable by the people who hold the tuning knowledge. Evaluated with a
whitelisted-node-type parser (e.g. `ast.parse` restricted to `BinOp`/`Num`/
`Name`, names restricted to the four inputs), never Python `eval()`.

Not every profile knob needs to be a `derive:` formula — most tuning
choices (see `oltp-large-node`/`legacy-baseline` above) are literal values
an expert picked once. Forcing e.g. `maintenance_work_mem: 2GB` into a
formula invents false precision it never had. `derive:` is opt-in, for the
handful of quantities an author genuinely wants recomputed per cell when a
resource limit is itself a swept factor.

## Validation ordering

Three distinct axes are in play for `loading.post_load`, the running
example — the third (selection) was added after the original two-axis
design shipped, once a concrete case (wanting `indexes`/`constraints`/
`statistics` applied to `PostgreSQL` but not a co-running `PgDuckDB` in the
same experiment) showed the two-axis model couldn't express it at all:

0. **Applicability** — is the system in the workload's `supports:` list at
   all? Checked before anything below — `tpch` against `Redis` fails
   immediately, since `Redis` isn't in `tpch.supports`.
1. **Legality** — does `workloads.tpch.loading.post_load.<key>` exist, and
   is the value legal for its declared `type`/`values`? (`storage_format:
   columnar` is a real workload concept — checked here regardless of which
   system is targeted.) Legality is checked against each system's
   *effective* post_load — its own `systems[].post_load` override if it has
   one, else the shared `loading.post_load` default (`_effective_post_load()`
   in `bexhoma/spec.py`) — not against one experiment-wide dict.
2. **Support** — for each system, is that value present in
   `systems.<name>.physical_design.<key>`? (`storage_format: columnar`
   against plain `PostgreSQL` fails *here*, specifically — the value is
   legal, just unsupported by *this* system. Against `Redis`, the whole
   `physical_design` check is skipped, not failed — the concept is absent,
   and step 0 should have already rejected `Redis` for `tpch`.)
3. **Selection** — *capable of* (step 2) is necessary but not sufficient for
   *will receive it*: a system can pass the support check and still not get
   a post_load option applied, because this experiment chose not to apply it
   there. This is what `systems[].post_load` (as opposed to the shared
   `loading.post_load`) actually expresses — see the worked example below.
   PgDuckDB's `physical_design` in `contract_catalog.yml` deliberately
   declares full support for `indexes`/`constraints`/`statistics` (identical to
   PostgreSQL's, not merely inherited via `extends`) precisely so that
   omitting them for PgDuckDB in a given `experiment.yml` reads as a
   selection choice, never a support failure.

Selection is a schema-level concept `bexhoma/spec.py` resolves; `tpch.py`'s
own CLI still can't *execute* a divergent selection through
`-xii`/`-xic`/`-xis`/`-xcol` — those stay global switches with no per-system
scope. `build_argv()` therefore computes each named system's effective
post_load and, when they all agree, emits the shared flags exactly as before;
when they diverge, it emits none of them and leaves the actual selection to
`resolve_physical_design_overrides()` — a separate, non-CLI channel — instead
of applying one system's choice to every system or refusing to translate at
all. See step 4 in "Integration with current code" below.

## Integration with current code (phase 1 — CLI stays ground truth)

**This section originally described a plan; it now describes what
`bexhoma/spec.py` actually does, which turned out simpler than first
sketched** — instead of reaching into `ExperimentBase.prepare_testbed()`'s
internals (pre-parsed `(selector_dict, value)` tuples merged directly into
`self.dbms_args`, `sut_parameters` populated by hand), the translator
targets one seam higher: it reuses `tpch.py`'s own `argparse` parser
end-to-end, by generating the same argument vector a human would type.
No changes to `tpch.py` or any other entry script were needed, and no code
had to duplicate the ~45 shared-flag defaults `bexhoma/cli_args.py`'s
`make_base_parser()` already owns.

1. `bexhoma/spec.py::load_catalog()`/`load_experiment()` load
   `contract_catalog.yml` and `experiment.yml` (plain `yaml.safe_load`, no
   relation to the `ast.literal_eval`-based `cluster.config` format).
2. `resolve_system()` resolves `extends:` chains, the named `profile:`
   (following a `ref:` to another system's profile when present), evaluates
   `derive:` formulas (`evaluate_derive_expression()`, a whitelisted-AST
   evaluator — verified to reject non-arithmetic constructs, including an
   attempted `__import__(...)` injection), and applies `override:`.
   `requires: {storage_class: ...}` (a single value or a list of acceptable
   values) is checked against the experiment's own `resources.storage_class`
   right here, raising `SpecError` before any argv is produced if it isn't
   one of them.
3. `validate_experiment()` checks, in order: the workload exists; every
   system is in the workload's `supports:` list; and, for each system's
   *effective* post_load (its own `systems[].post_load` override — a
   selection choice — or else the shared `loading.post_load` default), every
   option is legal for the workload and the system's `physical_design`
   actually supports the requested value.
4. `build_argv()` walks the resolved experiment and emits **only the CLI
   flags the spec actually sets** — e.g. `-sf`, `-t`, `-ne`, `-nc`, `-m`,
   `-rc`/`-lc`/`-rr`/`-lr`/`-rss`, `-rst` (derived from the resolved
   profile's `storage_class`) — falling back to `tpch.py`'s own argparse
   defaults for everything else. Before any of that, it computes every named
   system's effective post_load: `-xii`/`-xic`/`-xis`/`-xcol` are global CLI
   switches with no per-system scope in `tpch.py`, so when every system
   agrees, the shared flags are emitted exactly as before; when a
   `systems[].post_load` selection *diverges* across systems, none of those
   four flags are emitted at all — a global flag can't represent a divergent
   selection, so `resolve_physical_design_overrides()` (see "Per-system
   post_load selection" above) resolves it separately, outside argv
   entirely. Per-knob `arg_style` decides how a knob becomes CLI input:
   - `pg-guc` → a `--set deployment[<systems.<name>.deployment>].container[dbms].<knob>=<value>`
     token pair. `tpch.py`'s own `prepare_testbed()` parses these via the
     *existing* `parse_set_arg()` (`bexhoma/experiments/base.py:81`) exactly
     as if a human had typed `--set` — `build_argv()` never touches
     `dbms_args`/`patch_dbms_args()` directly.
   - `env-var` → mapped to whatever existing flag already sets that
     variable, when one exists (today: `duckdb_force_execution` →
     `-xdfe`). No generic env-var-to-CLI mapping exists yet, so any other
     `env-var` knob raises `SpecError` rather than being silently dropped.
   - `flag-equals`/`command-string`/`helm-values` → always raises
     `SpecError` ("not yet translatable to a CLI flag") — none of these
     apply to the PostgreSQL/PgDuckDB prototype pair, but the guard exists
     so extending the catalog to another system fails loudly instead of
     silently producing an incomplete command.
5. `build_command()` renders the argv as a copy-pasteable
   `python tpch.py ...` string; `translate()` chains steps 1–4 for a single
   call. The result is handed to a human, or to `subprocess`/CI — there is
   no in-process call into `prepare_testbed()` yet (see below).

**Not built**: a live call from `spec.py` into `prepare_testbed()` (the
generated argv is not currently fed back through `tpch.py`'s own parser
*and executed* in the same process — `dev/spec_prototype_demo.py` parses it
only to validate shape); a new `bexhoma spec run experiment.yaml` CLI
subcommand; and, per the "Near-term implementation scope" section below,
everything needed for systems beyond PostgreSQL/PgDuckDB
(`flag-equals`/`command-string`/`helm-values` knobs, `pool_component`,
`topology`).

### Phase 2 (later)

Once the catalog is trusted as ground truth:

- Generate/validate each entry script's `-x`-prefixed argparse flags *from*
  the catalog instead of hand-maintaining both in parallel.
- `k8s/deploymenttemplate-*.yml`'s currently-commented-out knob blocks
  become the generated content of `contract_catalog.yml`'s `systems`
  section — template renders from catalog, not the reverse.
- Extend the `flag-equals`/`command-string` systems' templates so their
  knobs become genuinely patchable (this is real implementation work per
  system, not just a catalog-authoring exercise — today's `--set` mechanism
  literally cannot reach them).
- `experiment.yaml` becomes the persisted/versioned artifact; the CLI
  becomes a thin generator over it.

## Near-term implementation scope

Per discussion: **TPC-H, PostgreSQL vs. PgDuckDB only**, first. Concretely
this means phase-1 work only needs:
- `workloads.tpch` (already fully specified above)
- `systems.PostgreSQL` and `systems.PgDuckDB` (already fully specified,
  including the `pg-guc`/`env-var` split)
- the `pg-guc` and `env-var` resolver branches — not `flag-equals`,
  `command-string`, `helm-values`, `pool_component`, or `topology`, all of
  which are needed by other systems but not this pair.

Everything else in the complete catalog above exists to confirm the schema
generalizes, not because it's in scope to implement now.

**Implemented so far:**
- `contracts/contract_catalog.yml` — the TPC-H/PostgreSQL/PgDuckDB-only
  slice of the catalog above; promoted out of `dev/catalog/` to
  `contracts/` once it graduated from prototype to the real input contract
  `bexhoma/spec.py` consumes.
- `dev/catalog/experiment.yml` — a sample experiment spec against it (still
  under `dev/`, since it's an example, not schema).
- `bexhoma/spec.py` — the Phase 1 translator: loads both files, resolves
  `extends`/profile/`derive:`/`override`, validates workload↔system support
  and post-load legality/capability/selection, and emits a `tpch.py`
  argument vector (`build_argv()`) or a copy-pasteable command line
  (`build_command()`). `build_argv()` only produces the CLI arguments a human
  would otherwise type by hand, and is genuinely wired into a real invocation
  path: `experiment.py`'s catalog-driven dispatch calls it and hands the
  result straight to `tpch.run()` in-process (see
  `RunExperimentYamlDispatchTest` in `tests/test_experiment_cli.py`).
  Per-system `post_load` selection is the one exception to "no entry script
  logic is modified": `resolve_indexing_key()`/`resolve_physical_design_overrides()`
  feed `tpch.py::run()`'s small `physical_design_overrides` hook (see
  "Per-system post_load selection" above) — the only change this catalog work
  has made to `tpch.py` or `bexhoma/benchmarks/tpch.py` itself, and it adds no
  CLI flag.
- `validate_experiment.py` — a dry-run CLI wrapping the same `build_argv()`
  plus `validate_environment()`, without touching a live cluster.
- `dev/spec_prototype_demo.py` — runs the translation end-to-end and parses
  the result through a parser mirroring `tpch.py`'s own, without needing a
  live cluster.

`contracts/contract_catalog.yml` and `contracts/contract_result.yml` live at
the repo root under `contracts/` — they're the active, consumed contracts,
not exploratory material. The sample `experiment.yml` and the generated
`environment.yml` stay under `dev/catalog/`: one is a worked example, the
other a per-cluster snapshot, neither is schema.

## Open questions

- Exact validation/schema ownership is called out in issue #764 as
  belonging to a separate milestone (M5) — this page assumes resolved
  catalog output is validated before `prepare_testbed()`, not what that
  schema looks like.
- Whether `-ms`/cluster-wide concurrency cap belongs in `environment.yml`
  (cluster capacity) with a per-experiment override, or purely in
  `experiment.yaml`, isn't settled.
- Single-file vs. split-file catalog layout may need revisiting once real
  DBMS variant count makes one file unwieldy to hand-edit — at ~19 systems
  already enumerated here, this is closer than it looked initially.
- `flag-equals`/`command-string` systems (MySQL, MariaDB, Redis,
  CockroachDB, TiDB, Dragonfly) need a real patch-mechanism decision before
  their `knobs:` are anything more than documentation — either extend
  `ensure_arg_pairs()` to understand more argument shapes, add a
  `command:`-block patcher, or accept these systems are catalog-documented
  but not catalog-configurable until that work happens.
- `pool_component` and `topology` are sketched from one example each
  (PGBouncer; Citus/CockroachDB/TiDB) — untested against a second case, so
  the shape may still be wrong in a way only a second real system would
  reveal.
- `tools.hardware`'s shape is a first pass — it wasn't cross-checked against
  a second non-DBMS tool (there isn't one yet), so it's the least-verified
  section here.
