# Plan: studies as first-class records

Status: **planned, nothing implemented** (2026-10-10; planned series added
2026-10-14). The first increment uses citations as *context* only; see
"Scope of the first increment".

## Goal

The agent carries out a *study*: one question, answered by zero or more
experiments. Zero is a legitimate outcome: the agent refused, or failed to
design an experiment. One or more experiments are an initial design, or a
planned series of sibling experiments, plus follow-ups or repeats.

Each experiment of a study can be addressed on its own. Another study can cite
it, build on it or rerun it, without re-running the experiment or the whole
study.

## What already exists

- The *investigation* directory is already a study in all but name. It holds
  one question (`task.txt`) and one append-only `trajectory.jsonl`, with all
  phases and follow-ups inside it (`agent/ARCHITECTURE.md`, "Phase state and
  follow-ups").
- The experiment code is a global key: one result folder per code under the
  result root, with `agent_summary.yml` beside the report
  (`agent.py::_write_agent_summary`).
- `follow_up_of` is a code. `agent.py::_load_ancestor_summaries` walks it
  through the result root without caring which investigation ran the parent,
  so lineage across studies already works.
- Directory naming: `agent.py::_new_investigation_directory` creates a
  timestamp name (`%Y%m%dT%H%M%S%f`, with `-NN` on a clash).
  `agent.py::_label_design_investigation` later renames it to
  `<timestamp>-sf<scale>-<model>`. The rename can fail on Windows while
  Bexhoma holds `bexhoma.log` open.
- The bare-model baseline runs as a **separate** investigation, before design.
  `lifecycle.py::_link_baseline` appends one `baseline` event to the design
  trajectory, holding the baseline's absolute path.
- A model-chosen repeat exists inside a study: a follow-up with
  `independent_repeat: true`. `agent.py::_author_followup` requires every
  execution setting to equal the parent's.
- **Read-scope hole, found 2026-10-10.** `tools.py::Workspace.__init__` adds
  `results_root` to `_readable_roots`, so the design and follow-up authoring
  contexts can read *anything* under the result root:
  - every result folder and report;
  - `results/agent/` with every study's trajectory and answer;
  - the baseline's answer.

  `ARCHITECTURE.md` says design reads "resolve only inside contracts, the
  inbox, or the explicitly allowed environment file". The code does not
  enforce that. The model is not told these paths, but result codes appear in
  ancestor summaries, and `results/<code>/report/index.md` is easy to guess.
  Context-only citation is meaningless while this hole is open, so closing it
  is step M0.

## Decisions

1. **The study ID is the timestamp directory name, and it is permanent.** No
   rename after design. Scale factor and model become metadata in
   `study.yml`, not part of the path. The scale factor is listed per
   experiment, because a follow-up may change it.
2. **The experiment code stays the global experiment key.** An experiment
   belongs to exactly one study, the one that ran it. Any number of studies
   may cite it.
3. **`study.yml`** lives in the study directory. Only the harness writes it,
   never the model. See "Data shapes".
4. **`agent_summary.yml` gains `study`, `design` and (later) `repeat_of`.**
   All are written by the harness.
5. **The bare-model baseline belongs to the same study**, as an *arm*, not as
   an experiment.
6. **Study-level answer:** a list of the study's experiments and citations,
   written by the harness, followed by the model's unchanged answer.
7. **Any past experiment can be rerun**, by the operator or by the model,
   with deviations computed by the harness. Not in the first increment.
8. **An experiment has a standing**: sound, qualified, failed, withdrawn or
   superseded. It decides whether the experiment can be cited.
9. **The model may propose a withdrawal**, and the operator confirms it.
   Not in the first increment.
10. **Citations are context, not evidence** (decided 2026-10-10). A cited
    experiment's compact record steers design and may be named in the answer.
    The model never reads a cited experiment's report, and no claim in the
    verdict may rest on it. The harness-computed anchor check is deferred.
11. **A setting that one experiment cannot sweep becomes a planned series**
    (decided 2026-10-14). Example: the TPC-H scale factor, which is a single
    value per experiment. The design phase plans a sequence of sibling
    experiments that differ only in that setting, and the agent **may compare
    numbers across the siblings of one series**. Comparison stays forbidden
    everywhere else, in particular against cited experiments (decision 10).
    See "Planned series".

## Scope of the first increment

In scope: M0–M6 of the implementation sketch.
- read-scope fix;
- study record;
- summary extension;
- study answer;
- baseline in the study;
- derived standing and operator withdrawal;
- discovery and context citations.

Later: M7 rerun (operator, then model), M8 model-proposed withdrawal, M9
planned series, and the anchor check. M9 builds on M1–M3 and M5, not on M6.

Not part of this plan: exporting a run for publication (issue #795) is a
separate, decoupled extension in `dev/plan-publish-bundle.md`.

## Data shapes

### `study.yml`

```yaml
study_version: 1
study_id: "20261010T101500123456"        # == directory name
question_ref: task.txt
created: "2026-10-10T10:15:00+00:00"
model: <served model id>                  # design model; interpret model per experiment
status: running | answered | no_experiment | incomplete
no_experiment_reason: refused | design_failed | budget_exhausted   # only with no_experiment
experiments:                              # ones this study ran, in order
  - code: "1787175665"
    role: initial                         # initial | follow_up | repeat | series
    follow_up_of: null
    scaling_factor: 10
    standing: sound                       # as derived when last written
  - code: "1787179264"
    role: follow_up
    follow_up_of: "1787175665"
    scaling_factor: 10
    standing: failed
    failure: "benchmark process exited 1"  # only with failed
  - code: "1787190000"                    # (M9) a series sibling
    role: series
    series: s1
    level: 100                            # this sibling's value of the swept setting
    anchor_of: null                       # code of the repeated sibling, only for the anchor
    scaling_factor: 100
    standing: sound
series:                                   # (M9) absent when the study plans none
  - id: s1
    setting: workload.params.scaling_factor
    levels: [1, 10, 100]
    basis: "query time per scale factor"  # comparison basis, fixed before the run
    anchor: true                          # last sibling repeats the first level
    status: planned | running | complete | partial
    comparison: series/s1/comparison.yml  # harness-written, after the last sibling
cites:                                    # ones produced elsewhere, used here
  - code: "1786000000"
    study: "20260901T080000000000"        # from the cited summary; null for legacy
    use: context                          # only value in the first increment
    reason: "levels 1-8 settled; this experiment covers 16-64"
    cited_by: "1787175665"                # the experiment whose spec carried it
    standing_at_citation: sound
baseline:                                 # absent when not requested
  status: answered | failed
  model: <served model id>
  answer: baseline/answer.md
  trajectory: baseline/trajectory.jsonl
answer: answer.md                         # absent until the study ends
```

### `agent_summary.yml`, version 1.1.0

New fields, all optional:

```yaml
study: "20261010T101500123456"            # null when interpreted outside a study
design:                                   # from the archived experiment.yml
  workload: tpch
  scaling_factor: 10
  systems: [PostgreSQL]
  discriminates: [concurrency]
  levels:                                 # one list per declared factor
    concurrency: [1, 2, 4, 8]
cites: [{code: "1786000000", reason: "..."}]   # copied from the spec
```

Rules:
- `_load_ancestor_summaries` accepts every summary with the **same major
  version** (1.x.y). Today it requires the exact current version, so a plain
  bump would silently cut every older lineage.
  - Minor versions only add optional fields.
  - A different major version stops the walk, as today.
- **Why the summary carries its own version.** The result folder's archived
  `contract_result.yml` describes the summary format as it stood when Bexhoma
  *ran* the experiment. The summary is written later, by the harness that
  *interprets* it, so the two can differ. The summary's own
  `agent_summary_version` is therefore authoritative for parsing it.
- **Interpretation is unaffected.** Reading a report always uses that result's
  archived `contract_result.yml` (`agent.py::main`). The loader is harness
  code that reads only summaries, never reports.
- An older summary has no `design` block, so its levels show as unknown and
  are never guessed from the hypothesis.

### `standing.yml`, in the result folder, append-only

```yaml
- standing: withdrawn | superseded | withdrawal_proposed | withdrawal_rejected | reinstated
  reason: "..."
  by: operator | model
  date: "..."
  superseded_by: "<code>"                 # only with superseded
```

### Experiment spec: `cites`

A new optional top-level field in `experiment.yml`:

```yaml
cites:
  - code: "1786000000"
    reason: "levels 1-8 settled; this experiment covers 16-64"
```

`use` is not in the spec. In the first increment it is always `context`, and
the harness adds it in `study.yml`.

## Standing

| standing | set by | meaning | citable |
|---|---|---|---|
| `sound` | harness | report and complete summary, no failed checks, no restriction | yes |
| `qualified` | harness | report exists, but failed checks, `incomplete_record` or `measurement_restriction` | yes, flags travel with the citation |
| `failed` | harness | no usable report, or no successful interpretation | no |
| `withdrawn` | operator | a defect found later; reason required | no |
| `superseded` | operator | replaced by `superseded_by`; reason required | only explicitly (later) |

Rules:
- **Derived from files only:** the report, `agent_summary.yml`, the status
  file, and the newest operator entry in `standing.yml`. Nothing is typed in
  by hand.
- **`agent_summary.yml` is never rewritten**, so the original verdict stays as
  recorded.
- **`reinstated` undoes a withdrawal**, with a reason.
- **Withdrawn and superseded ancestors still load** in
  `_load_ancestor_summaries`, so lineage has no gaps. They carry their standing
  and reason into the follow-up author's context.
- **A later withdrawal does not rewrite an existing `answer.md`.**

## Study answer

`answer.md` is written once, when the study ends. That is either the final
interpretation, or a design that ended without a code. It has these parts:

1. **Experiments of this study.** Written by the harness, one entry per
   `study.yml` experiment, in order:
   - code, role, `follow_up_of`, standing;
   - hypothesis;
   - verdict status and conclusion;
   - failed checks and scope;
   - `incomplete_record` and `measurement_restriction`;
   - link to `report/index.md`.

   A missing summary is reported as missing; it is never filled from the
   trajectory.
2. **Cited experiments.** Written by the harness: code, study, reason,
   standing at citation, and the cited verdict, all from the cited summary.
   Labelled as context, not measured in this study.
3. **Answer.** The model's answer for the last experiment, unchanged. It still
   follows the archived result contract's `answer_contract`. The model's
   answer turn does not see parts 1 and 2.

Two special cases:
- **Zero experiments:** parts 1 and 2 are empty or absent. Part 3 is replaced
  by the `no_experiment_reason` and the design phase's own account.
- **Baseline:** never part of the study answer. `study.yml` links it.

Numbers are compared across experiments only among the siblings of one
planned series (decision 11). In the answer, a series appears in part 1 as
one group, with its harness comparison table, and the model's series verdict
is part of part 3. Numbers from different series, from follow-ups outside a
series, or from cited experiments are never merged or compared.

## Citations as context

Example: a new study tests PostgreSQL concurrency. An earlier experiment
settled 1–8 clients, so the new study starts above 8, with one overlapping
level.

1. **Find.** A new design/authoring tool, `find_experiments(workload?, system?,
   factor?)`, returns compact rows built by the harness:
   - code, study, title, hypothesis;
   - `design` block;
   - verdict status and conclusion;
   - standing with its flags;
   - deployment summary: images of its systems from the archived catalog,
     catalog contract version, placement nodes;
   - date.

   Rows come only from result folders that have an `agent_summary.yml`, and
   failed and withdrawn experiments are left out (the rerun will want them
   later, marked). The output is bounded: the newest N matches, with filters.
   No file under the result root becomes readable through it.
2. **Cite.** The model adds `cites` to its spec, with a reason per code.
3. **Validate.** The agent validator checks each citation:
   - the code exists and has a summary;
   - its standing is citable (refused otherwise, with standing and reason);
   - the code was returned by `find_experiments` in this context, the same
     principle as "evidence must have been read";
   - the code is not this experiment's own `follow_up_of` parent, which is
     already in lineage. That is a warning.
4. **Inform, without refusing.** A valid result includes `citation_notes`:
   - **overlap:** for each factor declared by both, whether at least one
     level is shared. No overlap gives a warning that a difference between
     the runs would stay invisible.
   - **deployment deviations** between the cited run and the new design, for
     the systems both use: image, catalog contract version, placement nodes.
     The model decides whether the old levels still apply.
5. **Record.** On submission the harness copies the citations into
   `study.yml` (with `use: context`, `study`, `standing_at_citation`,
   `cited_by`), and into the new experiment's summary after interpretation.
6. **Interpret.** The interpretation's user message gets the cited compact
   rows, labelled "context: not evidence for this result".
   `_InterpretationGate` already refuses evidence paths outside the current
   result folder, so a verdict cannot cite the old report. The answer may say
   "16–64 measured here; 1–8 settled by <code> under these deviations". It
   may not present one series from 1 to 64.

Where `find_experiments` and `cites` are available: in initial design and in
follow-up authoring, because both are design contexts. Not in
interpretation.

## Baseline inside the study

- **Layout:** the baseline writes into `<study>/baseline/`, with its own
  `trajectory.jsonl` and `answer.md`. It never writes into the study's
  trajectory, because `_carry_forward` rebuilds task, spec, code and budget
  from that trajectory.
- **Shared question:** `task.txt` is shared.
- **Isolation:** after M0, no design or interpretation context can read
  `<study>/baseline/`. A test pins this.
- **Failure:** a baseline failure sets `baseline.status: failed` and leaves
  the study's status alone.
- **Ordering:**
  - The first phase run for a new question creates the study.
  - Both `--phase baseline` and `--phase design` accept `--run <study>`.
  - Design refuses a study that already has experiments.
  - The lifecycle runs baseline (creates), then design with `--run`.
  - `_link_baseline` goes away.
- **Out of scope:** the with/without-handbook ablation runs two full
  pipelines, so it is two studies of the same question.

## Planned series (later, M9)

Some questions need a setting swept that one experiment cannot sweep: the
TPC-H scale factor, a storage class, a Bexhoma option without a sweep list.
The agent then plans a *series*: a sequence of sibling experiments, one per
level, that differ only in that setting. Within a series, numbers may be
compared across experiments (decision 11).

**First choice stays one experiment.** If the setting can be a declared
factor inside one experiment (concurrency, cpu, memory, and later
`storage_class` per `dev/plan-storage-class-sweep.md`), a series is refused,
with that hint. A series is for settings the catalog contract lists as
series-only.

### Authoring

- The design phase (and follow-up authoring) may submit a *series spec*
  instead of a single spec:

  ```yaml
  series:
    base: <an ordinary experiment spec>
    vary:
      setting: workload.params.scaling_factor
      levels: [1, 10, 100]
    basis: "query time per scale factor"
    anchor: true
  ```

- **Siblings by construction.** The harness expands `base` into one spec per
  level, changing only `setting`. The model never writes the siblings one by
  one, so "differ only in the swept setting" holds by construction. Each
  expanded spec goes through the normal validator. If one fails, the whole
  series is refused.
- **Series-only settings** are listed in the catalog contract (new
  `series_settings`), with the allowed value type. To start with:
  `workload.params.scaling_factor` and `resources.storage_class`.
- **Comparison basis before the run.** `basis` is required, and the
  hypothesis states the expected relation in it, for example "time per scale
  factor stays within 20 %" or "throughput scales linearly up to sf 100".
  For a scale factor, raw times are not comparable. This is the same rule as
  "criterion before the run" for staged optimization.
- **Anchor (recommended, not required).** With `anchor: true` the harness
  appends one more sibling that repeats the first level, with `anchor_of` set.
  It guards against drift between the runs: the siblings run hours apart on
  a shared cluster, and the Ceph pool load changes.
- **Budget.** A series uses one experiment from the budget per sibling,
  anchor included. A series that does not fit into the remaining budget is
  refused.

### Running

- **Sequential.** The harness submits the siblings one at a time in level
  order, and the anchor last. Each sibling gets its own code and result
  folder, and is interpreted on its own as today. The interpretation of a
  sibling does not decide follow-ups: no follow-up is authored until the
  series ends.
- **Failure.** A failed sibling is marked `failed` and the series goes on.
  The series ends `partial` when any sibling failed, `complete` otherwise.
  Missing levels are named, never interpolated.
- **Resume.** `--resume` continues with the next unsubmitted sibling,
  derived from `study.yml`.

### Comparison

After the last sibling, a *series interpretation* step runs:

1. **Harness table**, written to `series/<id>/comparison.yml`:
   - per level: code, standing, run dates, and the values of the metrics
     named in `basis`, read from each sibling's report;
   - deployment deviations between siblings (images, catalog version,
     placement nodes), from `study.deployment_diff` (M6). By construction
     only deployment can deviate; any deviation is a flag.
   - the anchor result: first level vs. anchor, with the step rule of
     `assess_comparison_quality`. When the anchor disagrees, the comparison
     is `qualified`, and the verdict must say so.
   - `hardware_baseline` status of the used nodes, where available.
2. **Model verdict.** The interpretation gate admits evidence paths in the
   result folders of the series' siblings, and nothing else. A claim that
   compares levels must cite evidence from each sibling it names. Context
   citations stay as in "Citations as context".
3. **Record.** The series verdict goes to `series/<id>/verdict.yml`. The
   per-sibling `agent_summary.yml` stays unchanged. After the series
   verdict, follow-up authoring sees it as the ancestor of a follow-up of
   the series.

What a series still cannot do: compare against experiments outside it,
including cited ones (that needs the anchor check), or relate *different*
metrics across experiments (see "Pattern: reference measurement").

## Rerun (later, M7)

A rerun is always a new experiment with a new code, in a new study, with
`role: repeat` and `repeat_of: <code>`.

What it keeps and what may change:
- **Kept: the design**, which is the spec minus `placement`.
- **May change: the deployment** — placement, images and other catalog values,
  catalog version, hardware, Bexhoma version.

Catalog modes:
- `pinned` (default) uses the archived catalog.
- `current` uses today's catalog.
- The operator may add `--set` overrides.

Recording and limits:
- The harness computes `deviations: [{field, original, rerun, cause}]`, where
  cause is `pinned`, `current`, `override` or `rebound`.
- Placement is rebound.
- A design that no longer validates is refused, never repaired.
- A pinned rerun needs a submission path that checks the archived catalog's
  integrity instead of the fingerprint against the current catalog.
- **Model-started:** in design, via a `rerun` tool. A `rerun_rationale` is
  required: why a rerun, the expected outcome, and the mode and why. The model
  has no `--set` overrides. The rerun consumes budget and needs no
  confirmation. `find_experiments` then also lists failed and withdrawn runs,
  marked.

## Model-proposed withdrawal (later, M8)

- **How it is proposed:** `record_interpretation` gets an optional
  `propose_withdrawal: {reason, evidence_paths}`, with the same read checks as
  the verdict's evidence. It applies to the current result only.
- **The run does not wait:** the harness appends a `withdrawal_proposed` entry
  and carries on.
- **While pending:** the standing is unchanged, but citations and ancestor
  rows show the flag. The proposing study starts no follow-up from that
  result.
- **The operator decides:** confirm or reject, with a reason either way. A
  pending-list command exists, and the lifecycle's final output names pending
  proposals.

## Anchor check (deferred)

- The harness reads both reports and compares the overlapping level with the
  step rule of `assess_comparison_quality`.
- It files `anchor: {level, cited, new, agrees}` beside the verdict.
- A single series appears in the study answer only when the anchor agrees and
  there are no deviations.
- The model's read scope stays one result.

## Open decisions

1. **Answer a study from citations alone?** That would be a fourth
   zero-experiment outcome, "existing evidence suffices". With context-only
   citations, the agent cannot verify such an answer itself, so it is not part
   of the first increment.
2. **Planned multi-experiment studies with harness comparison?** Resolved
   2026-10-14 as decision 11: see "Planned series". Two cases that led
   there, and how they fit now:
   - **Storage backend for PostgreSQL TPC-H.** `resources.storage_class` is
     a single value today, so it needs a series. Once
     `dev/plan-storage-class-sweep.md` makes it a factor inside one
     experiment, that is preferred, and the setting leaves the series-only
     list.
   - **HammerDB at 16 vs. 32 virtual users, each on a fresh volume**
     (2026-10-13). Today the operator runs two experiments (`-nbt 16` and
     `-nbt 32`, each with `-rsrp`) and merges them with
     `collectors.tpcc(path, [code_16, code_32])`. In one experiment,
     `-nbt 16,32` runs the second round on data the first one changed, and
     `-rsrp` (`dev/plan-storage-remove-per-repetition.md`) gives a fresh
     volume per repetition, not per round. The agent needs a `hammerdb`
     workload in the catalog either way. Preferred is still one experiment
     (virtual users as rounds, with a reload before every round); a series
     over virtual users is the fallback until then.

## Pattern: staged optimization (2026-10-13)

A study varies one factor, picks its optimal level, and then varies a second
factor with the first held at that level. Example: a fio sweep, first the
queue depth at a fixed block size, then the block size at the chosen queue
depth.

- **It fits the chain model.** Experiment 2 is a follow-up of experiment 1.
  It does not compare its numbers with experiment 1; it uses one conclusion
  of experiment 1, the chosen level, as a fixed setting. This is not a
  planned series: the second factor's levels depend on the first result.
- **Prefer one experiment when affordable.** `hardware.py` crosses its fio
  lists (`-xfid 1,4,16,64 -xfbs 4k,16k,64k,1M` runs all 16 combinations in
  one experiment), which shows interactions and keeps every comparison inside
  one code. Staging pays off when the full grid is too large.

Methodological rules for the design and follow-up prompts:
- **Interaction.** The optimum of the first factor may depend on the second.
  Experiment 2 varies the first factor again around its chosen level (e.g.
  `-xfid 8,16,32`), or a confirmation run follows.
- **Criterion before the run.** "Optimal" is fixed in the hypothesis: maximum
  throughput, a latency bound (e.g. p99 < 1 ms), or the knee of the curve.
- **Noise.** Repetitions, and a rule for when two levels count as equal.

What the agent needs:
1. **A `hardware` workload in the catalog** (only `tpch` and `ycsb` exist).
2. **A structured chosen level.** Today the follow-up author sees the parent's
   level only as prose in the verdict conclusion. Add to `agent_summary.yml`
   (with M2, version 1.1.0):

   ```yaml
   selected:                       # absent when the experiment selects nothing
     fio_iodepth: 16
     criterion: "max IOPS with p99 < 1 ms"
   ```

   It is written from `record_interpretation`, and must be one of the levels
   in the `design` block.
3. **Validation of the follow-up.** A follow-up whose parent has `selected`
   either holds that factor at the selected level, or declares it a factor
   again (the interaction check above). Anything else is refused.
4. **The answer names its sources.** "Queue depth 16 (<code 1>), block size
   64k given queue depth 16 (<code 2>)": conclusions are chained, numbers are
   not compared.

## Pattern: reference measurement (2026-10-13)

A study measures disk speed (fio) and network speed (sockperf), then a DBMS,
and relates the DBMS result to the hardware: "the DBMS reaches X % of the
volume's write IOPS", "commit latency is about N network round trips".

- **Not a chain and not a series.** Numbers of *different* metrics are
  related across experiments. As three separate experiments this is not
  allowed: outside a planned series, numbers are never compared across
  experiments, and a series compares one metric across siblings that differ
  in one setting.

### What works today: `environment.yml`

- `bexhoma environment create -xhw` runs the hardware baseline
  (`bexhoma/hardware_baseline.py`):
  - sysbench and fio on each node's local disk;
  - fio on a throwaway PVC of each named storage class;
  - optionally sockperf between nodes.

  The results go into `hardware_baseline` per node and per storage class, and
  `network_matrix` (`bexhoma/environment.py::apply_hardware_baseline`).
- The design prompt already points to these speeds
  (`prompts.py::_ENVIRONMENT_AVAILABLE`).
- `tools.py::_stage_provenance` copies `environment.yml` into the result
  folder at submission, so interpretation can read it inside the current
  result folder.
- The DBMS experiment measures its own use of disk and network (`-m`/`-mc`,
  Ceph pool metrics).

So "capacity X, used Y" fits into one result folder, with the hardware
speeds as facts about the cluster, not as an experiment.

Limits:
- **Different conditions:** the baseline is short (default size 256M) with
  fixed fio settings, not the DBMS's I/O pattern (e.g. WAL: 8k writes with
  fsync).
- **Different time:** measured when `environment.yml` was created, not during
  the run. The cluster is shared and the Ceph pool load changes.
- **Contract gap:** `contract_result.yml` describes the archived
  `environment.yml` only as "cluster descriptor used for validation". See
  the next subsection.

### Decision: interpretation may read `environment.yml`

Good idea, with rules. The archived `environment.yml` is inside the result
folder, so the interpretation gate already allows it; what is missing is a
contract rule for what it may support.

Why: a verdict that explains a result needs the hardware behind it (CPU
model and cores, RAM, kernel, storage backend and replication, network
latency). Without it, the model guesses or leaves the explanation out.

Rules, in `contract_result.yml` (`provenance.agent_inputs` and a new
`interpretation_context` entry):
1. **Snapshot from design time.** `environment.yml` describes the cluster
   when the experiment was designed, not when it ran.
2. **Run-time facts win.** For the nodes the run used, `connections.config`
   `hostsystem` (CPU, RAM, GPU, node, host system, disk) and the
   `*.describe.log` files are measured at run time. Where they disagree with
   `environment.yml`, the run-time value counts, and the difference is worth
   reporting.
3. **What it may support:**
   - static facts (hardware, kernel, runtime, storage class provisioner and
     Ceph pool) as context for an explanation;
   - `hardware_baseline` and `network_matrix` as reference values, always
     with their date, size and settings;
   - not occupancy (`free`, `requested`, `limits_pct`): stale by run time.
4. **Explanation, not evidence.** A claim built on environment facts ("CPU
   bound: 32 streams on 32 cores") is labelled an explanation. The verdict on
   the hypothesis rests on the result's own measurements.
5. **Only the nodes the run used.** The interpretation reads the entries of
   the nodes named in the describe logs (SUT, loaders, benchmarkers), not the
   whole file. This keeps the read budget small and matches the publish
   bundle, which keeps only used nodes (`dev/plan-publish-bundle.md`).

To do:
- the contract entries above, and `docs/AgentResultContract.md`;
- one sentence in the interpretation prompt: where the archived
  `environment.yml` is and what it may support;
- `hardware_baseline_status` (complete, missing) is passed on: a missing
  entry is reported as not measured, never estimated;
- a test that the interpretation gate accepts the archived `environment.yml`
  as an evidence path.

### Matched measurements

When fio must match the DBMS's I/O pattern, the baseline is not enough.
Two routes:
- **Inside one experiment (preferred):** a hardware round on the same node
  and volume as the DBMS, in the same code. Bexhoma has mixed experiments
  (several benchmarks in one code); whether hardware + DBMS on the same PVC
  works is not checked yet.
- **Reference experiments across codes:** needs its own comparability check
  (same node, same storage class, close time window, declared fio settings).
  This is a different check from the series comparison, and the large route.

## Implementation sketch

Each milestone ships with its tests and docs and leaves the pipeline working.

### M0 — close the design read scope

- `tools.py::Workspace.__init__`: drop `results_root` from
  `_readable_roots`. `restrict_to_result` keeps using `results_root` for its
  own check.
- Check first why it was added. The inbox (under `results/agent/inbox`) is a
  root of its own. `_await_result_folder` and `list_results` use
  `results_root`/`status_dir` directly, not via `read_file`.
- Tests:
  - design refuses `results/<code>/report/index.md`;
  - design refuses `results/agent/<study>/answer.md` and
    `<study>/baseline/answer.md`;
  - follow-up authoring refuses the parent's report;
  - the inbox stays readable.

### M1 — study record

New module `agent/harness/study.py`, with no model-facing code:

```python
STUDY_FILE = "study.yml"
STUDY_VERSION = 1

def create(directory: Path, task: str, model: str) -> dict: ...
def load(directory: Path) -> dict | None:              # None = legacy investigation
def save(directory: Path, record: dict) -> None:       # tmp + replace, like _write_agent_summary
def add_experiment(record, code, role, follow_up_of, scaling_factor) -> None: ...
def set_standing(record, code, standing, failure=None) -> None: ...
def add_citations(record, cited_by, citations: list[dict]) -> None: ...
def finish(record, status, no_experiment_reason=None, answer=None) -> None: ...
def study_id(directory: Path) -> str:                  # name; legacy: part before "-sf"
```

Changes in `agent.py::main`:
- **Design:** `study.create` right after `_new_investigation_directory`, or
  load it when `--run` is given (see M4). After `run_design`:
  - with a code: `add_experiment(code, "initial", None, sf)`;
  - without a code, at a terminal end: `finish(no_experiment, reason)`.
- **Interpret:** after a submitted follow-up, call `add_experiment(...,
  "follow_up" | "repeat", parent, sf)`. The role comes from
  `decision.independent_repeat`. At the final interpretation, call
  `finish("answered" | "incomplete")`, depending on `record_incomplete`.
- **Delete** `_label_design_investigation`, its call at `main`, the
  `phase_directory` re-rooting after it, the second `_record_run_directory`
  call, the `investigation_label_skipped` event, and `_name_component`. It is
  the only place that renames an agent folder. Neither the model name nor the
  scale factor goes into any path any more.
- **Replace what the name gave.** Today the README sells the label as
  identifying "the experiment scale and the exact served model, commit
  included, without opening the trajectory". That information moves to
  `study.yml`:
  - `model`: the served model id, unchanged, including its commit suffix;
  - `scaling_factor` per experiment.

  New operator command `python -m agent.harness.study list [--model ...]
  [--status ...]` prints one line per study: ID, model, scale factors,
  status, number of experiments, baseline yes/no.
- **Existing tests to change:** the rename assertions in
  `tests/test_agent_harness.py` (names ending in `-sf1-…`, and
  `investigation_label_skipped`). They become "the name is unchanged and
  `study.yml` carries model and scale factor".

The no-experiment reason comes from the design outcome. **What counts as
terminal must be checked against the code:**

| condition in `run_design` outcome | reason |
|---|---|
| no `validate` call at all, and a closing summary | `refused` |
| `attempts_used >= attempts`, no valid spec | `design_failed` |
| turn limit reached (`turns >= max_turns`) without submission | `budget_exhausted` |
| `ModelUnreachable`, `ContextWindowExhausted`, setup error | **not terminal**: status stays `running`, resumable |

A spec that validated but whose submission failed is a submission error,
not a no-experiment outcome. It stays `running`, so the operator can resume
it.

### M2 — summary extension

- `_write_agent_summary`: add `study` (from `study.study_id(run_directory)`,
  passed in) and `design`. Set `_AGENT_SUMMARY_VERSION = "1.1.0"`.
- `design` builder: `_design_block(experiment: dict) -> dict`.
  - workload name and `scaling_factor` from `workload.params`;
  - system names from `systems[]`;
  - `discriminates`;
  - levels per factor, using the same level extraction as
    `tools.py::_expected_levels` / `_resource_dimensions`, not a second
    parser. Concurrency comes from the rounds; cpu and memory from
    `resources`.
- `_load_ancestor_summaries`: accept any version with the same major part as
  `_AGENT_SUMMARY_VERSION`. Use a small `_compatible_summary_version(value)`
  helper, which `study.experiment_index` (M6) reuses.
- `contracts/contract_result.yml`, `agent_summary_contract`: version 1.1.0,
  the new fields with sources, and `lineage_use` unchanged.

### M3 — study answer

- New `study.render_answer(directory, record, results_root, model_answer)
  -> str`. It builds parts 1–2 from the summaries and the standing, then
  appends `model_answer`.
- `agent.py::_write_reports`: when `final`, write `render_answer(...)`
  instead of `summary`. The phase report under `reports/` stays the plain
  summary.
- **Zero experiments:** when M1 calls `finish(no_experiment, ...)`, also write
  `answer.md` with the reason and the design summary. Today `final` is false
  for a design without a code, so this is a new, explicit path, not a change
  to `final`.

### M4 — baseline in the study

- **`agent.py::main`:** `--phase baseline` and `--phase design` accept
  `--run`.
  - Baseline: `Trajectory(run_directory / "baseline")`, and the baseline
    answer goes to `baseline/answer.md`. Record `baseline:` in `study.yml`.
    The phase number and `phases/` entry for the baseline live under
    `baseline/` too.
  - Design with `--run`: refuse when `study.yml` lists experiments.
    `task.txt` must match the given `--task`, or `--task` is omitted and read
    from the file.
- **`lifecycle.py`:** run the baseline first, then design with
  `--run <baseline study>`. Delete `_link_baseline`. If the baseline fails
  before creating the study, design creates it.
- **`_carry_forward`:** unchanged. A test proves it ignores `baseline/`.

### M5 — standing

- `study.derive_standing(result_directory, status_file) -> dict` returns
  `{standing, flags, reason}`:
  - no report, or a failed status: `failed`;
  - summary flags present: `qualified`;
  - otherwise: `sound`;
  - then the newest operator entry in `standing.yml` overrides it.
- `study.append_standing(result_directory, entry)`: append-only. It refuses
  an entry without a reason for `withdrawn`, `superseded` and `reinstated`.
- **Operator CLI:** `python -m agent.harness.study standing <code>
  withdraw|supersede|reinstate --reason ... [--by <code>]`, and `... list`.
- `_load_ancestor_summaries` attaches `standing` to each summary it returns,
  so the follow-up author sees it.
- **Lifecycle:** when a definitive benchmark failure leads to
  `_cleanup_failed_benchmark`, the next phase marks that experiment `failed`
  in `study.yml`. A study whose last experiment failed ends with status
  `incomplete`, and its answer lists the failure.

### M6 — discovery and context citations

- **Catalog contract** (`contracts/contract_catalog.yml`,
  `experiment_schema.fields`): add `cites`, typed as a list of
  `{code: str, reason: str}`, with semantics "context only; never evidence".
  This is catalog contract minor version 1.11.0, plus
  `contract_catalog_comments.md`.
  - Watch the catalog read limit: the catalog is already close to the
    read limit, so keep the entry short.
- **`bexhoma/spec.py::validate_experiment`:** shape check only, next to
  `follow_up_of`. Bexhoma itself ignores the field.
- **Index:** new `study.experiment_index(results_root, filters, limit) ->
  list[dict]`. It scans `results_root/*/agent_summary.yml`, plus
  `standing.yml` and the archived `contract_catalog.yml` for the deployment
  summary.
  - The images come from `systems.<name>.image` of the archived catalog,
    resolved through `extends:` like `bexhoma/spec.py` does. Use the shared
    resolver, not a copy.
  - No cache in the first increment. Revisit if scanning gets slow.
- **Tool:** `find_experiments` in `tools.py`, added to `DESIGN_TOOLS` and
  `FOLLOWUP_AUTHOR_TOOLS` and dispatched in `Workspace.call`. The Workspace
  remembers the returned codes per context (cleared in
  `reset_read_context`). Its results count against the read budget like a
  file read.
- **Validation:** in `agent/harness/validation.py`, after the existing
  checks, `_citation_checks(experiment, index_lookup, seen_codes)`. It
  returns errors (missing, not citable, not seen) and `citation_notes`
  (overlap, deployment deviations). The deviations come from a new
  `study.deployment_of(result_directory)` and
  `study.deployment_diff(a, b)`. The rerun reuses both later.
  - **Fingerprint:** the validation fingerprint must include the cited
    codes' standing. A withdrawal between validate and submit must then
    invalidate the validation, and the existing fingerprint check in
    `submit` refuses.
- **Submission:** `tools.py::submit` returns the cited codes. `agent.py`
  calls `study.add_citations` for both design and follow-up submissions.
- **Interpretation:** `prompts.interpret_messages` gets an optional
  `cited: list[dict]` of compact rows, rendered under the "context: not
  evidence for this result" heading. `run_interpret` loads them from the
  spec's `cites` via the index. `_InterpretationGate` stays unchanged: it
  already refuses evidence outside the current result folder.
- **Prompts:** in `DESIGN_SYSTEM_PROMPT` and `FOLLOWUP_AUTHOR_SYSTEM_PROMPT`,
  one paragraph:
  - what `find_experiments` is for;
  - that `cites` needs a reason;
  - that citations are context;
  - that overlapping by one level is recommended.

  The handbook could get a short note on extending a settled range with an
  overlapping level. Its source rules apply.

### M7 — rerun (later)

- `study.rerun(code, mode, overrides)` is the operator entry point.
- A pinned-catalog submission path is added in `tools.py`/`submit.py`.
- `deviations` are recorded in `study.yml` and the summary.
- Then the model's `rerun` tool, with `rerun_rationale`.
- `find_experiments` gains `include_failed`.

### M8 — model-proposed withdrawal (later)

- An optional `propose_withdrawal` field in the `record_interpretation`
  schema.
- A check in `_InterpretationGate._section_errors`, with the same rules as
  `_evidence_error`.
- An append in `run_interpret`, plus confirm/reject in the M5 CLI.

### M9 — planned series (later)

- **Catalog contract:** `series_settings` (setting path, value type), and
  the `series` spec shape (`base`, `vary`, `basis`, `anchor`). Minor version
  bump, plus `contract_catalog_comments.md`.
- **Expansion and validation:** `study.expand_series(series_spec) ->
  list[dict]`, then the normal validator per sibling. Refused: a setting not
  in `series_settings`, a setting that is a declared factor or could be one
  (hint to the single experiment), fewer than two levels, duplicate levels,
  no `basis`, a series larger than the remaining budget.
- **Submission:** `tools.py::submit` accepts a validated series and submits
  only the first sibling. `study.yml` records the whole series as `planned`.
  The lifecycle submits the next sibling after the previous one is
  interpreted, until the list (and the anchor) is done. Follow-up authoring
  is skipped while a series is open.
- **Comparison:** `study.compare_series(record, series_id, results_root)`
  writes `comparison.yml`. It reads the basis metrics from each sibling's
  report through the archived result contract, reuses
  `study.deployment_diff` and the step rule of `assess_comparison_quality`.
- **Series interpretation:** a new phase, `--phase series`, with its own
  prompt. `_InterpretationGate` takes a list of admitted result folders
  instead of one; for every other phase the list holds only the current
  folder. Writes `verdict.yml`; `render_answer` (M3) shows the series group.
- **Prompts:** in `DESIGN_SYSTEM_PROMPT` and `FOLLOWUP_AUTHOR_SYSTEM_PROMPT`,
  one paragraph: when a series is allowed, that one experiment is preferred,
  the basis and the anchor.

## Existing investigations

- Old directories have no `study.yml`, and readers treat that as legacy.
- `study.study_id` returns the timestamp part before `-sf` for labelled
  directories.
- Old summaries (1.0.0) still load, and have no `design` block.
- Historical output is not migrated.

## Tests

- **M0:** design and authoring cannot read result folders, study
  directories or `baseline/`; the inbox stays readable.
- **M1:**
  - a new study keeps its timestamp ID after a submitted design;
  - `study.yml` goes from `running` to `answered`;
  - each no-experiment reason is produced, and each non-terminal error leaves
    the study `running`;
  - follow-up appends `follow_up`, and an independent repeat appends
    `repeat`;
  - a cross-study follow-up's parent still loads.
- **M2:**
  - the summary carries `study` and `design`, with the levels for a
    concurrency and a resource sweep;
  - 1.0.0 ancestors still load, and a 2.0.0 summary stops the walk;
  - a result whose archived contract describes 1.0.0 but whose summary is
    1.1.0 loads by the summary's own version.
- **M3:**
  - the answer lists experiments in order, with flags and standing;
  - a missing summary is reported, not filled in;
  - the model answer is unchanged, and the prompt for the answer turn is
    unchanged;
  - a zero-experiment answer exists.
- **M4:**
  - the baseline lands in `baseline/`;
  - the study trajectory has no baseline events, and `_carry_forward` is
    unaffected;
  - a failure leaves the study status alone;
  - design with `--run` refuses a study with experiments;
  - the lifecycle runs baseline then design in one study.
- **M5:**
  - every derived standing;
  - newest entry wins, and reinstatement works;
  - a reason is required;
  - withdrawn ancestors still load, with their standing;
  - a failed run is listed in `study.yml`;
  - `answer.md` is not rewritten after a withdrawal.
- **M6:**
  - **Index:** it filters, is bounded, and omits failed and withdrawn
    experiments.
  - **Validation errors:**
    - a cited code that was not seen, missing, or withdrawn is refused;
    - a withdrawal between validate and submit is refused at submit.
  - **Validation notes:**
    - overlap present or absent;
    - an image deviation reported.
  - **Recording and interpretation:**
    - `study.yml` and the summary carry the citations;
    - interpretation sees the cited rows;
    - an evidence path into a cited result is refused.
  - **Spec shape:** `bexhoma/spec.py` rejects a malformed `cites`.
- **M9:**
  - expansion changes only the swept setting;
  - each refusal reason above;
  - siblings are submitted in order, the anchor last, and `--resume`
    continues with the next one;
  - a failed sibling gives `partial`, and the missing level is named;
  - an anchor disagreement makes the comparison `qualified`;
  - the series gate admits sibling folders and refuses a cited or
    non-series result;
  - a per-experiment interpretation still admits only its own folder.
- **All milestones:** lifecycle `--resume` on a study, which the Kubernetes
  controller relies on.

## Docs and contracts to update

- `agent/ARCHITECTURE.md`:
  - "investigation" becomes "study" where meant;
  - phase state, user-facing answer contract, capability boundary (the new
    tool; the M0 scope now enforced);
  - local lifecycle (the baseline in the study);
  - known limits (context-only citations).
- `agent/README.md` and `docs/AgentHarness.md`, together. Both describe the
  `<timestamp>-sf<scale>-<model>` naming (README "investigation directory"
  paragraph, AgentHarness.md around line 436). Replace it with the permanent
  timestamp ID, `study.yml` and `study list`. `ARCHITECTURE.md` line 218
  says the same.
- `contracts/contract_result.yml` (`agent_summary_contract` 1.1.0;
  `known_gaps` entry on cross-experiment comparison mentions citations as
  context, and with M9 the comparison within a planned series) and
  `docs/AgentResultContract.md`.
- `contracts/contract_catalog.yml` (`cites`, 1.11.0),
  `contracts/contract_catalog_comments.md`, `docs/AgentCatalogContract.md`.
- `agent/WEAKNESSES.md`: the M0 hole, until it is fixed.
