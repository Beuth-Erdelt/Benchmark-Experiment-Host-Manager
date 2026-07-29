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
first implementation — see `docs/Design-Catalog-Contract.md` for the full
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

## PgDuckDB's orphaned experiments directory (implementation detail)

`experiments/tpch/PgDuckDB/` exists on disk but is unused: `tpch.py` points
`PgDuckDB` at `experiments/tpch/PostgreSQL/` instead (DDL reuse, formalized
in the catalog via PgDuckDB's `extends: PostgreSQL`). Not relevant to
building a valid `experiment.yml` — noted here only so nobody "fixes" the
orphaned directory by wiring it back in without knowing why it was unused.

## See also

- `docs/Design-Catalog-Contract.md` — full design rationale, the
  all-workload/all-system breadth pass this contract was trimmed from, and
  open questions.
- `contracts/contract_catalog.yml` — the actual contract.
- `contracts/contract_result.yml` — what a completed run's result folder
  contains.
