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

## `observe:` — what is measured, and when it is worth it (2026-09-24)

The three monitoring switches used to carry a one-line `semantics:` each and
no `when:`, which hid three facts. First, the whole block only matters when
the hypothesis needs hardware metrics (CPU, memory, GPU) or database-internal
statistics, so that is now the block's `when:`, together with the warm-up
note that used to be labelled `why:` although it describes when readings can
be trusted. Second, `monitoring_app` was described as benchmarker/loader
metrics, but bexhoma actually attaches the database's own metrics exporter to
the SUT; and it only takes effect when `monitoring_sut` or
`monitoring_cluster` is also on, because bexhoma sets up no monitoring at all
otherwise. Third, `monitoring_cluster` replaces rather than adds to the
per-experiment collection, so turning on both equals cluster monitoring
alone.

The new wording deliberately says what is measured, not how it is collected.
An earlier draft described SUT monitoring as sidecar containers, which is no
longer how bexhoma collects it; naming the mechanism is what makes such text
go stale. "Hardware metrics" deliberately omits disk and network, because
the metric collector bexhoma deploys is configured to skip both.

The block moved the version 1.5.1 -> 1.6.0 (minor: meaning of existing
fields corrected and conditions added; nothing that validated before is
rejected now), with `spec.CATALOG_CONTRACT_VERSION` kept in lockstep.

## Pinning loader and benchmarker pods is uncommon (2026-09-25)

`placement.loading` and `placement.benchmarking` used to carry only a
one-line `semantics:`, so nothing told an agent whether pinning them was
normal. Design runs pinned them routinely, which adds a node choice to every
experiment without a reason in the hypothesis and can crowd many client pods
onto one node (see the YCSB `benchmarking:` section below for a run that
stalled that way). Both fields now carry a `when:` saying that pinning is
uncommon and only recommended when the network path between the client pods
and the SUT might play a role, in which case the network belongs in
`discriminates`. `placement.sut` is unchanged, because the node the SUT runs
on is a genuine factor on a heterogeneous cluster.

This moved the version 1.6.0 -> 1.6.1 (patch: guidance only; nothing that
validated before is rejected now), with `spec.CATALOG_CONTRACT_VERSION` kept
in lockstep.

## TPC-H loading timeout recommendation (2026-09-24)

`catalog_concepts.experimental_design.bounded_loading` tells an agent to set
`loading.timeout_minutes` but deliberately gives no universal value, and until
now nothing said what value suits TPC-H. `workloads.tpch.loading.timeout_minutes`
now recommends 10 minutes per unit of scaling factor. The rule is a
maintainer's rule of thumb and is advisory only: validation does not compare
the timeout against the scaling factor. The entry repeats the schema field's
`type: int`, `min: 1` and `required: false`, because the agent validator
merges the workload's loading block over the schema's and lets the workload
entry win. Without those keys the TPC-H entry would silently switch off the
integer and minimum checks.

Together with the `engine:` description below, this moved the version
1.5.0 -> 1.5.1, with `spec.CATALOG_CONTRACT_VERSION` kept in lockstep. Neither
change alters what validates, but a new version makes any agent or cache keyed
on the version string re-read the catalog.

## `engine:` — description, not option (2026-09-24)

Each system may carry an `engine:` block (`execution`, `data_layout`) that
describes in plain words how it runs queries and stores data — for
example, that PgDuckDB executes vectorized and ignores PostgreSQL indexes
while still reading the same heap tables. It exists so that whoever
interprets a result can explain a difference between systems, not so that
an experiment can choose anything. Unlike `physical_design:`, which states a
capability that `post_load` then selects from, `engine:` has no selection
counterpart at all.

Consequently it plays no part in validation or resolution. `bexhoma/spec.py`
never reads it, and it does not reach the generated command line. On the
`experiment.yml` side, the `systems[]` item fields are only `name`,
`profile`, `override` and `post_load`, so an entry that sets `engine:` is
rejected as an unknown field by the agent's validator. Because `engine:` is
not one of the keys `extends:` merges, a system that extends another falls
back to the base's description unless it declares its own — PgDuckDB does.

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

End-to-end wiring (2026-08-27, same change): a catalog-driven `ycsb`
experiment.yml now runs, not just validates.

- `bexhoma/experiments/ycsb_catalog.py::build_ycsb_argv()` translates the
  spec into a `ycsb.py` argv; `bexhoma/spec.py::build_argv()` dispatches
  `workload.name == "ycsb"` to it (alongside the existing `tpch` branch).
- `ycsb.py` gained `build_parser()` + `run(args, on_experiment_built=...)`,
  extracted from its `if __name__ == '__main__'` block exactly like
  `tpch.py` — a plain `python ycsb.py ...` invocation is unchanged.
