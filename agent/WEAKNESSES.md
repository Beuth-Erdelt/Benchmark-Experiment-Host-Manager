# Current agent: material weaknesses

Recorded on 2026-09-21 from the source review and executable probes in
`agent/analysis/current-agent-2026-09-21/`. This is deliberately a short repair
backlog. It excludes style issues and speculative improvements that do not
threaten safety or the validity of a benchmark conclusion.

## 1. Phase and dry-run tool boundaries are advisory — partly repaired

The loop advertises a phase-specific tool list, but dispatch still accepts any
registered tool name. A model can therefore call an unadvertised write tool
during interpretation, and a dry run can call `submit` if the model emits that
name without having been shown its schema. This is a cluster-safety defect:
authorization must be enforced at dispatch, with dry-run submission impossible
below the model layer.

This has since happened in practice. Patrick's supervisor reported that Qwen
submitted a real experiment during a `--dry-run` design, although the submit
tool had not been offered to it. The server's tool-call parser only picks a
tool name out of the model's text, so a name the model remembered from the task
or the handbook went straight through to the cluster.

Patrick's fix on `dev` (commit `eff7c310`, 2026-09-21) closes the dispatch half.
Every tool call the model emits is now checked against the tools offered in
that phase before it runs, and a withheld name comes back to the model as an
error. This covers design, evidence interpretation and follow-up authoring,
because all model-issued calls pass through the same conversation loop. The dry-run case
is regression-tested. The second half is still open: the workspace itself does
not know it is in a dry run, so any future code path that dispatches outside
that loop would bypass the check.

**Repair criterion:** dispatch rejects every tool outside the active phase's
allowlist (done), and the workspace itself refuses submission in dry-run mode
(open).

## 2. Accepted interpretations are not semantically tied to their evidence

The evidence gate proves that required result files were opened and that cited
paths are reachable. It does not prove that a cited file supports the claim or
that the final prose agrees with the accepted structured interpretation. A
model can cite an unrelated result file or contradict its recorded verdict in
its closing answer while the phase still succeeds.

**Repair criterion:** accepted claims carry structured evidence references that
resolve to the relevant metric/check, and the delivered answer is rendered from
or checked against the accepted record.

## 3. A benchmark can pass without proof that the full dataset loaded

The result contract discloses that loading completeness is not verified. That
means a truncated or partially loaded dataset can produce clean-looking
throughput and latency numbers and still pass the current evidence workflow.

**Repair criterion:** each system records and validates expected-versus-loaded
row counts, or an equivalent workload-specific completeness invariant, before
performance results are claimable.

## 4. Submission can execute different catalog inputs from those validated

Submission stages immutable copies and their hashes, but the child process
still resolves the experiment through the live catalog path. If that file
changes between validation and child startup, the executed configuration can
differ from the provenance snapshot attached to the run.

**Repair criterion:** execution consumes the staged catalog, result contract
and environment snapshot, and verifies their recorded hashes immediately before
launch.

## 5. Recovery state is not committed atomically

Trajectory events, status YAML and phase artifacts are separate writes. A crash
between them can leave a submitted experiment without recoverable status or
leave a newer follow-up invisible to the resume path, which currently starts
from the newest design root rather than reconstructing the latest durable phase.

**Repair criterion:** use an atomic phase checkpoint (or a replayable event
protocol with commit markers), then resume from the newest committed phase and
reconcile any submitted experiment by its durable code.
