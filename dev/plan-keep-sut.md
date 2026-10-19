# Plan: choose whether SUTs are kept, and never deadlock on a kept SUT

Status: **implemented** (2026-10-15), committed (`6d60215e`). Cluster check
2026-10-19 (TPC-H SF1 PostgreSQL `load -rst nvme,cephcsi -rsr -mse 1`):
the first run crashed when PostgreSQL-1 finished loading: `_waits_for_slot()`
called `sut_exists()` of the waiting PostgreSQL-2, whose `deployment_infos`
is still empty before its SUT starts (`KeyError: 'deployment'`); the unit
tests used stub status objects. Fixed in `configurations/status.py`
(`sut_exists()` is False without deployment infos), regression test with the
real `ComponentStatus` in `tests/test_keep_sut.py`. Rerun (1792368663):
PostgreSQL-1 "stopped instead of kept, PostgreSQL-2 waits for its slot"
(once), PostgreSQL-2 started, loaded and was kept (port-forward printed),
summary line "stopped instead of kept: PostgreSQL-2 waited for its slot".
**Done.**
Deviations: the workload info adds "stopped after loading" only for
`load -ks no` (a line on every `run` would be noise); the catalog
translators emit `-ks no` for every mode but `start`, so agent runs never
keep a SUT (contract 1.12.0, folded in, not released); the `--help` blocks
pasted in `docs/Example-*.md` are not regenerated.

## Problem

Whether a SUT is left running at the end is decided by the mode, and only
`run` can be changed:

| Mode | `stop_after_benchmarking` | SUT at the end | Can be changed |
|---|---|---|---|
| `run` | `args.skip_shutdown` | stopped | `-ss` keeps it |
| `load` | `True`, fixed (`experiments/base.py:312`) | kept | no |
| `start` | `True`, fixed (`experiments/base.py:286`) | kept, never loaded | no |

"Kept" means: the last repetition of **every** configuration keeps its SUT
(`_leaves_sut_running()`; earlier repetitions restart since the `-nc` fix).

Two defects follow:

1. **Hang with a SUT cap.** A kept SUT holds its slot under `-ms` (cluster
   cap, `cluster.max_sut`), `-mse` (experiment cap, `experiment.max_sut`) or
   `max_sut_dbms`. A configuration still waiting for that slot prints
   `has to wait - 1 running ...` forever, or until `-et` aborts the
   experiment. It happens as soon as there are more configurations than the
   cap: a storage/resource sweep (`-rst nvme,cephcsi`), several `-dbms`, a
   loading-pods sweep. Example: `bexhoma tpch ... -ms 1 -rst nvme,cephcsi load`
   keeps PostgreSQL-1, and PostgreSQL-2 never starts.
2. **No way to load and stop.** `load` cannot be told to clean up, so a pure
   loading measurement (e.g. bulk-write throughput per storage class) leaves
   SUTs and their nodes busy, and scripts need `bexperiments stop -e <code>`.

Minor: the workload info says "SUT pods are kept running" only for `-ss`, not
for `load`/`start`, which keep them too.

## Decisions

1. **One option `-ks/--keep-sut {auto,yes,no}`**, default `auto`.
   - `auto`: `yes` for `load` and `start`, `no` for every other mode. This is
     today's behaviour, so existing scripts and docs stay correct.
   - `yes`: keep the SUT of each configuration's last repetition.
   - `no`: stop every SUT, in every mode.
   - `-ss/--skip-shutdown` stays as an alias for `--keep-sut yes`.
     `-ss --keep-sut no` is a usage error.
   - `start --keep-sut no` is a usage error: `start` only starts SUTs.
2. **Keeping never blocks a waiting configuration (fixes the hang).** When a
   configuration's last repetition ends and keeping is on, its SUT is kept
   only if no other configuration of this experiment is still waiting to
   start *and* a cap applies to it (`experiment.max_sut`, `cluster.max_sut`,
   or `max_sut_dbms` for the same docker). Otherwise it is stopped like in
   `run`, with the message
   `{config}: stopped instead of kept, {other} waits for its slot (-ms N)`.
   - So under a cap of N, the last N configurations to finish are kept; with
     no cap, all are kept, as today.
   - SUTs of other experiments that fill a cluster-wide cap are not this
     experiment's to stop; that case is unchanged.
   - A stopped SUT on a persistent volume keeps its data: a later `run`
     without `-rsr` finds it loaded (`loading_inherited`).
3. **The result says what was kept.** The workload info states the resolved
   choice ("SUT pods of the last repetition are kept running" /
   "... are stopped"). `workload['sut_service']` (the port-forward lines in
   "Services") lists only the SUTs actually kept, as today; a SUT stopped by
   rule 2 gets a line there saying why.

## Implementation sketch

### M1: option and its resolution

- `bexhoma/cli_args.py::make_base_parser`: add `-ks/--keep-sut` with
  `choices=['auto', 'yes', 'no']`, `default='auto'`; keep `-ss`. Help texts
  name the per-mode default.
- `ExperimentBase.prepare_testbed`: resolve once into `self.keep_sut: bool`
  from `mode`, `keep_sut` and `skip_shutdown`; raise `ValueError` for the two
  conflicts. Entry scripts with their own parser may lack `keep_sut`: read it
  with `getattr(args, 'keep_sut', 'auto')`, as for `-rsrp`.
- `ExperimentBase.process`: pass `stop_after_benchmarking=self.keep_sut` in
  the `run` and `load` branches; `start` keeps `True`.
- Workload info line from decision 3 replaces the `skip_shutdown`-only line
  (`experiments/base.py:753`).

### M2: never keep a SUT another configuration waits for

- New `ExperimentBase._waits_for_slot(config) -> Optional[str]`: name of
  another configuration of this experiment that is not `experiment_done`,
  has no SUT yet (`not status.sut_exists()`) and is limited by a cap that
  counts `config`'s SUT; `None` otherwise. Pure enough to test with stub
  configurations.
- `_leaves_sut_running(config, ...)`: becomes an instance method; after the
  existing checks it returns `False` when `_waits_for_slot(config)` names a
  configuration, and prints the message from decision 2.
- The stop path is the existing `run` path, so logs, descriptions and
  restart snapshots are stored as for any stopped SUT, and
  `experiment_done` is set. The prepare-only benchmarker job
  (`only_prepare=True`) stays tied to a kept SUT.

### M3: tests

- Resolution: `auto` per mode, `yes`/`no`, `-ss` alias, both conflicts.
- `_leaves_sut_running` / `_waits_for_slot`: kept without a cap; stopped
  when a capped configuration waits; kept again once nothing waits; a cap
  for another docker (`max_sut_dbms`) does not count; repetitions still
  restart (existing `LeavesSutRunningTest`).
- Workload info line per resolved choice.

### M4: docs

- `docs/WorkBenchmarkList.md`: the pseudo-code still shows the old keep
  branch (no repetitions, no slot rule).
- The `--help` blocks pasted in `docs/Example-*.md` list `-ss`; regenerate
  them or add `-ks` by hand.
- A short note where `load` is described: `--keep-sut no` for loading-only
  measurements; `-ms` with several configurations keeps only the last ones.

## Risks and open points

- **Default for `load`.** `auto` keeps today's behaviour. If nobody relies
  on `load` leaving SUTs up, `no` would be the safer default; it changes
  what existing commands do, so it is not part of this plan.
- **Waiting configurations of a resumed experiment** (`-e <code>`): the slot
  check uses this process's configurations only; fine, since a resumed run
  rebuilds them.
- **`-et` timeout** stays the safety net for caps filled by other experiments.
