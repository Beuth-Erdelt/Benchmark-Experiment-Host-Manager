# Plan: planned disruptions (pods or containers terminated on purpose)

Status (2026-11-25): **not started, deliberately later.** Split off from P11 of
`dev/plan-silent-malfunctions.md`. Nothing to build until a benchmark needs it, e.g. one that
measures the time a DBMS takes to recover after its pod or a container is terminated.

Goal: a benchmark may terminate SUT pods or containers on purpose. Such a run must pass when the
disruptions happened as planned, and still fail for every disruption that was not planned or a planned
one that left no trace. Without a declaration, every check stays as strict as today.

## 1. What a deliberate disruption triggers today

| Check | Where | Triggered by | Today |
|---|---|---|---|
| Replaced SUT pod is not loaded again (S18) | `LoadingCoordinator.start_exec()`, `bexhoma/configurations/loading.py` | pod deleted and replaced, during loading or benchmarking | **aborts the experiment** (`fail_loading_fatally`: "SUT pod ... replaced during benchmarking (n rounds submitted) ... it is not loaded again"), writes the restart snapshot with the new UID (`store_replaced_pod_snapshot()`) |
| `SUT pods not replaced` (S6, S13) | `ExperimentBase._test_sut_pods_not_replaced()` | a UID that changes within a repetition: loading start, round starts, end-of-repetition snapshot | failed test |
| `No SUT container restarts` | `ExperimentBase.show_summary_header()` | `restartCount` of a container in the same pod (kill of the process, OOM) | failed test |
| `SUT data survived container restarts` | same, from `*.describe.log` | a restarted container without a data volume | failed test, or skipped |
| Load counts as failed | `LoadingCoordinator.check_sut_restarts_during_loading()` | a container restart during loading | the volume is never labelled `loaded=True` |
| Benchmarker errors | evaluators | queries while the SUT is gone | counted and reported only (D1): fits |
| Runtime failures stored | `bexhoma-runtime-failures.json` (S19) | any of the aborts above | shown again by `bexhoma summary` |

Why the abort matters most: since S18 a recovery benchmark cannot even run to its end. Before S18 the
new pod was loaded again while the benchmarker pods ran, which is not a recovery either.

## 2. Design

1. **Declare.** The benchmark (or the experiment) declares its disruptions per repetition and round:
   target (SUT pod, a worker pod by component and index, a container by name), kind (`replace` = delete the
   pod, `restart` = kill a container in place), when (round, offset after the round started), how often.
   Stored in `queries.config` next to `workflow_planned`, e.g. `disruptions_planned`.
2. **Perform and record.** One component performs the disruptions (bexhoma itself via the API, or a
   disruptor job) and records each one: target, time, UID that went away, UID or restart count after. Stored
   in the result folder (`bexhoma-disruptions.json`, written like the runtime failures: atomic, read back by
   `bexhoma summary`). The recovery measurement needs these times anyway.
3. **S18 follows the plan.** A replacement that matches a declared one does not abort. bexhoma waits for the
   new pod; then, by benchmark:
   - data on a PVC: the new pod mounts it; copy the loading labels to the new pod (as an inherited volume
     does through the pod template), do not load again;
   - data without a PVC: either load again on purpose (the recovery includes the load) or declare that the
     benchmark measures an empty restart; the benchmark has to say which.
   An undeclared replacement keeps aborting.
4. **Compare observed with planned.** New test, e.g. `Disruptions as planned`:
   - every planned disruption has a record and a matching observation (new UID, restart count + n): passed,
     e.g. `SUT pods replaced as planned (1 of 1)`;
   - a planned one without a trace: failed (the benchmark did not do what it measures);
   - an observation not covered by the plan: failed, as today.
   `SUT pods not replaced` and `No SUT container restarts` then count only what the plan does not cover
   ("allowed n UIDs" / "expected restart count" instead of 1 UID / 0 restarts).
5. **No declaration: no change.** Every check stays strict.

## 3. Open questions

- Who performs the disruption: bexhoma (simple, same process, exact times) or a job (closer to an external
  fault, needs RBAC to delete pods)?
- Timing reference: offset after round start, after a synchronised start time (`BEXHOMA_TIME_START`), or a
  share of the benchmark duration?
- What "recovered" means per DBMS (first successful query, throughput back to x % of the level before),
  and whether bexhoma computes it or the evaluator.
- Workers of distributed DBMS (StatefulSets keep the pod name, only the UID changes; S13 already reads
  worker UIDs).
- Interaction with `-nc` repetitions and `-rsrp` (fresh volume per repetition).

## 4. Effort (rough)

| Part | Effort |
|---|---|
| Declaration + storage in `queries.config` | small |
| Performing and recording (bexhoma via API) | medium |
| S18 exception + label copy for PVC data | medium; the no-PVC case needs a decision per benchmark |
| Test `Disruptions as planned`, relaxed S6/S13/restart tests | medium |
| Cluster runs: replace and restart, with and without PVC, standalone and distributed | several runs |