- `experiment.py`'s catalog-driven branch dispatches by workload name
  (`_ENTRY_MODULE_BY_WORKLOAD`): `tpch` -> `tpch.run`, `ycsb` -> `ycsb.run`.
- No resource sweep and no per-system post_load for `ycsb`: `resources.cpu`
  / `resources.memory` must each be a single `{request, limit}` dict, and
  `build_ycsb_argv()` raises on a list. YCSB manages its own schema, so
  there is no `-xii/-xic/-xis`-style physical-design step.
- `ycsb.py` only constrains the PostgreSQL SUT pod's CPU/memory when the
  catalog run opts in (`args.apply_sut_resources`, set by `experiment.py`
  when the experiment.yml has a `resources:` block) — a plain CLI run still
  leaves the SUT pod unconstrained.

Still `tpch`-only: `bexhoma.experiments.tpch_loader` (the *self-specified*
YAML path, `workload: ycsb` as a bare string), which is unrelated to the
catalog path.

## `loading.split` removed from the catalog surface (2026-08-30)

The `loading.split` field was removed from both `experiment_schema` and
`workloads.tpch.loading` (`catalog_contract_version` 1.2.0 -> 1.3.0,
`spec.CATALOG_CONTRACT_VERSION` kept in lockstep), and
`bexhoma/experiments/tpch_catalog.py::build_tpch_argv()` no longer emits the
`-xnls` flag it drove.

Rationale: `split` set `-xnls`, which `tpch.py` divides the total loader-pod
count by to decide how many pods run at once (`PODS_PARALLEL = pods //
split`). Any value above 1 therefore makes the Kubernetes loading job run its
pods in sequential waves. But `tpch.py` also hard-codes `BEXHOMA_SYNCH_LOAD=1`
and `BEXHOMA_SYNCH_GENERATE=1`, and the synchronized loader barrier waits for
*every* loader pod to check in before any of them proceeds. Sequential waves
plus an all-pods barrier is a deadlock: the first wave blocks on the barrier,
the later waves are never scheduled, and the run sits until
`loading.timeout_minutes` expires and tears everything down. A design run hit
exactly this on 2026-08-29 (`pods: 2, split: 2`).

Since synchronized loading can only ever use `split: 1`, the field could not
express anything valid and is gone from the contract. A spec that still
carries `loading.split` is now rejected by `validate_experiment()` as an
unknown field. This is a catalog-surface removal only: `tpch.py`'s `-xnls`
argument and `bexhoma/experiments/tpch_builder.py`'s `split` handling (the
separate self-specified-YAML path) are unchanged.

## Two-sentence `why:` fields in the TPC-H block (2026-08-31)

Every `why:` field under `workloads.tpch` was rewritten to a fixed two-part
shape: a first sentence that neutrally states what the field or value does,
then a second sentence that motivates when an experiment author would actually
set it — the trade-off it buys, the rival explanation it rules out, or the cost
it adds. For example, `post_load.constraints` now says both that it adds the
primary- and foreign-key constraints after loading and that you enable it when
the hypothesis depends on referential integrity or on the planner exploiting
guaranteed key uniqueness. Only descriptive prose in `why:` fields changed; no
field name, type, default, legal value, or `when:`/`out_of_scope:` text was
touched, and no code path reads these strings. `resource_profile.why` already
had this structure and was left as written.

The version moved 1.3.0 -> 1.4.0 with `spec.CATALOG_CONTRACT_VERSION` kept in
lockstep (required by `tests/test_naming_conformance.py`), even though the
contract shape did not change, so that any agent or cache keyed on the version
string re-reads the block.

## YCSB benchmarking-phase pods/threads split added (2026-09-12)

`workloads.ycsb` gained a `benchmarking:` block (`catalog_contract_version`
1.4.0 -> 1.5.0, `spec.CATALOG_CONTRACT_VERSION` kept in lockstep), mirroring
the pre-existing `loading:` block's `pods`/`threads` pair but for the
benchmarking phase, and `bexhoma/experiments/ycsb_catalog.py::build_ycsb_argv()`
now emits `-nbp`/`-nbt` from it.

