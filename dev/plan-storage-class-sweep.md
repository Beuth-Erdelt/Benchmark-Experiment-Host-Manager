# Plan: `resources.storage_class` as a sweep list

Status: **implemented** (2026-10-10, branch `feature/storage-class-sweep`):
M0, M0b, M1–M5. Catalog contract 1.11.0, result contract 1.10.0. Not yet
run against the cluster. Deviations from the sketch below: the handbook got
no new guideline (M4.1/M4.2 already cover storage regimes); the result side
records `storage_reused` per connection and a validity test
`Loading measured in this experiment` instead of a `known_gaps` entry.

## Goal

One TPC-H experiment compares storage backends for one system. On the
reference cluster that is PostgreSQL on `cephcsi` (Ceph RBD block), `shared`
(CephFS) and ephemeral node-local disk: the only classes the cluster config
declares, and the only ones `environment.yml` marks `usable` (done
2026-10-10, catalog 1.11.0 / environment 1.3.0; `ceph` and `cephxfs` use
Rook's legacy FlexVolume provisioner, `local-hdd` is not for SUT volumes).
The agent declares the factor, the validator checks it, Bexhoma runs one SUT
configuration per backend, and `assess_comparison_quality` ranks the backends
deterministically. This is the smaller alternative named in
`dev/plan-studies.md`, open decision 2.

## What exists today

- **Contract:** `resources.storage_class` is a single `str`
  (`contracts/contract_catalog.yml`, `resources.storage_class`). Only
  `resources.cpu` and `resources.memory` take a list. `discriminates` allows
  `[system, concurrency, cpu, memory]`.
- **Sweep mechanics:** cpu and memory are paired by position, not crossed. A
  single entry is broadcast to every cell, and lists longer than one must share
  one length. This is implemented three times, and all three must stay in step:
  - `tpch.py::_resource_cells` (the CLI side);
  - `bexhoma/experiments/tpch_catalog.py::build_tpch_argv` (`-rc/-lc/-rr/-lr`
    comma lists, configuration names `{system}-{cell}`);
  - `agent/harness/validation.py::resolved_configurations` and
    `agent/harness/tools.py::_resource_dimensions`.
- **Storage is experiment-wide in Bexhoma.**
  `ExperimentBase.prepare_testbed` validates `args.request_storage_type`
  against `cluster.get_available_storage_types()` and calls
  `self.set_storage(storageClassName=...)` once
  (`bexhoma/experiments/base.py:527-533, 607-611`). Each configuration copies
  the experiment storage at init (`configurations/base.py:126`), and
  `SutConfiguration.set_storage` merges, so a per-configuration override is
  already possible.
- **PVC identity is the name, not the class.** The PVC is named from
  `storage_label` + `storageConfiguration` (`configurations/lifecycle.py:642-649`).
  `get_labels_from_loaded_pvc` (`lifecycle.py:575-595`) reuses an existing PVC
  with that name and its `loaded` labels, without checking its storage class.
  In `tpch.py` a resource cell already gets its own `storageConfiguration`
  (`postgresql-{cell}`), but the name says nothing about the class.

### Bug found while planning (fix first, M0)

`build_tpch_argv` emits `-rst` only from `ResolvedSystem.storage_class`
(`tpch_catalog.py:296-300`). `spec.resolve_system` sets that field only when the
profile declares `requires.storage_class` (`spec.py:410-422`). An experiment
with `storage_class: ceph` and no such profile therefore **runs on ephemeral
storage**, with no error. `ycsb_catalog.py:180` emits `-rst` straight from
`resources` and is not affected. No test in `tests/test_tpch_catalog*.py`
covers `-rst`.

### Gap found while planning: volume reuse is invisible (fix second, M0b)

- **Bexhoma side:** `-rsr`/`--request-storage-remove` deletes an existing
  PVC before the run (`cli_args.py:150`; used in `lifecycle.py:560, 821, 835,
  980`). Without it, `get_labels_from_loaded_pvc` finds the existing PVC and
  copies its `loaded`, `time_loading`, `time_schema`, `time_index`, ...
  labels onto the new SUT pod, labelled `storage_exists=True`
  (`lifecycle.py:575-599`). Loading is then skipped, and the loading times
  come from whichever run filled the volume.
- **Contract side:** `contract_catalog.yml` has no field for it, and neither
  `tpch_catalog.py` nor `ycsb_catalog.py` emits `-rsr`, so an agent cannot ask
  for a fresh volume. `contract_result.yml` says nothing about a reused
  volume; only `evaluators/ycsb.py:1100-1102` skips its loading-throughput
  test when loading was deactivated.

## Decisions

1. **Factor name `storage_class`**, mirroring `resources.storage_class` the way
   `cpu` and `memory` mirror their fields. It is added to `discriminates`.
2. **Same sweep rule as cpu and memory:** `resources.storage_class` may be a
   string, `null`/absent, or a list. Lists are paired by position with the cpu
   and memory lists; a single entry is broadcast; lists longer than one share
   one length. No crossing. A design that wants storage × memory enumerates
   the combinations, as today for cpu × memory.
3. **`null` is a legal list entry** and means ephemeral node-local storage, as
   for the scalar today and as in `requires.storage_class`.
4. **Entries must be distinct** when `storage_class` is the only varying
   resource. Duplicates with other dimensions varying are allowed (same as
   cpu/memory).
5. **`storage_class` is categorical.** The assessor ranks its levels at each
   fixed context, like `system`, and never builds an ordered sweep over it.
6. **PVC identity includes the class.** When the storage class varies across
   cells, each cell's `storageConfiguration` gets the class as a suffix
   (`postgresql-{cell}-{class}`), so a PVC loaded on one backend is never
   reused for another, in this run or a later one.
7. **`resources.storage.size` stays one shared value.** It is the PVC size, or
   the node-local request for `null` cells.
8. **Fresh volumes are a contract choice.** `resources.storage.remove_existing`
   (bool) maps to `-rsr`. Default `true` whenever `storage_class` is set, so
   an agent run measures its own loading; `false` is deliberate reuse to save
   loading time. When `storage_class` is a declared factor, `false` is
   refused, because loading on each backend is part of the comparison.
9. **Reuse is visible in the result.** Each configuration records whether it
   loaded or found an existing volume. Inherited loading times are reported
   as not measured in this run.
10. **TPC-H only in this increment.** YCSB keeps a scalar: `ycsb_catalog.py`
   rejects a list with a clear `SpecError`, and its catalog entry says so in
   `out_of_scope`. `tpch_builder.py` (the separate phase-1 YAML path) is out
   of scope.

## Implementation sketch

Each milestone ships with its tests and leaves the pipeline working.

### M0 — emit `-rst` for every TPC-H experiment

- `tpch_catalog.py::build_tpch_argv`: emit `-rst` from
  `resources.storage_class`, like `ycsb_catalog.py`. Keep the
  `requires` check in `resolve_system` as a precondition only.
- Tests: `storage_class: ceph` without a profile emits `-rst ceph`; unset emits
  no `-rst`; `analytical-ssd` with `ssd` still emits it.
- Ship this on its own; it changes what existing specs do.

### M0b — fresh volumes and visible reuse

Independent of the sweep; applies to every experiment with persistent storage,
TPC-H and YCSB.

- **Catalog:** `resources.storage.remove_existing: {type: bool}`, semantics
  "delete any existing PVC of this experiment's SUT configurations before
  loading, so data is loaded into a fresh volume"; default `true` when
  `storage_class` is set, ignored for ephemeral storage. `why:` loading
  times are only measured when loading runs. Minor version bump, comments
  entry, `docs/AgentCatalogContract.md`.
- **Translators:** `tpch_catalog.py` and `ycsb_catalog.py` emit `-rsr` when
  the effective value is `true` and `storage_class` is set.
- **Agent validation:** refuse `remove_existing: false` when
  `storage_class` is in `discriminates` (decision 8).
- **Result side:**
  - Check what reaches the result folder today: whether `storage_exists` and
    the copied `time_*` labels are in `connections.config` or only on the
    pod, and what the TPC-H report shows for a reused volume.
  - Surface per configuration `storage_reused: bool` in tier 1/2 (connections
    page), and mark loading times of a reused volume as inherited.
  - `contract_result.yml`: document the field; add a validity check (or a
    `known_gaps` entry until it exists) that a configuration with a reused
    volume has no loading measurement of its own. `docs/AgentResultContract.md`.
- **Assessor:** loading metrics of a reused configuration enter no
  comparison; say so in the assessment rather than dropping them silently.
- **Tests:** default emits `-rsr`; explicit `false` omits it; ephemeral never
  emits it; a factor with `false` is refused; a reused-volume fixture is
  reported as reused and its loading excluded.

### M1 — CLI: `-rst` as a comma list in `tpch.py`

- `tpch.py::_resource_cells`: add `storage_class` as a fifth dimension, read
  from `experiment.get_parameter_as_list_str('request_storage_type')`. An
  empty token means ephemeral (`None`). The same length rule applies.
- `prepare_testbed` (`experiments/base.py`): validate **each** listed class
  against `get_available_storage_types()`. Keep the experiment-wide
  `set_storage` for the first (or only) value so non-sweep callers are
  unchanged. Write the workload info line per class when there are several.
- Cell loop in `tpch.py` (PostgreSQL branch, lines 299-363, and every other
  branch that iterates `resource_cells`): call
  `config.set_storage(storageClassName=cell['storage_class'], storageConfiguration=...)`
  with the class suffix from decision 6 when the class varies.
- No change needed below the CLI (checked 2026-10-10): every storage
  decision reads the per-configuration `cfg.storage` — `use_storage`/
  `use_ramdisk` (`configurations/base.py:1062-1093`), the PVC manifest
  (`lifecycle.py:809-815`), statefulset volume claims (1013-1020), ephemeral
  size (913/1308), PVC labelling in `loading.py` and PVC deletion (1378-1390).
  `hardware_baseline.py:401-437` already runs ephemeral and `cephcsi`
  configurations side by side in one experiment. Only
  `request_storage_remove` stays experiment-wide, which is fine.
- Tests: `_resource_cells` with a storage list; length mismatch raises; a
  sweep builds one configuration per class with distinct
  `storageConfiguration` and the right `storageClassName`; an empty token
  gives an ephemeral configuration.

### M2 — catalog contract and resolver

- `contracts/contract_catalog.yml`:
  - `resources.storage_class`: type `"str or null or list[str or null]"`,
    `when:` the same sweep rule as cpu, `out_of_scope:` lists of different
    lengths; YCSB accepts only a scalar.
  - `experiment_schema.discriminates.values`: add `storage_class`.
  - `catalog_concepts.derive`: `storage_class` is per cell.
  - `catalog_concepts.requires`: checked per cell; one disallowed cell fails
    the whole spec.
  - Minor version bump; entry in `contracts/contract_catalog_comments.md`;
    `docs/AgentCatalogContract.md`.
  - Keep the entries short: the catalog is close to the agent's read limit
    (see `dev/plan-studies.md`, M6).
- `bexhoma/spec.py`:
  - `validate_experiment`: shape check (scalar, null or list of them).
  - `validate_environment`: check every non-null entry against
    `usable_storage_classes(environment)`.
- `tpch_catalog.py::build_tpch_argv`:
  - include storage in `num_cells` and the length check;
  - pass the cell's class to `resolve_system` (so `requires` and `derive`
    see the cell value);
  - emit `-rst` as a comma list (empty token for `null`) when it varies;
  - drop the "conflicting storage classes" `SpecError`, which a sweep makes
    legitimate.
