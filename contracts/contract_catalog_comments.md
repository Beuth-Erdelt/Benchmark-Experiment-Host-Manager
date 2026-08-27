# contract_catalog.yml — design rationale and provenance

This file is **not** required to build a valid `experiment.yml`.
`contracts/contract_catalog.yml` is fully self-contained on its own: every
field an agent needs — including the full `experiment.yml` top-level shape
and the `resources:` quantity format — is encoded as actual parseable YAML
data in that file (its `catalog_concepts:` and `experiment_schema:` keys),
not as comments. Nothing in `contract_catalog.yml` should ever require
reading this document, or any other file, to construct or hand-check a
valid `experiment.yml` against it — the only other files an agent needs are
`environment.yml` (cluster-specific facts: which nodes/storage classes
actually exist) and `contract_result.yml` (what a completed run's result
folder contains).

This document exists purely for human maintainers: the *why* behind the
choices baked into the contract, its provenance, and pointers to the wider
design history that produced it.

## Status and provenance

`contracts/contract_catalog.yml` is active and consumed by `bexhoma/spec.py`
(`validate_experiment()`, `build_argv()`), `validate_experiment.py`, and
`experiment.py`'s catalog-driven dispatch. It was promoted out of `dev/`
once it graduated from exploratory prototype to the real input contract
those consume.

Its scope is narrowed to the TPC-H/PostgreSQL/PgDuckDB slice chosen for the
first implementation, plus a basic YCSB/PostgreSQL workload (see below) —
see `docs/Design-Catalog-Contract.md` for the full
design rationale, the complete (all-workload, all-system) breadth pass this
was extracted from, and open questions.

## Two catalog concepts kept intentionally separate

- `workloads:` — what to run (params, loading behavior, physical-design
  semantics)
- `systems:` — what to run it on (server knobs, physical-design support,
  profiles)

## `derive:` expression language

Deliberately minimal: arithmetic over exactly `{memory_limit, cpu_limit,
storage_class, scaling_factor}` — no functions, no conditionals. A
profile's `knobs:` are literal values an expert chose; `derive:` is only
for the handful of quantities that should scale with an experiment's own
resource limits. Richer than plain arithmetic and the catalog stops being
writable by the people who hold the tuning knowledge; forcing every knob
into a formula would invent false precision most of them never had.

## `physical_design:` — capability, not selection

A system's `physical_design:` block says which post_load-style options
(`indexes`/`constraints`/`statistics`/`storage_format`) that system CAN
support at all. Being capable of an option is necessary but not sufficient
for actually receiving it in a given run — that's a separate,
per-experiment *selection* choice made via `loading.post_load` /
`systems[].post_load` in `experiment.yml`. PgDuckDB's `physical_design` is
fully capable of all three, and an experiment can still choose not to apply
them there.

## Storage class mechanics (implementation detail)