Rationale: before this change, the only lever the catalog exposed for
benchmarking-phase concurrency was `rounds`, and each entry in that list
becomes one Kubernetes pod running the YCSB benchmarker with exactly one
thread (`ycsb.py`'s own `-nbp`/`-nbt` default to `1`, and neither was ever
wired into the catalog translator). An agent designing a concurrency sweep
had no way to ask for "128 concurrent clients" except `rounds: [128]`, i.e.
128 separate single-threaded pods. A design run on 2026-09-11 did exactly
that (`rounds: [64, 128]`, both pinned to one node via `placement.benchmarking`)
and stalled: Kubernetes nodes default to a 110-pod kubelet cap, so a chunk of
the 128 pods most likely sat `Pending` indefinitely, and the run had to be
killed by hand after an OIDC access-token refresh mid-poll (a known,
unrelated failure mode, see this repository's `CLAUDE.md` "Cluster access"
section) made the stall visible in the log.

`benchmarking.pods`/`benchmarking.threads` let an experiment reach a given
thread-level concurrency without multiplying pod count: `rounds: [1]` with
`benchmarking: {pods: 4, threads: 128}` runs 4 pods at 32 threads each, 128
total clients, instead of 128 pods. The two mechanisms are independent and
compose by multiplication rather than one replacing the other — `rounds`
still multiplies pod count on top of `benchmarking.pods`, and
`benchmarking.threads` splits only across `benchmarking.pods`, not across the
`rounds` multiplier — so a `rounds` sweep of more than one entry combined
with a non-default `benchmarking.threads` compounds concurrency; both
`contract_catalog.yml`'s `why:` text and `docs/AgentCatalogContract.md`
spell this out to head off that combination being set by accident. This is
purely a catalog-and-translator addition: `-nbp`/`-nbt` already existed on
`ycsb.py`'s CLI (via the shared `bexhoma/cli_args.py` base parser) and were
already read by `ycsb.py`'s own run loop; neither file needed a change.

## Three YCSB knobs that validated but silently did nothing, corrected (2026-09-12)

Reading `ycsb.py` end to end while investigating the incident above turned up
three places where `bexhoma/experiments/ycsb_catalog.py::build_ycsb_argv()`
either never translated a field the schema already accepted, or never gave
the workload a way to reach a real `ycsb.py` behavior at all. All three are
fixed in the same change as the `benchmarking:` block above.

- **`loading.timeout_minutes` reached the validator's timeout budget but not
  `ycsb.py`.** This field is generic (`experiment_schema.fields.loading`),
  and `agent/harness/validation.py`'s cost estimate already accounts for it
  for every workload. `bexhoma/experiments/tpch_catalog.py` translates it
  into `--loading-timeout`; `ycsb_catalog.py` never did, so a YCSB
  experiment declaring this field got a clean validation and a timeout
  figure in its budget that was never actually enforced against a stuck
  load. `build_ycsb_argv()` now emits `--loading-timeout` from it, exactly
  like the TPC-H builder.
- **The PostgreSQL reset script never ran.** `ycsb.py`'s PostgreSQL branch
  unconditionally calls `config.set_benchmark_resetscript(['reset-ycsb.sql'])`
  with a comment saying it runs CHECKPOINT + VACUUM ANALYZE before each
  benchmarking round "to produce a consistent, cold-cache starting state" —
  but that script only actually executes when `ycsb.py`'s shared `-ar`/
  `--activate-reset` flag is set (`bexhoma/experiments/base.py`'s
  `resetscript_active = args.activate_reset`), and no catalog path ever set
  it. Every catalog-driven YCSB run therefore skipped the reset regardless
  of what an experiment.yml said, letting table bloat and buffer-cache state
  carry over from one round or repetition into the next — a real confound
  for a workload whose entire point is comparing rounds. Unlike the other
  two fixes, this one is not exposed as a new `experiment.yml` field:
  `build_ycsb_argv()` now emits `-ar` unconditionally, because skipping the
  reset is never a valid experimental treatment, only a bug.
- **`-tr`/`--test-result` had no YCSB-side path to turn it on.** The
  underlying mechanism is workload-agnostic (`bexhoma/experiments/base.py`
  reads `self.args.test_result` directly), and `bexhoma/evaluators/ycsb.py`
  already implements `record_tests()` — non-zero loading/benchmarking
  throughput, the planned workflow actually ran, no `FAILED` operation
  column — so turning it on is meaningful, not a no-op. `tpch_catalog.py`
  gates its own `-tr` emission on a `params.verify_result` value, but that
  param was never added to `contract_catalog.yml`'s `workloads.tpch.params`,
  making it unreachable from the documented contract for TPC-H too (a
  pre-existing issue, left alone since fixing it wasn't asked for). YCSB
  gets its own, properly documented `params.verify_result` (`type: bool`,
  default `false`), and `build_ycsb_argv()` emits `-tr` when it is set.

No version bump beyond the 1.4.0 -> 1.5.0 move above: these three fixes and
the `benchmarking:` addition land together as one catalog-contract change.

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