- `ycsb_catalog.py`: reject a list.
- Tests: argv for a two-class sweep, broadcast with a memory sweep, a `null`
  entry, `requires` failing for one cell, environment rejection naming the
  unknown class, YCSB rejection.

### M3 — agent validation

- `agent/harness/validation.py`:
  - `_check_storage_class`: check each entry against
    `spec.usable_storage_classes`, keep the message that lists them.
  - `_check_declared_factors`: a list with more than one distinct entry adds
    `storage_class` to `varied`; extend the "nothing to isolate" hint.
  - `resolved_configurations` / `_describe_configuration`: add the
    `storage_class` dimension.
  - `_check_factor_attribution`: include `storage_class` with cpu and memory,
    so storage that only ever moves together with memory is refused.
  - `_expansion` and the run/duration estimate: count storage cells.
- Tests in `tests/test_agent_harness.py`: declared/varied mismatch both ways,
  lockstep storage + memory refused, estimate counts the cells, unknown class
  in a list named.

### M4 — comparison assessor

- `agent/harness/tools.py`:
  - `_DISCRIMINATING_FACTORS`: add `storage_class`.
  - `_resource_dimensions`: carry the cell's storage class as a string level
    (`"ephemeral"` for `null`), alongside the numeric cpu/memory values.
  - `_categorical_claims`: generalise from the hard-coded `"system"` to a
    categorical factor argument; call it for `system` and for
    `storage_class`. The expected level set for storage is the distinct
    entries of the list.
  - `_ordered_sweep_claims` / `_expected_levels`: never build an ordered sweep
    for `storage_class`; `_FACTOR_UNITS` gets no entry.
  - `_configuration_cell` already decodes `{system}-{cell}`; verify it is
    unaffected by the storage suffix, which lives in `storageConfiguration`,
    not in the configuration name.
