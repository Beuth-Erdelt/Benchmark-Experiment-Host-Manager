# Plan: remove the SUT volume before every repetition

Status: M1, M1b, M2, M3 implemented 2026-10-13 (not committed); M4 (cluster
run) open. Deviations from the text below: the contradiction
`remove_per_repetition: true` + `remove_existing: false` is refused in
`spec.validate_experiment()` (so the agent gets it too), not in
`agent/harness/validation.py`; no warning for `repetitions: 1`. Contract
versions: catalog 1.11.0 -> 1.12.0, result 1.10.0 -> 1.11.0 (both were
released in v0.11.3). `loading_inherited` is no pass/fail check: it is
documented under `validity.loading_measured_in_experiment.repetitions`, and
the summary prints an informational "Inherited Loading" block.

## Goal

`-rsr` / `--request-storage-remove` deletes an existing SUT PVC once, before
the first repetition. Repetitions 2..n (`-nc`) then reuse the volume: loading
is skipped and the loading labels of run 1 are copied. Add a second option
that deletes the PVC before **every** repetition, so each repetition loads into
a fresh volume and measures its own loading. The agent sees it in the
experiment.yml contract.

## How it works today

- The CLI always calls `set_storage(..., keep=True)`
  ([bexhoma/experiments/base.py:642](../bexhoma/experiments/base.py#L642)), so
  `stop_sut()` keeps the PVC between repetitions
  ([lifecycle.py:1393](../bexhoma/configurations/lifecycle.py#L1393)).
- Between repetitions, `base.py:2138-2151` runs `stop_sut()`, waits until the
  SUT is gone, `reset_sut()` (sets `loading_finished = False`), `start_sut()`.
- `start_sut()` deletes the PVC only if
  `not loading_finished and request_storage_remove and num_experiment_to_apply_done == 0`.
  This condition is copied four times in `lifecycle.py`:
  - `should_we_remove_pvcs()` (556) — also gates reading labels of a loaded PVC
  - the storage PVC (838-841)
  - per-tenant PVCs (852-855)
  - StatefulSet worker PVCs (996-999)
- In repetition 2+, `done > 0`, so the PVC survives; the deployment gets
  `storage_exists` labels and loading is skipped.

## Design

One new CLI flag, one new contract field. Deletion happens where `-rsr` already
deletes, at `start_sut()`, so the wait-until-gone loops and the worker/tenant
paths are reused unchanged. `stop_sut()` and `keep` are not changed: after the
last repetition the volume stays, as with `-rsr`.

### M1 — bexhoma core

1. **CLI** ([cli_args.py:259](../bexhoma/cli_args.py#L259)): add
   `-rsrp`, `--request-storage-remove-per-repetition`, `store_true`, help:
   "delete the SUT's PVC before every repetition (-nc), so each repetition
   loads into a fresh volume; implies -rsr". Add `-rsrp` to the flag order in
   [scripts/_reorder_flags.py:48](../scripts/_reorder_flags.py#L48) and the
   O-group row in `scripts/README.md`.
2. **One predicate** instead of four copies. Add to the configuration (e.g.
   `ConfigurationBase.removes_storage_now()` or a lifecycle helper):
   ```python
   args = cfg.experiment.args_dict
   if cfg.loading_finished:
       return False
   if args.get('request_storage_remove_per_repetition'):
       return True
   return args['request_storage_remove'] and cfg.num_experiment_to_apply_done == 0
   ```
   Use `.get()` for the new key: other entry scripts (TPCTC23, `example.py`,
   `dev/simple_tpch.py`) build their own parsers and won't have it.
   Replace lifecycle.py 556-559, 838-840, 852-854, 996-999 with this call.
3. **Fix while there**: `reset_and_remove_pvc()` checks
   `if should_we_remove_pvcs:` (the function object, always truthy) at
   [lifecycle.py:562](../bexhoma/configurations/lifecycle.py#L562). Its callers
   already check the condition, so this has no effect today, but it must call
   the predicate.
4. **`storage_reused`** ([lifecycle.py:615](../bexhoma/configurations/lifecycle.py#L615))
   is already False when no labels are copied. No change needed; add a test.
5. **Workload info** ([base.py:711-716](../bexhoma/experiments/base.py#L711-L716)):
   with the flag set, write "Persistent storage is removed before every
   repetition." instead of "... at experiment start." Read
   `args.request_storage_remove_per_repetition` next to
   `request_storage_remove` at base.py:570 (with `getattr(..., False)`).
6. **No-op cases**: no storage class / ramdisk → nothing to delete, same as
   `-rsr`. With `-nc 1` it does the same as `-rsr`.

### M2 — agent contract

1. **Catalog** ([contracts/contract_catalog.yml:376](../contracts/contract_catalog.yml#L376)),
   next to `remove_existing`:
   ```yaml
   remove_per_repetition:
     type: bool
     required: false
     semantics: "delete the volume before every repetition, not only before
       the first, so each repetition loads into a fresh volume. Default false;
       ignored without storage_class"
     why: "by default repetitions 2..n reuse the volume of repetition 1:
       loading is skipped and its loading times are copied, so loading
       variance and fresh-volume effects are measured only once"
     when: "the hypothesis is about loading, or benchmark results may depend
       on volume age or layout (fresh volume vs. reused). Costs one load per
       repetition: runtime grows by load time x (repetitions - 1)"
   ```
   Add a line to `contracts/contract_catalog_comments.md` (near line 174):
   `remove_per_repetition` maps to `-rsrp`.
2. **Spec** ([bexhoma/spec.py:518](../bexhoma/spec.py#L518)): validate it as
   bool like `remove_existing`. Add `removes_storage_per_repetition(resources)`
   next to `removes_existing_storage()` (707): True only when some cell has a
   storage class and the field is true. Export it in `__all__`.
3. **argv** ([tpch_catalog.py:225](../bexhoma/experiments/tpch_catalog.py#L225)):
   in `append_resource_flags()`, emit `-rsrp` when that returns True. YCSB gets
   it too because `ycsb_catalog.py` calls the same function.
4. **Agent validation** ([agent/harness/validation.py:582](../agent/harness/validation.py#L582)),
   next to `_check_fresh_storage`:
   - `remove_per_repetition: true` with `remove_existing: false` → error
     (contradiction).
   - `remove_per_repetition: true` with `repetitions` 1 → warning (no effect),
     if the harness has a warning channel; otherwise leave it.
5. **Docs**: `docs/AgentHarness.md` (near line 238) one sentence; the CLI help
   dumps in `docs/` (e.g. `docs/Example-Hardware.md:3308`) are regenerated, not
   edited by hand, if there is a script for that.

### M3 — tests

- `tests/test_storage_classes.py`: `build_tpch_argv` emits `-rsrp` (and `-rsr`)
  for `remove_per_repetition: true`; not without storage class; bool
  validation; `removes_storage_per_repetition` defaults.
- `tests/test_ycsb_catalog.py`: flag reaches the YCSB argv.
- `tests/test_agent_harness.py`: contradiction refused.
- New unit test for the predicate: `-rsr` → True only at done == 0;
  `-rsrp` → True at done == 0, 1, 2; always False once `loading_finished`;
  missing key in `args_dict` → behaves like today.
- Test that a lifecycle `start_sut()` in repetition 2 with `-rsrp` calls
  `delete_pvc` for storage, tenant and worker PVCs (stub cluster as in
  `tests/test_naming_conformance.py:222`).

### M4 — cluster check

One short TPC-H run, `-rst cephcsi -rss 10Gi -nc 2 -rsrp`, one DBMS:
- log shows "storage ... should be removed" / "is gone" twice;
- both repetitions have their own, different `time_loading`;
- without `-rsrp` (only `-rsr`), repetition 2 shows "storage ... exists" and
  the copied loading time.

## Open questions

- **Name.** `-rsrp` / `remove_per_repetition` is proposed. Alternative: turn
  `remove_existing` into `false | true | "per_repetition"` — one field, but it
  breaks the bool check and the agent's existing understanding. Prefer the
  separate bool.
- **Should `-rsrp` imply `-rsr`?** Proposed: yes (the predicate makes it so),
  and the catalog does not require both. The argv builder can still emit both
  for readability.
- **Evaluation.** Checked: nothing to change for `-rsrp`. Each connection
  stores `cfg.time_loading` of its own repetition
  ([metrics.py:123](../bexhoma/configurations/metrics.py#L123)), the evaluator
  reads `time_load` + `experiment_run` per connection
  ([evaluators/base.py:618-622](../bexhoma/evaluators/base.py#L618-L622)) and
  `get_loading_per_run()` groups by `experiment_run`. Same path as ephemeral
  storage, which reloads every repetition already.

### M1b — mark repetitions that did not load

The gap is the *existing* behaviour without `-rsrp`: repetitions 2..n copy
`time_loading` etc. from the PVC labels of run 1, and nothing in the result
says so (`storage_reused` deliberately covers only a volume from an earlier
experiment, [lifecycle.py:612-616](../bexhoma/configurations/lifecycle.py#L612-L616)).
`get_loading_per_run()` then shows identical loading times for runs 2..n that
look measured.

1. Add `cfg.loading_inherited` (reset to False in `reset_sut()`), set True in
   `set_labels_from_loaded_pvc()` whenever labels are copied.
2. Store it in the connection next to `storage_reused`
   ([metrics.py:137](../bexhoma/configurations/metrics.py#L137)).
3. Evaluator: add a `loading_inherited` column in `add_connection_to_result()`
   (absent in old results → unknown, as `storage_reused`), keep it in
   `get_loading_per_connection()` / `get_loading_per_run()`.
4. Summary / agent result contract: loading statistics across repetitions use
   only rows with `loading_inherited` False; mention it next to
   `storage_reused` in `contracts/contract_result.yml:156`.
5. Test: run 2 with a kept PVC → True; with `-rsrp` or ephemeral → False.
