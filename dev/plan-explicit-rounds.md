# Plan: explicit rounds as the experiment's source of truth

Status: **direction decided (2026-11-26), not implemented.** Comes out of the discussion of decision 4 in
issue #925 (TPC-DS data maintenance).

Related: [plan-start-conditions](plan-start-conditions.md) (ordering inside one round, kept as a later
schema extension), [Design-Yaml-Experiment-Entry-Script](Design-Yaml-Experiment-Entry-Script.md),
[plan-dbms-generic-verification](plan-dbms-generic-verification.md) (no DBMS or benchmark names outside
`bexhoma/benchmarks/<benchmark>/`).

---

## 1. Direction

| # | Decision |
|---|---|
| D1 | `experiment.yml` becomes the source of truth. A user or an agent writes it. The experiment dict either goes away or is built from it. |
| D2 | CLI options are helpers that build an `experiment.yml` for the most common cases. The YAML / dict is the powerful part. |
| D3 | The Python core stays generic: nothing about a DBMS or a benchmark outside `bexhoma/benchmarks/<benchmark>/`. |
| D4 | Rounds are explicit: a list of rounds, each a list of entries, and rounds may differ. Shortcuts such as `-ne` are expanded by the builder, not by the core at run time. |
| D5 | #925 uses explicit DM-only rounds. It does not depend on start conditions. |

Target shape of the benchmarker section (identical in the YAML and in the dict):

```yaml
benchmarker:
  - [{name: tpcds, parallelism: 1}]                                   # power
  - [{name: tpcds, parallelism: 4}]                                   # throughput 1
  - [{name: tpcds_dm, parallelism: 1, template: ..., parameters: {}}] # DM 1
  - [{name: tpcds, parallelism: 4}]                                   # throughput 2
  - [{name: tpcds_dm, parallelism: 1, ...}]                           # DM 2
```

---

## 2. Core: run any explicit list of rounds

The core assumes today that all rounds look alike in these places:

| # | Assumption | Where | Change |
|---|---|---|---|
| C1 | The benchmark of a job is found by position: `self.benchmarks[benchmark_run - 1]` | `end_benchmarking()`, `end_loading()` in `bexhoma/experiments/base.py` | Read `client` and `benchmark_run` from the job name (`...-<client>-<benchmark_run>`, see `generate_component_name()`), resolve the entry `name` from the experiment dict and pick the benchmark with that name. The summaries already do this (`is_own_benchmark()`, `get_benchmark_name_at()` in `bexhoma/evaluators/base.py`). |
| C2 | Per-round data outside the dict: `benchmarking_parameters_list[i]`, `benchmark_list`, `benchmark_list_template` | `bexhoma/configurations/base.py` | A round's parameters live only in its entries. The lists stay as builder input at most. |
| C3 | Round 0 is a template that is copied into every round | `add_benchmark_list()`, `add_benchmarking_parameters()`, `set_benchmarking_parameters()`, `set_benchmark_resetscript()` in `bexhoma/configurations/base.py` | Builder logic only. Running an experiment must not depend on it. |
| C4 | `-nc` repetitions rebuild the rounds from the templates | `_prepare_next_repetition()` in `bexhoma/experiments/base.py` | Replay the explicit rounds. Check what the dict path does today. |

Unaffected, as far as checked: the main loop already runs rounds one after the other; every entry has
its own `resetscript`; container tenancy, monitoring windows and the workflow planned/actual check work
per round.

Side effect: inserted rounds use up client numbers. With `-ne 1,4,4` and two DM rounds the connections
are numbered 1–5. Visible in connection names and summaries, nothing breaks.

Tests: unit tests for a dict with mixed rounds (C1 lookup per job name, parameters per entry, `-nc`
replay).

---

## 3. #925: TPC-DS data maintenance on explicit rounds

Everything in `bexhoma/benchmarks/tpcds/`:

- `cli.py` (or a builder there): `-xdm` / `-xdmo` and where DM rounds go. The spec order
  Power → Throughput 1 → DM 1 → Throughput 2 → DM 2 is `-ne 1,4,4` with a DM round after every round
  except the first. This placement rule is TPC-DS knowledge and stays here.
- `experiment.py`: `enable_data_maintenance()` writes the DM entries into the explicit round list and
  registers the DM benchmark with `add_benchmark()`. `add_configuration()` sets the DM template from the
  DBMS's `dockers:` entry via `refresh_template(dockers, docker, 'tpcds')`; a DBMS without one raises
  `IncompatibleBenchmark`, as for the TPC-H refresh stream.
- `benchmark.py`: the DM benchmark class, like `RefreshStreamBenchmark`: begin, end and duration per DM
  round, plus per-function times.

Effort, core part (section 2): about 40 lines of Python plus unit tests. No image changes, no Redis
counters.

The DM pod is scheduled and pulls its image after the query streams end. That gap is not part of the
measured DM time.

---

## 4. Later

1. The experiment YAML schema gets the explicit-rounds form. The short form `rounds: [1, 2]` of the
   current TPC-H `experiment.yaml` (`bexhoma/benchmarks/tpch/builder.py`) stays as a shortcut that
   expands into explicit rounds.
2. Start conditions (`start_after`, `start_delay`, see [plan-start-conditions](plan-start-conditions.md))
   as a schema extension for ordering inside one round: warm-up before the main run, staggered pods, DM
   overlapping the end of the streams. Explicit rounds can't express these.

---

## 5. Order

1. Core: C1–C4 with unit tests on mixed rounds.
2. #925 on top of it, all in `bexhoma/benchmarks/tpcds/`.
3. YAML schema with explicit rounds, then start conditions.