- Tests in `tests/test_agent_harness.py` and
  `tests/test_harness_partial_results.py`: ranking of two backends at a fixed
  context, `system × storage_class` gives one ranking per factor per context,
  a missing backend leaves the factor unsupported.

### M5 — report and prompts

- The report must show which configuration ran on which class. Check what
  `report_writer.py` and the workload info line expose; if the class is only
  in the archived `experiment.yml`, add it to the per-configuration overview.
- `agent/harness/prompts.py` and the handbook: one line that storage backends
  are compared with a `storage_class` list, that loading time is part of what
  differs, and that `observe.metrics` should name the disk I/O metrics the
  hypothesis relies on.
- `agent/ARCHITECTURE.md` (factor list in the interpretation assessor
  paragraph), `agent/README.md`, `docs/AgentHarness.md`.

## Risks and open points

- **Stale PVCs from older runs.** Decision 6 protects runs after this change.
  A PVC named `…-postgresql-1` created earlier on another class is no longer
  matched once the suffix applies; it is not deleted either, since
  `remove_existing` only removes the names the current run uses. Document
  manual cleanup.
- **Cost of the new default.** `remove_existing: true` makes every run with
  persistent storage reload its data, which is slow at large scaling factors.
  This is deliberate for agent runs; operators who want reuse set `false` and
  get a result that says the loading was inherited.
- **Placement.** Network storage (`cephcsi`, `shared`) does not bind to a
  node, but ephemeral cells use the scheduled node's own disk, so cells may
  differ by node as well as by backend. Consider a methodology warning when
  `storage_class` is declared and `placement.sut` is unset. (Static
  `WaitForFirstConsumer` classes like `local-hdd`, and their reclaim
  behaviour under `remove_existing`, are out of scope while they are not
  usable.)
- **Profiles with `requires`**, such as `analytical-ssd` (`[ssd, null]`),
  reject most sweeps by design. Profile knobs like `random_page_cost` are
  tuned per backend, so a sweep under one fixed profile tests "profile X on
  each backend", not "best setup per backend". The hypothesis has to say
  which.
- **Loading time differs by backend.** That is part of the effect, but the
  report and the assessor treat loading and benchmarking separately; check
  that the ranking uses the benchmarking phase, as for cpu/memory.