`resources.storage_class` maps, underneath bexhoma, to
`bexhoma/clusters.py::Kubernetes.get_available_storage_types()` and the
`-rst`/`--request-storage-type` CLI flag. `None`/`''` (ephemeral) and
`'ramdisk'` (in-memory) are always valid regardless of cluster; any other
value must be one of the cluster's actual declared storage classes
(`environment.yml`'s `storage_classes:`).

Note: `catalog_concepts.extends`/`.profile_ref`/`.requires`/`.arg_style`/
`.knob_status` in `contract_catalog.yml` cover the mechanics above (and a
few more: `extends:`/`ref:` merge semantics, `arg_style` GUC-vs-env-var
dispatch, `status: reference-only` vs. `fixed: true` on a knob) as actual
data now, not just this prose — keep both in sync if either changes.

## TPC-H params trimmed from the catalog (2026-08-01)

Three `workloads.TPCH.params` entries were removed as exposed options:

- `verbose_explain` — dropped entirely. It only prints EXPLAIN output for
  interactive debugging; `store_explain` (which persists EXPLAIN into the
  protocol) covers the real use case, so there's no reason to expose the
  print-only variant as a catalog option.
- `verify_result` — dropped as an option because it should always be `true`.
  Result-row sanity checking is not something an experiment should be able
  to opt out of.
- `limit_import_table` — dropped; the partial-reload use case it served
  isn't needed for this contract's scope.

None of these were removed from the underlying bexhoma code (`tpch.py`,
`bexhoma/spec.py`, `bexhoma/benchmarks/tpch.py` still reference them) — only
from the catalog's exposed surface. If the code paths for these are later
found unused elsewhere, that's a separate cleanup, not implied by this one.

## Single SUT at a time by default (2026-08-26)

`catalog_concepts.sut_isolation` and two `experiment_schema` fields
(`max_sut`, `max_sut_experiment`, both `default: 1`) were added
(`catalog_contract_version` 1.0.0 -> 1.1.0, `spec.CATALOG_CONTRACT_VERSION`
kept in lockstep). The `-ms`/`-mse` CLI defaults are **unchanged** (still
`None` = no limit) — this is purely a catalog-contract addition.

Rationale: the default benchmarking situation is one system-under-test at a
time. A `systems:` list (and any `resources:` sweep crossed with it)
resolves to several configurations, and nothing stops bexhoma from bringing
two of their SUTs up concurrently on the same cluster. Co-located SUTs share
node CPU, memory bandwidth, disk and network, so a side-by-side run measures
that interference instead of the factor in `discriminates:`. A cap of 1
keeps every measurement attributable to a single configuration.

Design points:

- **The default lives in the contract, not the CLI.** `tpch.py`'s own
  `-ms`/`-mse` argparse defaults stay `None` (no limit); a bare
  `python tpch.py ...` is unaffected. The serial default applies only to
  catalog-driven runs: `build_tpch_argv()` reads `experiment.get(field, 1)`
  and always emits `-ms N` / `-mse N`, so an experiment.yml that omits the
  fields still gets `-ms 1 -mse 1` on the generated command.
- **Two independent caps, kept independent.** `-ms` counts SUTs
  cluster-wide (across every concurrent bexhoma experiment); `-mse` counts
  only the current experiment's own. `bexhoma/experiments/base.py` enforces
  both — a new SUT starts only if both allow it — so they compose without
  either subsuming the other.
- **`0` means "no limit".** In the YAML, `max_sut: 0` makes
  `build_tpch_argv()` *omit* the `-ms` flag, so `tpch.py` falls back to its
  own no-limit default. (`-ms 0` is never emitted — the entry scripts'
  `int(args.max_sut)` would read a literal 0 as "cap at zero".)
  `validate_experiment()` still requires a non-negative integer.

## Basic YCSB workload added (2026-08-27)

`workloads.ycsb` was added (`catalog_contract_version` 1.1.0 -> 1.2.0,
`spec.CATALOG_CONTRACT_VERSION` kept in lockstep). Like `workloads.tpch`, it
is deliberately trimmed to the prototype slice: `supports: [PostgreSQL]` only.

Scope decisions:

- **PostgreSQL only.** The full `ycsb.py` supports a dozen engines (MySQL,
  MariaDB, YugabyteDB, CockroachDB, TiDB, DatabaseService, PGBouncer, Redis,
  Citus, CedarDB, Dragonfly); all are listed under `out_of_scope.systems`.
  Connection pooling (PGBouncer's `-xnpp/-xnpi/-xnpo`) and the per-system
  knobs (`-xnsr` SUT replicas, `-xnpd` TiDB PD nodes) only matter for those
  engines, so they are left out of the catalog block entirely rather than
  documented as unused.
- **No `post_load` / `physical_design` for this workload.** YCSB creates and
  manages its own schema (one `usertable` + primary key) through the JDBC
  binding — there is no indexes/constraints/statistics/storage_format
  selection to make. `loading.out_of_scope` states this explicitly.
- **`params` mirror `ycsb.py`'s `-x*` flags**, renamed to catalog vocabulary:
  `workload` (`-xwl`), `scaling_factor` (`-sf`, rows = SF·1e6),
  `operations_scale` (`-xop`, millions), `target_base` (`-xtb`),
  `loading_target_factors` (`-xnlf`), `benchmarking_target_factors`
  (`-xnbf`), `batchsize` (`-xsbs`), `logging_interval` (`-xli`, seconds),
  `insert_order` (`-xio`), `max_execution_time` (`-xmet`).
- **`produces` grounded in `YcsbEvaluator`**: `per_operation` (one row per
  op type), whole-workload `summary`, and a `time_series` (per-interval
  `current_ops_per_sec`, both phases) — the running signal DBMSBenchmarker
  workloads can't produce. No `per_query` — YCSB has no query concept.

Not added: an argv builder. `bexhoma/spec.py::build_argv()` still dispatches
only `tpch`; a catalog-driven `ycsb` experiment validates against the
catalog but `build_argv()` / `bexhoma.experiments.tpch_loader` still reject
it as not-yet-translatable (see `test_experiment_loader.py`). Wiring a
`ycsb` argv builder is separate follow-up work.

## PgDuckDB's orphaned experiments directory (implementation detail)

`experiments/tpch/PgDuckDB/` exists on disk but is unused: `tpch.py` points
`PgDuckDB` at `experiments/tpch/PostgreSQL/` instead (DDL reuse, formalized
in the catalog via PgDuckDB's `extends: PostgreSQL`). Not relevant to
building a valid `experiment.yml` — noted here only so nobody "fixes" the
orphaned directory by wiring it back in without knowing why it was unused.

## See also

- `docs/AgentWorkflow.md` — the end-to-end agent loop this file is the
  input half of: question → contracts → `experiment.yml` → validate → run →
  answer.
- `docs/AgentCatalogContract.md` — prose/condensed-YAML version of this
  file's shape, worked example, and known gaps — the input-side counterpart
  to `docs/AgentResultContract.md`.
- `docs/Design-Catalog-Contract.md` — full design rationale, the
  all-workload/all-system breadth pass this contract was trimmed from, and
  open questions.
- `contracts/contract_catalog.yml` — the actual contract.
- `contracts/contract_result.yml` — what a completed run's result folder
  contains.
