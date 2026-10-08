# Current agent: material weaknesses

Recorded on 2026-09-21 from the source review and executable probes in
`agent/analysis/current-agent-2026-09-21/`. This is deliberately a short repair
backlog. It excludes style issues and speculative improvements that do not
threaten safety or the validity of a benchmark conclusion.

Re-checked against the code on 2026-10-05. Each item below ends with its
status; none of the five is fully repaired.

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

**Status 2026-10-05: unchanged.** `Workspace.submit` in `agent/harness/tools.py`
still has no notion of a dry run; the guard is the withheld tool schema plus the
dispatch check in `agent/harness/agent.py`.

## 2. Accepted interpretations are not semantically tied to their evidence

The evidence gate proves that required result files were opened and that cited
paths are reachable. It does not prove that a cited file supports the claim or
that the final prose agrees with the accepted structured interpretation. A
model can cite an unrelated result file or contradict its recorded verdict in
its closing answer while the phase still succeeds.

**Repair criterion:** accepted claims carry structured evidence references that
resolve to the relevant metric/check, and the delivered answer is rendered from
or checked against the accepted record.

**Status 2026-10-05: partly repaired.** Since 2026-09-25 the harness files its
computed validity and result claims beside the model's verdict, withholds
comparisons it can show are invalid (for example YCSB throughput summed over
unequal pod durations), and carries the resulting measurement restriction into
the answer. A cited file is still not checked for supporting its claim.

## 3. A benchmark can pass without proof that the full dataset loaded

The result contract discloses that loading completeness is not verified. That
means a truncated or partially loaded dataset can produce clean-looking
throughput and latency numbers and still pass the current evidence workflow.

**Repair criterion:** each system records and validates expected-versus-loaded
row counts, or an equivalent workload-specific completeness invariant, before
performance results are claimable.

**Status 2026-10-05: open, disclosed.** `contracts/contract_result.yml` lists it
under `known_gaps` and tells the interpreter where to look for evidence of a
truncated load (the loading pods' sensor and stderr logs, and latency collapse on
queries touching a missing table). No check enforces it.

## 4. Submission can execute different catalog inputs from those validated

Submission stages immutable copies and their hashes, but the child process
still resolves the experiment through the live catalog path. If that file
changes between validation and child startup, the executed configuration can
differ from the provenance snapshot attached to the run.

**Repair criterion:** execution consumes the staged catalog, result contract
and environment snapshot, and verifies their recorded hashes immediately before
launch.

**Status 2026-10-05: partly repaired.** `Workspace.submit` refuses a
specification whose bytes, or whose catalog or environment file, differ from what
passed validation (`_fingerprint`), and stages copies of all inputs. The child
process is still started with `--catalog` pointing at the live catalog path
rather than the staged copy, so a change after the check and before it reads the
file is still possible.

## 5. Recovery state is not committed atomically

Trajectory events, status YAML and phase artifacts are separate writes. A crash
between them can leave a submitted experiment without recoverable status or
leave a newer follow-up invisible to the resume path, which currently starts
from the newest design root rather than reconstructing the latest durable phase.

**Repair criterion:** use an atomic phase checkpoint (or a replayable event
protocol with commit markers), then resume from the newest committed phase and
reconcile any submitted experiment by its durable code.

**Status 2026-10-05: open, mitigated.** Status files are still written with a
plain `write_text`. The in-cluster controller recovers a submission from durable
status and resumes by experiment code, and concurrent lifecycles now take
the run lock atomically (`agent/harness/_runlock.py`) and record their own
investigation directory (`--run-record`), which closed two races between them.
A crash between the separate writes can still lose a status file or a follow-up.
