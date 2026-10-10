# Plan: studies as first-class records

Status: **planned, nothing implemented** (2026-10-10). The first increment
uses citations as *context* only; see "Scope of the first increment".

## Goal

The agent carries out a *study*: one question, answered by a series of zero or
more experiments. Zero is a legitimate outcome: the agent refused, or failed to
design an experiment. One or more experiments are an initial design plus
follow-ups or repeats.

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

## Scope of the first increment

In scope: M0–M6 of the implementation sketch.
- read-scope fix;
- study record;
- summary extension;
- study answer;
- baseline in the study;
- derived standing and operator withdrawal;
- discovery and context citations.

Later: M7 rerun (operator, then model), M8 model-proposed withdrawal, and the
anchor check.

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
    role: initial                         # initial | follow_up | repeat
    follow_up_of: null
    scaling_factor: 10
    standing: sound                       # as derived when last written
  - code: "1787179264"
    role: follow_up
    follow_up_of: "1787175665"
    scaling_factor: 10
    standing: failed
    failure: "benchmark process exited 1"  # only with failed
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

Numbers are never merged or compared across experiments.

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
  context) and `docs/AgentResultContract.md`.
- `contracts/contract_catalog.yml` (`cites`, 1.11.0),
  `contracts/contract_catalog_comments.md`, `docs/AgentCatalogContract.md`.
- `agent/WEAKNESSES.md`: the M0 hole, until it is fixed.
