# Features

Traceability record for this repository. It has two parts, and both are kept
current in the same change that ships the work.

**Part 1** is the inventory: what exists, where it lives, and whether it is
finished. **Part 2** is the request log: what was asked for and when, in the
order it was asked. Nothing disappears silently — a feature that is removed or
replaced keeps its Part 1 entry, marked as such, with a pointer to whatever
replaced it.

---

## Part 1 — Inventory

### Agent harness

The contract-driven prototype designs, validates, submits, interprets, and may
follow up on a benchmark. The full current description and visual flow live in
`agent/ARCHITECTURE.md`; `agent/README.md` contains commands only.

| Component | Location | Status |
|---|---|---|
| Structured validation verdict | `agent/harness/validation.py` | Done |
| Catalog, shape, environment, and methodology validation | `agent/harness/validation.py`, `contracts/contract_catalog.yml` | Done |
| Phase-scoped tools, path policy, immutable submission, and deterministic query comparison | `agent/harness/tools.py` | Done |
| Exact one-result selection, link-reachable evidence reads, and result-contract answer structure | `agent/harness/prompts.py`, `agent/harness/tools.py`, `contracts/contract_result.yml` | Done and regression-tested |
| Model adapter for the self-hosted server | `agent/harness/model_client.py` | Done |
| Per-turn output sized to the served context window, with an exhausted window reported like other setup errors | `agent/harness/model_client.py`, `agent/harness/agent.py` | Done and regression-tested |
| Design, one-result interpretation, bounded follow-up authoring, durable lineage, phase reports, standalone `--report` operation, and CLI | `agent/harness/agent.py` | Done and regression-tested |
| Human-readable completed-investigation names containing scale factor and served model | `agent/harness/agent.py`, `agent/trajectories/` | Done and regression-tested; incomplete designs remain timestamp-only |
| Model server manifest with idle GPU release | `agent/k8s/vllm-qwen38-27b.yml` | Done |
| Durable Kubernetes lifecycle controller with in-cluster authentication and restart recovery | `agent/lifecycle_controller.py`, `agent/k8s/lifecycle-controller.yml`, `agent/Dockerfile.lifecycle` | Done and regression-tested; image publication and target-cluster values remain deployment steps |
| Sequential isolation of agent-submitted SUT configurations | `agent/harness/submit.py`, `contracts/contract_catalog.yml` | Done and regression-tested through BeXhoma's public one-SUT option |
| Result-contract disclosure of unverified loading and of the warnings check's real scope | `contracts/contract_result.yml`, `docs/AgentResultContract.md` | Done |
| Result root taken from Bexhoma's `cluster.config` | `agent/harness/tools.py` | Done |
| Environment refresh with local cluster facts | `dev/catalog/refresh_environment.py` (gitignored) | Done |
| Repeated same-system treatments rejected before Bexhoma collapses them | `agent/harness/validation.py` | Done and regression-tested |
| Distinct identities for every CPU or memory resource-sweep cell | `bexhoma/spec.py`, `tpch.py` | Done and regression-tested |
| Component-aware peak resource validation for pinned benchmarker placement | `contracts/contract_catalog.yml`, `agent/harness/validation.py` | Done and regression-tested; mirrors the current BeXhoma template limits |
| Stable upstream BeXhoma integration | repository history, `bexhoma/experiments/tpch_catalog.py` | v0.10.10 merged; local agent and loading safeguards preserved and regression-tested |
| Environment-checked submission gate and recoverable slow-start state | `agent/harness/tools.py` | Done and regression-tested |
| Agent-exposed per-configuration loading timeout and automatic failure diagnostics | `contracts/contract_catalog.yml`, `bexhoma/spec.py`, `bexhoma/experiments/base.py`, `bexhoma/configurations/lifecycle.py` | Done and regression-tested |
| Enforced initial catalog/environment consultation | `agent/harness/agent.py` | Done and regression-tested |
| Validity-first evidence gate, read-path citations, and result-contract-driven answer | `agent/harness/agent.py`, `agent/harness/tools.py` | Done and regression-tested |
| Deterministic query coverage, throughput comparability, and repetition-anomaly disclosure | `agent/harness/tools.py`, `agent/harness/agent.py`, `agent/harness/prompts.py` | Done and regression-tested without changing BeXhoma |
| Conservative timeout-cost estimate and enforced focused-query follow-ups | `agent/harness/validation.py`, `agent/harness/agent.py`, `agent/harness/prompts.py`, `contracts/contract_catalog.yml` | Done and regression-tested |
| Exact `follow_up_of` lineage and rejection of execution-identical follow-ups | `agent/harness/agent.py` | Done and regression-tested without changing BeXhoma |
| Portable per-experiment hypothesis verdict and compact ancestor memory for follow-up authoring | `agent/harness/agent.py`, `agent/harness/prompts.py`, `contracts/contract_result.yml` | Done and regression-tested without changing BeXhoma |
| Installable agent and TPC-H launcher package | `pyproject.toml` | Done and wheel-smoke-tested outside the checkout |
| Maintained-suite test discovery | `pyproject.toml` | Done; plain `pytest` runs `tests/` |
| Local server/benchmark lifecycle, retry, resume, signal-safe cleanup, namespace restoration, restart of a self-finished pod, and exact failed-experiment cleanup | `dev/agent_lifecycle.py`, `dev/model_server.sh` | Local-only; unit- and cluster-checked |
| Quick start | `agent/README.md` | Done |
| Full pipeline, annotated visual, replay rules, and decision record | `agent/ARCHITECTURE.md` | Done; all older agent-pipeline descriptions merged here |
| Critic as a separate invocation | — | Optional evaluation, intentionally outside the prototype |

All model contexts share one bounded conversation loop but receive different
prompts and tools. Contracts are read rather than embedded, all reads and writes
are logged, and submission is bound to the exact validated specification and
contract hashes.

### Cluster configuration

The default cluster-level monitoring endpoint points to the shared Prometheus
service in the `monitor` namespace. The per-experiment application-monitoring
endpoint remains templated because Bexhoma creates that service in the active
experiment namespace.

### Model server

`agent/k8s/vllm-qwen38-27b.yml` serves `Qwen/Qwen3.8-27B-FP8` through vLLM's
OpenAI-compatible API on the first available H100 or H200 node. It follows the pattern already
used for the other model servers in this namespace: one pod that downloads the
weights into a persistent volume on first start and serves them from there
afterwards. It is deliberately not placed on the node bexhoma uses for the
system under test, because a model server competing for that node's resources
would contaminate the measurements the agent is designing.

The pod releases its GPU on its own once nothing has sent it a request for
twenty minutes, so a server left behind by a hand-launched phase does not hold a
Hopper node indefinitely. The operator wrapper still shuts it down immediately
when it is in charge; the watchdog is the backstop for when it is not.

Which server the agent talks to is not fixed to that pod. The agent CLI
(`agent/harness/agent.py`) and the local lifecycle wrapper
(`dev/agent_lifecycle.py`) load an optional `.env` from the repository root at
startup, supplying `AGENT_MODEL`, `AGENT_BASE_URL`, and `AGENT_API_KEY` where
the shell has not already exported them. An exported variable overrides the
file, and the corresponding command-line flag overrides both. `.env.example`
documents a block per backend — the bundled vLLM server through a port forward,
the same server by its in-cluster service name, a local Ollama, OpenAI, and
Mistral — and `.env` itself is gitignored so keys stay out of the history. The
loader is `python-dotenv`, added to the `agent` extra alongside the OpenAI
client.

Two adjustments in the model adapter make a hosted endpoint usable in place of
the self-hosted one. The context-length probe accepts either spelling a server
publishes it under (`max_model_len` for vLLM, `max_context_length` for
Mistral), so the per-turn budget guard keeps working off the cluster. And a
turn refused for rate limiting is retried with a doubling wait, honouring a
`retry-after` header when one is sent, before the phase reports the endpoint as
unusable. A self-hosted server queues requests rather than refusing them, so
this engages only against a metered API, where a per-minute quota would
otherwise end an investigation mid-design.

---

## Part 2 — Request log

### 2026-08-27 — Configure the model backend from a .env file

Asked whether a `.env` file existed for choosing the model server, and for a
configuration that swaps the agent easily between the cluster's vLLM server, a
hosted API such as OpenAI or Mistral, and a local Ollama. No such file existed:
the three settings were readable only from exported shell variables or flags.

Both entrypoints now load a repository-root `.env` before parsing arguments, so
the file supplies `AGENT_MODEL`, `AGENT_BASE_URL`, and `AGENT_API_KEY` when the
shell has not. Precedence runs flag over exported variable over file, which
keeps a one-off override possible without editing the file. A committed
`.env.example` documents a block for each backend, `.env` is gitignored, and
`python-dotenv` joins the `agent` extra. Where the three existing settings may
come from is all that changed for the self-hosted path.

Running the first Mistral-backed investigation then exposed two gaps the
self-hosted server had hidden, both fixed in the model adapter: the served
context window went undetected because Mistral publishes it under a different
field name, and a design phase died on a rate-limit refusal four turns in.
Refused turns are now waited out. No contract or BeXhoma code changed.

### 2026-08-27 — Label successful trajectories with scale and model

Asked to check the trajectory archive as well as the result folders, rename the
two verified end-to-end investigations, and make future trajectory names expose
the experiment scale factor and model used. The SF1 and SF10 investigations are
now named `20260824T095408142020-sf1-qwen3.8-27b` and
`20260825T162917565149-sf10-qwen3.8-27b`. No incomplete historical trajectory
was renamed or removed.

A new design still begins in a timestamp-only directory because the scale
factor is not known until the generated experiment has passed validation. On
successful completion, the harness reads the validated specification and
renames the directory to `<timestamp>-sf<scale>-<model>`. It records that
relocation in the append-only trajectory and resolves archived specifications
from their stable phase-relative location when resuming, so the readable name
does not break interpretation or lifecycle discovery. Submission-status paths
are relocated with the directory, and the lifecycle wrapper now passes its
configured persistent status directory into every agent phase. This preserves
restart recovery in the Kubernetes controller as well as in local runs. Unsafe
model-name characters, such as the slash in a repository-style model
identifier, become hyphens. Incomplete designs retain timestamp-only names
rather than advertising unvalidated metadata. No BeXhoma code or Kubernetes
template was changed.

### 2026-08-27 — Preserve compact hypothesis verdicts across follow-ups

Asked to adopt the proposed per-experiment `code / hypothesis / verdict`
record so a follow-up can consider what its ancestors already settled without
oscillating between hypotheses. The one-result evidence boundary remains
unchanged: interpretation reads and judges exactly one result folder.

The structured interpretation now records a scientific hypothesis status —
supported, refuted, inconclusive, or invalid — separately from the report's
mechanical pass/fail/skip checks. After that record is accepted, the harness
writes `agent_summary.yml` into the interpreted result folder. It contains the
experiment code, parent code, archived hypothesis, scientific verdict,
technical validity, unresolved next question, and result-relative evidence
paths. The artifact is produced from the existing interpretation call; no
second model response or competing conclusion is introduced.

Follow-up authoring walks `follow_up_of` and receives valid ancestor summaries
oldest-first. It does not receive ancestor reports, metrics, trajectories, or
conversations, and the summaries are explicitly orientation rather than
evidence for the current interpretation. Traversal stops safely at a missing,
malformed, mismatched, or cyclic record. The result contract documents this
agent extension separately from BeXhoma's unchanged result schema version.
No BeXhoma implementation or Kubernetes template was changed.

### 2026-08-27 — Make the experiment lifecycle durable and isolate system loaders

Asked why an SF3 comparison exposed a loader failure that earlier comparisons
did not, how to prevent it, and to move the full experiment lifecycle into a
Pod without changing BeXhoma. Earlier generator logs showed zero-second
generation for both systems because those scale-factor directories were
already complete. In the failed SF3 run, PostgreSQL and PgDuckDB entered a new
shared directory one second apart; one generated the files while the other
blocked forever on an interactive overwrite prompt. The 30-minute loading
deadline detected that hang rather than causing it.

No BeXhoma implementation or template was changed. The agent submission adapter
now invokes BeXhoma's existing maximum-one-SUT option for every submitted run.
System configurations consequently load and benchmark sequentially, preventing
both cold-cache generator races and cross-system resource contention. The input
contract discloses this execution invariant, while concurrent query streams
inside the active SUT remain controlled by the experiment's rounds.

The new lifecycle controller is packaged as a Kubernetes Job rather than a bare
Pod. A persistent volume holds trajectories, statuses, inbox files, refreshed
environment facts, and results. The controller uses a namespace-scoped service
account instead of an expiring workstation login, writes a runtime cluster
configuration from the supplied portable settings, and resumes the latest
durable submission after restart. It also recovers the narrow case where the
benchmark was recorded in status after launch but the agent process stopped
before writing its phase outcome. Because Pod replacement also ends detached
children, the replacement controller reacquires the shared result lock and
restarts BeXhoma's own resume path with the same experiment code, archived
catalog, and immutable submitted specification. Cluster-wide permissions are read-only and
limited to the node, storage-class, and priority-class facts used in the
environment contract; the model still has no terminal or Kubernetes tool.

The quick start documents image build and publication, input ConfigMap creation,
the four target-cluster values that must be supplied, Job launch, and log
following. There is deliberately no Job runtime deadline because a valid SF10
or SF100 investigation may run for days.

### 2026-08-26 — Remove only stale failed-experiment resources

Asked whether the many pods visible in k9s consumed benchmark resources, to
remove stale ones safely, and to prevent failed experiments from leaving them
again. The inventory separated shared BeXhoma infrastructure from
experiment-scoped objects. The per-node `bexhoma-monitoring-default-*` Pods are
the expected monitoring DaemonSet, while the dashboard and message queue are
shared services; they were retained. Completed unrelated Jobs do not consume
CPU or memory. Only resources carrying the exact codes of two previously failed
experiments were removed, and their result folders were preserved.

The local lifecycle now invokes Bexhoma's existing `stop -e <code>` cleanup when
the exact submitted benchmark is marked failed or its process has exited before
writing a report. It never applies an unscoped delete and does not clean a live
run merely because the wrapper is interrupted, preserving the documented
resume behavior. The input contract also tells the experimenter to choose a
scale-appropriate loading deadline rather than leave a hung loader unlimited;
there is intentionally no fixed deadline that would be wrong for SF10 or SF100.
Tests verify the exact cleanup code and the existing server-shutdown behavior.

### 2026-08-26 — Make one experiment the unit of interpretation

Asked to implement the supervisor's intended prototype model: the agent
evaluates one completed experiment at a time, reports what remains open, and
may design one next experiment carrying `follow_up_of`, without loading prior
reports into the same context or producing a cross-experiment synthesis. The
change was restricted to the agent, its contracts, tests, and documentation;
no BeXhoma implementation or Kubernetes template was changed.

Interpretation now starts from one explicit `report/index.md`. The portable
command accepts that file directly through `--report`, so it does not depend on
this machine's trajectory, status, or cluster configuration files; when no
result root is configured, it derives that root from the selected report. In
the evidence context, the exact report, exact result contract, and archived
experiment are the initial readable interface. A successful Markdown read
exposes only existing local files linked from that page and still inside the
same result directory. Unlinked files and sibling experiment folders are
rejected by code, not merely discouraged by the prompt.

The interpretation's structured record now includes its finish-or-follow-up
decision. This removes the separate decision context, the model-facing result
listing, the cross-result latency tool, the previous-result handoff, and the
fixed eight-section aggregation template. The closing answer follows the
archived result contract's `answer_contract` and discusses the current
experiment only. If a follow-up is justified and budget remains, a fresh
authoring context rereads the input catalog and environment. Before shared
validation can accept the draft, the harness requires `follow_up_of` to equal
the current experiment code and rejects a draft whose execution-relevant fields
are identical to its parent. Focused-query and cost checks remain unchanged.

The local BeXhoma report writer remains at schema version 1.3.0, so the result
contract keeps that version rather than implying a BeXhoma change. The new
`answer_contract` is consumed by the agent as an interpretation instruction; it
does not alter the generated result-folder layout or report frontmatter.

Regression tests cover the exact read boundary, standalone one-result behavior,
combined interpretation decision, mandatory lineage, repeat rejection, and the
reduced phase-specific tool sets.

### 2026-08-26 — Keep every turn inside the served context window

Asked for the minimum change that prevents the context and output window
failures, after an interpretation died without leaving a trace. That phase had
finished its analysis and had its structured record accepted; the single
remaining turn, which writes the report as prose, asked to reserve half the
window on top of a conversation that already filled half, so the server refused
the request outright. Because only an unreachable endpoint was translated into a
reported failure, a refused request ended the process with a stack trace and no
record, and eleven minutes of accepted work were lost.

The reading guardrails already bound what enters a context — capped whole-file
and section reads, a cumulative allowance per phase, fresh contexts between
stages — but nothing related the per-turn output reservation to any of it. The
model adapter now asks the server once for the context length it serves and
sizes each turn's reservation to what the conversation actually leaves, keeping
the configured ceiling whenever it fits. The estimate is anchored on the prompt
count the server reported for the previous request, so only the turns appended
since then are approximated, and a margin is held back for the chat template.
When too little room remains to answer at all, the adapter raises before
sending, and the phase reports the exhausted window and records an aborted
event exactly as it already did for an unreachable endpoint. A server that does
not publish its window keeps the configured ceiling unchanged.

This also resolves a conflict between the two documented window failures. A
model that spends a whole turn thinking and returns nothing is remedied by
raising the per-turn ceiling, which is what the failed run had done at twice the
default; that remedy is now safe, because a ceiling too large for the remaining
window is narrowed instead of overflowing it.

### 2026-08-26 — Disclose the unverified load in the result contract

Asked to improve the result contract after a completed follow-up run reported a
clean-looking repetition whose numbers were physically impossible. In that run
the Kubernetes node hosting the system under test lost its readiness part-way
through one loading phase, so every new connection was refused; three tables and
part of a fourth never loaded, and the run still reported ten passed checks. The
contract said nothing about loading being unverified, and its `no_sql_warnings`
entry claimed a result-set comparison "across systems" that the driver never
performs.

The contract now lists `loaded_data_complete` among its validity entries, marked
not implemented, and states plainly that a loading phase counts as successful
when its Kubernetes Job exits zero. A new known gap explains why a partial load
survives every implemented check, and names the tier-3 evidence that exposes
one: the post-load statistics script's stderr carries a live row count per
table, its stdout prints the reference-table counts that script already selects,
and each loader pod's log shows a row count per table or the client error that
replaced it. The `no_sql_warnings` entry now describes what the driver actually
compares — result sets stored inside one process — and records that BeXhoma
gives every benchmarking pod its own process and one connection, so the check
passes vacuously at a single query repetition and never certifies agreement
between two systems, phases or repetitions. Two loader-pod log patterns that
the detection recipe depends on were missing from the provenance listing and are
now described, and the pod-description entry now mentions node-readiness events,
which is where this incident's root cause was recorded.

The contract version stays at 1.3.0: it is pinned by test to the report writer's
schema version, and the report's own shape did not change — only the description
of what its checks are worth.

### 2026-08-26 — Finalize prototype interpretation and follow-up safeguards

Asked to begin the agreed prototype-finalization improvements after updating
from upstream, while changing only the agent codebase and leaving BeXhoma
untouched. Upstream `master` was already fully merged. The newer `dev` branch
was inspected but not merged because it is unreleased and would change
BeXhoma; its relevant additions are an output answer contract and agent-facing
documentation, which are compatible with this implementation.

The interpretation boundary now computes a deterministic TPC-H comparison
quality record from `benchmarking.md`. It reports planned and commonly
successful queries, per-configuration query coverage, whether whole-workload
throughput is comparable, and repetitions whose geometric-mean latency differs
by at least threefold from the median of their peers at the same concurrency.
Such a repetition is marked suspect but is never invalidated automatically.
The model must run this assessment and reproduce its coverage, throughput, and
suspect-phase fields exactly before its structured interpretation is accepted.
This prevents a prose conclusion from silently turning partial query coverage
into a whole-workload win or discarding an inconvenient repetition.

Validation now reports a conservative timeout budget alongside the existing
expanded phase count. It multiplies the declared or catalog-default per-query
deadline by the active-query count, query repeats, and sequential phases, and
adds declared per-configuration loading deadlines. The value is explicitly a
deadline ceiling for comparing designs, not a calibrated runtime prediction.
The TPC-H contract now records BeXhoma's existing 600-second query-timeout
default so an omitted timeout no longer hides this cost from the agent.

Follow-up decisions now record either a focused query list or an explicit need
for the full workload, together with a cost rationale. When a list is chosen,
the authoring gate rejects validation until `workload.params.active_queries`
matches it exactly. Tests cover partial coverage and non-comparable throughput,
the threefold anomaly warning, exact structured interpretation, timeout-budget
arithmetic, rejection and repair of an overly broad follow-up, and preservation
of a concise user question while operational context remains in the system
prompt and contracts.

### 2026-08-25 — Refresh the prototype onto BeXhoma v0.10.10

Asked to stop the failed retry and pull the latest BeXhoma repository before
starting again. Stable upstream `v0.10.10` was merged into the prototype branch
through a recoverable stash because the checkout contained extensive local
agent and loading-safety work. The updated BeXhoma lifecycle and generic
contract engine were retained. Local loading-failure diagnostics remain in the
lifecycle, while loading-timeout translation and stable resource-sweep names
were moved into upstream's new workload-specific TPC-H translator instead of
restoring the superseded generic implementation.

The only upstream-merge conflict was the ignore file, resolved by retaining
both sets of rules. Reapplying local work then required the two adaptations
above. The full maintained test suite passes after integration.

### 2026-08-25 — Reject unsafe benchmarker placement before submission

Asked to keep the BeXhoma resource-template divergence as a local follow-up and
fix the failed retry entirely at the agent boundary. The TPC-H catalog now tells
the agent that each concurrent stream creates one benchmarker Pod whose current
BeXhoma template declares limits of 16 CPU cores and 128 GiB memory. These
limits are independent of `resources.cpu` and `resources.memory`, which continue
to configure only the system under test. An inline contract comment marks the
values as local BeXhoma/cluster settings that must remain synchronized.

When `placement.benchmarking` pins those Pods to a node, agent validation now
multiplies the per-Pod limits by the largest concurrency round and compares the
peak with that node's allocatable CPU and memory. If the system under test is
pinned to the same node, its largest declared limits are added to the peak. A
rejected design receives the computed Pod count, required capacity, available
capacity, and the useful remedies: reduce concurrency or choose a separate,
larger benchmark node. The check deliberately uses limits rather than requests.
Requests answer whether Kubernetes can schedule a Pod; limits describe the
maximum resource envelope that could distort or exhaust a benchmark node.

This fixes the contract gap exposed by the retry, where four benchmarker Pods
could expand to 512 GiB despite a 64 GiB database budget. It does not claim to
identify or repair the original PgDuckDB loader's no-output failure; the loading
deadline and preserved diagnostics documented below are the mechanism for
capturing that root cause on a new attempt.

Known divergence for later: the catalog currently mirrors fixed values from
BeXhoma's benchmarker template. A permanent execution-host change should expose
or derive those component limits from one source so a template edit cannot make
the agent contract stale. That BeXhoma change is intentionally outside this
agent-only implementation.

### 2026-08-25 — Bound loading and preserve failure diagnostics

Asked to expose a BeXhoma loading timeout and failure-log capture to the agent,
which required a narrow change to the execution host rather than prompt-only
instructions. The input contract now accepts an optional loading timeout in
minutes. It is translated to BeXhoma's command line and measured independently
for each resolved system configuration from the moment that configuration
actually begins loading. A configuration waiting for cluster capacity does not
consume the deadline, and omitting the field preserves the previous unlimited
loading behavior.

Failure capture is automatic rather than another opt-in switch. A terminally
failed Kubernetes loader Job or an expired loading deadline stops the
experiment, but only after BeXhoma stores the loader and system-under-test
container logs, Pod descriptions, and loader Job descriptions. The parent Job
description is important because it retains the terminal condition and events
for failed Pods that Kubernetes may already have replaced or garbage-collected.
The same diagnostics-before-teardown rule also applies when loading is stopped
through the existing experiment-wide timeout or another cleanup path.

This deliberately avoids a disable knob: failure diagnostics are part of the
experiment's audit record, and making them optional could discard the only
evidence explaining why a run produced no report. Tests cover contract bounds,
backward-compatible omission, translation, active loading, per-configuration
expiry, terminal Job failure, and capture ordering before deletion.

### 2026-08-24 — Allow either Hopper GPU for the model server

Initially requested H100 placement for the next agent benchmark, then allowed
H200 as well while waiting for capacity. The model-server affinity therefore
admits nodes labelled `gpu: h100` or `gpu: h200`, and the quick start describes
that the scheduler uses whichever compatible GPU becomes available first.

### 2026-08-24 — Use the cluster's shared Prometheus endpoint by default

Asked to apply the endpoint confirmed by the cluster administrator after the
agent benchmark produced no CPU or memory measurements. The working
`cluster.config`, checked-in template, and configuration guide now use
`http://prometheus.monitor.svc.cluster.local:9090/api/v1/` for cluster-level
monitoring. Application monitoring keeps its service and namespace placeholders
because those endpoints belong to each experiment.

The endpoint was checked from the running Bexhoma dashboard pod. It returned
HTTP 200, the node-memory metric used by Bexhoma's health probe, and container
memory series for the active PgDuckDB system-under-test pods.

### 2026-08-24 — Give interpretation prose its own output budget

Asked to address the token-budget risk in requiring the complete study report
inside the structured interpretation call. That call now records only validity,
question coverage, conclusions, and the paths supporting them. Once accepted,
the model writes the self-contained Markdown report in a separate tool-free
turn, so the report does not pay JSON-escaping overhead or compete with the
structured record for the same generated output.

The harness validates the final prose before accepting it. Its title and all
eight required section headings must occur exactly once, in order, with no
additional level-one or level-two headings. A malformed report is returned to
the model for correction within the bounded phase. This preserves the structural
guardrail without trying to judge the semantic correctness of natural-language
inference.

### 2026-08-24 — Add the remaining lean prototype guardrails

Asked to implement the remaining high-benefit review items except automatic
cross-experiment comparability, which was judged beyond the prototype boundary.

Initial design now uses the same design-space gate as follow-up work. It cannot
write a specification before reading the complete catalog and, when present,
the environment descriptor. This turns the initial prompt instruction into the
same auditable enforcement already used later in the loop.

Interpretation now requires successful reads of the exact report index, its
Tests evidence, and the archived result contract before accepting conclusions.
The recorded failed-check count must match report frontmatter; failed checks
require a scope explanation. Every question declares whether its evidence is
supported, limited, or invalid and cites paths actually read in that model
context. A settled question requires supported evidence. The initially shipped
structured report object was replaced by the separate validated prose turn
described above, which reduces generation overhead while retaining the required
section contract. The harness deliberately does not attempt to prove the
semantic correctness of natural-language inference.

Package discovery now includes the agent package and the root-level TPC-H
launcher that its detached submission adapter imports. A built wheel was
installed in a temporary environment outside the checkout; the agent imported,
the launcher was discoverable, and the command-line help ran. Pytest is also
configured to collect the maintained `tests/` directory, avoiding the
executable root-level benchmark script during normal test runs.

### 2026-08-24 — Repair execution-validity defects found by the paper review

Asked to begin implementing the recommended fixes from a comprehensive review
of the agent prototype against the paper. This first batch addresses the three
execution defects that could collapse treatments, submit without checking the
target cluster, or lose the identity of a live experiment.

Resource sweeps now share one stable positional identity between the catalog
translator and the TPC-H configuration builder. CPU-only sweeps and cells that
share a memory request therefore produce distinct configurations and storage
scopes instead of all receiving the same memory-derived name.

Catalog-only validation remains available for an explicit dry run, but it no
longer authorizes submission. The workspace records a submission fingerprint
only after the environment checks have also passed, so a missing descriptor
cannot silently reach Kubernetes.

A detached process that is still alive when the startup wait expires now
returns its preassigned experiment code with `starting` state instead of
raising and losing the code from the phase outcome. The exact specification,
catalog, environment, and result contract are snapshotted before launch and
named in its status file; result discovery archives those snapshots when the
folder becomes observable. Regression tests cover all three paths.

### 2026-08-24 — Restore the configured Kubernetes namespace on every server operation

Requested a portable fix for the model-server and benchmark workflow after a
valid Keycloak token was used with a context that had lost its namespace. The
server wrapper now reapplies `MODEL_SERVER_NAMESPACE` on every invocation,
including when the token is still valid, so namespaced resources do not fall
back to `default`. The agent quick start documents both this environment
variable and the matching Bexhoma cluster configuration setting.

The standard model-server manifest also caps vLLM at 512 concurrent sequences.
The H100 has fewer available Mamba cache blocks than vLLM's default sequence
limit, so this portable cap prevents startup failure when Kubernetes selects an
H100. The agent uses only a small number of concurrent model requests, so it
does not constrain the benchmark study.

### 2026-08-18 — Build the design-and-validate loop, and host a model on the cluster

Asked for the first half of the agent harness: turn a question into an
experiment specification, check it, and let the agent repair it when the check
fails. Asked separately for a self-hosted model to drive it, suggesting a Qwen
model on an H100 or H200.

Delivered the five harness modules listed above, plus the Kubernetes manifest
for the model server, and generated the cluster's environment descriptor so the
placement and resource-ceiling checks have something to check against.

Verified in three layers. The validator envelope, the run-count estimate and the
path policy were checked directly against known-good and deliberately broken
specifications. The repair loop was then driven by a scripted stand-in model, to
confirm that a rejected specification comes back for repair and that a used-up
budget ends the run instead of spending turns on attempts that cannot succeed.
Finally the whole loop was run against the served model on the real question
from the paper, which produced a specification that validated.

Two things were deliberately left out. There is no critic yet, because keeping
it a separate invocation makes it a clean experimental variable and it is not
needed to get the loop working. There is no duration estimate in the verdict,
because estimating one needs an archive of past runs that does not exist yet.

### 2026-08-18 — Keep local cluster facts out of the shared contract

Asked for a gitignored script that adds this cluster's storage-class reality to
the environment descriptor each time it is regenerated, leaving
`bexhoma/environment.py` cluster-neutral.

Delivered `dev/catalog/refresh_environment.py`, which regenerates the descriptor
and then rewrites `excluded_nodes`. It reuses that existing block rather than
adding a field, because the validator already refuses to place an experiment on
anything listed there — so the correction is enforced rather than merely written
down.

It ended up as an allowlist rather than a list of known-bad nodes. Free capacity
cannot be recovered on this cluster at all, with or without the generator, since
every route to it needs cluster-scoped permission to list pods; and the `k8s/`
templates already pin every bexhoma pod to one node, so any other choice the
agent makes would be silently overridden at apply time. Keeping only that node
makes the descriptor agree with what will actually happen.

### 2026-08-18 — Read the contracts through a tool; put the repetitions rule in the catalog

Asked to stop placing the catalog in the prompt and have the agent fetch it, in
line with the interface agreement, and to give the catalog a minimum number of
repetitions rather than relying on the agent to choose well.

Both delivered. The opening prompt dropped from about 6,400 tokens to about
1,200, and the agent now reads the catalog and the environment descriptor itself
on its first turn, with both reads logged by size. The catalog gained
`minimum_for_conclusions` on the workload's `repetitions` field; the harness
enforces it by reading the number from the catalog, and only for experiments that
actually compare configurations. On the next run the agent chose three
repetitions on its own.

### 2026-08-18 — Submission and interpretation, at a smaller size

Asked for the remaining two phases, and for less code: a prototype should not
need nine hundred lines to propose and validate a specification.

Delivered `submit` and `list_results`, and the interpretation phase. Submission
launches bexhoma detached and identifies the run by the result folder it
creates, so nothing has to be parsed out of console output and the agent exits
rather than sitting through the benchmark. Interpretation is a separate
invocation that rebuilds what it needs from the design run's log by rule --
question, specification, experiment code -- and leaves the rejected drafts
behind.

On size: the two phases together added about a hundred and fifteen lines of
code, because both now share one loop. Measured across the package, 581 lines
are code and 396 are docstrings required by this repository's own conventions.

Also fixed a local blocker: `cluster.config` still pointed at a macOS result
path from another machine, so no run could have written results here.

### 2026-08-18 — Explain the harness in plain English, and run it against the cluster for real

Asked two things: a single compact document explaining how the agent works in
simple English, and a genuine end-to-end run rather than another rehearsal.

Delivered `agent/README.md`, which walks through the idea, the three phases, all
five components and what each one is for, what gets logged, and how to run it.
It also corrects two names that misled, and then renamed the modules to match:
`verdict.py` became `validation.py`, because it is the validator used during
design rather than the interpreter, and `llm.py` became `model_client.py`,
because it is only the adapter for one exchange with the model -- the
tool-calling loop lives in `agent.py`. The word "verdict" stays as the name of
the object validation returns, since that is the term the architecture document
and the result contract already use.

The real run exposed two genuine blockers that no offline rehearsal could have
found. Both are cluster-local and neither belongs in a commit.

The first was a silent submission failure. bexhoma invokes `kubectl --context
<ctx> create -f ...` without ever passing a namespace, so it depends on the
kubectl context carrying one. This context had none, so every object was sent to
`default`, where this account has no rights. Nothing surfaced, because the error
sat unflushed in a block-buffered log while the orchestrator polled for a
dashboard that was never created. Fixed by setting the namespace on the context,
which the login script leaves alone, so it survives re-authentication.

The second was placement. Only five of the `k8s/` templates carried the local
pin to the one node where this cluster's shared volumes mount, and the PgDuckDB
deployment was not among them, so that system would have been scheduled where its
storage could not attach. Pinned it the same way as the others.

A third issue is a real gap rather than a local accident. The agent read "10GB
dataset" correctly as scale factor 10 and, with three concurrency levels and
three repetitions across two systems, designed eighteen benchmark runs on
join-heavy queries -- scientifically sound and operationally expensive. The
verdict reports the run count but still returns `null` for duration, so neither
the agent nor the operator saw the cost before it was committed. The run was
stopped and re-asked with a 1GB dataset in the question, and nothing else
changed. The agent moved to scale factor 1 and, unprompted, also cut the
per-query timeout from an hour to five minutes -- it adjusted the design rather
than just the one number that changed in the question. That run was submitted as
experiment 1787066092.

That run completed cleanly in 2,084 seconds: no SQL errors, no result
mismatches, no container restarts, and the pod sweep matched the plan. The
interpretation phase then read it and answered well on the evidence -- it caught
that all four monitoring checks failed and scoped every resource claim out,
recomputed per-query means correctly across a 42-column latency table, and
reported the two systems as a statistical tie.

It also missed the finding that matters. The catalog declares
`duckdb_force_execution`, which routes every query through DuckDB's engine
instead of pg_duckdb's own cost-based routing, and it defaults to false. The
design agent left it at the default, so with heap tables and no forcing the
extension was loaded but idle, and the experiment almost certainly compared
PostgreSQL against PostgreSQL. Neither phase questioned whether the treatment
had been applied, and the follow-up proposed more concurrency rather than
turning the system under test on. This is a clean, reproducible failure of the
agent rather than of the contract: the knob was declared, discoverable, and
described in exactly the terms the question needed.

Fixed one harness bug the run exposed. The first interpretation attempt produced
an empty answer: the model spent its entire per-turn token allowance thinking
and was cut off before writing anything, and the harness wrote the blank result
to disk without complaint. The per-turn ceiling is now larger and settable from
the command line, an empty closing answer is reported as an error instead of
being written silently, and the model's reasoning is now recorded in the
trajectory -- it was being captured and then thrown away, which is what made a
turn truncated mid-thought look like a model that simply said nothing.

### 2026-08-19 — Enforce the contract boundary and complete the prototype loop

Asked to turn the paper review into focused prototype changes: enforce the
catalog instead of trusting the prompt, keep the existing shared resolver out of
the agent implementation, execute through the catalog path, isolate runs,
communicate a 32/64 GiB design when 64 GiB is a ceiling, and let interpretation
execute a follow-up. Also asked to keep the scope appropriate for a vision-paper
prototype rather than expanding it into critic infrastructure and a full
ablation study.

The agent-facing validator now rejects unknown catalog fields and requires the
declared factors to match the system, concurrency, CPU, and memory dimensions
that actually vary. It still delegates resolution and environment checks to the
pre-existing `bexhoma/spec.py`; that file is shared infrastructure, not part of
the agent implementation, and was left unchanged.

Submission is now bound to hashes of the validated specification, catalog, and
environment descriptor. It launches an immutable copy through the
catalog-driven `experiment.py` path with a result code assigned beforehand, then
archives the exact inputs in that result folder. An inherited filesystem lock
serialises agent-started runs on the same result root. The harness rejects a busy
root instead of giving the model a wait tool, because design, execution, and
interpretation are deliberately separate invocations.

The catalog now explains that a resource maximum is a ceiling. When resource
pressure can distinguish rival explanations, it recommends sweeping half the
ceiling and the ceiling and naming that resource as a factor; for a 64 GiB limit
this yields 32 and 64 GiB. This remains experimental judgment available to the
agent, not a universally hardcoded transformation.

Interpretation receives writing, validation, and submission tools while a
follow-up remains. A successful follow-up records its immutable input and exact
code, consumes the budget, and ends the invocation. No critic or ablation
framework was added: those are optional evaluation choices beyond the runnable
vision-paper prototype.

### 2026-08-19 — Consolidate the agent documentation

Asked to document the preceding edits and decisions, identify where the project
actually records documentation, and consolidate overlapping material.

The former `agent/prototype-architecture.md` described a planned mock interface
that no longer matched the implementation, while `agent/design-decisions.md`
mixed current rationale, build history, and stale plans. They were replaced by
`agent/ARCHITECTURE.md`, the single current source for the harness boundary,
state model, decisions, and known limits. `agent/README.md` is now the compact
operator entry point and includes a documentation map.

The broader contract documents were kept separate because they have different
owners: the YAML files are normative machine-readable contracts, their design
documents explain reusable Bexhoma interfaces, and this file remains the dated
repository-wide implementation log. This separation removes duplication without
making historical requests or contract rationale disappear.

### 2026-08-19 — Enforce the numeric bounds the catalog declares

A review found that validation checked which fields may appear but never what
their values were. A specification could name a negative scale factor, a
timeout of zero seconds, query number 99 in a benchmark that defines 22, an
empty query list, zero loader pods, or a CPU request larger than its own limit,
and still be accepted and launched. Three of these bounds were already written
in the contract as `min: 1` and were simply never read, which contradicted the
claim that validation rejects what the contract does not cover.

The field walk now checks each value against the definition it already had in
hand, so every section it visits gained bounds checking without a new call site.
Only `int` and `list[int]` are enforced; the remaining declared types are prose
such as `quantity`, and interpreting them would mean writing a parser for the
contract's own type language. The bounds the contract lacked were added to it:
a positive scale factor, a positive timeout, and query numbers within 1..22. A
separate check rejects a resource request that exceeds its own limit, which
Kubernetes would otherwise refuse only after the run had taken the lock and
deployed pods.

Bounds are read from wherever the contract declares them, so the workload's own
loading block is merged over the schema's shape definition rather than the
`min: 1` values being duplicated into it.

The initial implementation covered only `int` and `list[int]`. The later
primitive-type hardening entry below supersedes that limitation.

### 2026-08-19 — Tell the catalog when forcing DuckDB execution matters

The first live run compared PgDuckDB against PostgreSQL and found them
indistinguishable. The cause was that `duckdb_force_execution` defaults to
false, and on heap-stored tables pg_duckdb's cost-based routing keeps queries in
PostgreSQL's own executor, so the extension was loaded but idle and the run
compared PostgreSQL against itself. The knob was declared and discoverable; the
agent simply had no reason to reach for it, because the contract said what the
knob does but not when it matters.

Its declaration now carries a `when:` clause stating that any hypothesis
comparing PgDuckDB's execution engine to another system must set it, and that
leaving it false is correct only when the routing behaviour itself is under
test. This is a contract change rather than a validator change on purpose: the
specification was legal, and what was missing was the knowledge needed to design
a meaningful experiment rather than a rule that could have rejected a bad one.

### 2026-08-19 — Complete primitive contract checks without replacing the shared validator

A follow-up review confirmed that `bexhoma/spec.py` and
`validate_experiment.py` are Patrick's existing operational validator. The
agent's `validation.py` remains a structured adapter around those functions plus
agent-only methodology; it is not an independent execution validator.

The review also found that malformed nested shapes could crash while the verdict
calculated its run estimate, and that the adapter accepted invalid enum, string,
and boolean values. In particular, `mode: nonsense` passed validation only to
fail in `tpch.py`, while a string supplied for a monitoring boolean was truthy
and could silently enable monitoring.

The adapter now enforces the primitive types already declared by the experiment
schema: integers, strings, booleans, enums, objects, lists, typed integer/string
lists, and object-or-list resource cells. It also enforces declared required
fields. Invalid shapes return a verdict without attempting a run estimate.
Kubernetes quantities, system/profile resolution, command translation, and
cluster-fit checks still go through the existing `bexhoma.spec` implementation.

### 2026-08-19 — Catch a mistyped type in the contract itself

Type checking matches the catalog's `type:` names as exact strings, so a
misspelling switched that field's check off with no warning: `string` for `str`
let a numeric title through, `boolean` for `bool` let an integer through. With
nine enforced type names there were nine ways to write a definition that looked
strict in review and did nothing, which is worse than being visibly loose.

A field definition declaring a type outside the known set is now rejected, and
the message says the catalog is at fault rather than the experiment. The known
set holds the nine enforced types plus `float`, `memory`, `quantity` and
`duration`, which the catalog uses and the resolver owns. This is four lines in
the agent's validator and touches no Bexhoma code; a full schema for the
contract was judged out of proportion to a prototype.

### 2026-08-19 — Dev-only helper to free the GPU during a benchmark

The agent is stateless between phases: design submits and exits, and
interpretation is a fresh process that starts only once results exist. Nothing
needs the model server during the hours a benchmark takes, so holding an H200
for that window wastes shared hardware.

`dev/model_server.sh` releases the server and restores it when the run's report
lands, keeping the weights volume so a restart needs no re-download. It lives in
`dev/` and is deliberately not part of the prototype: it is operator
convenience, and a paper claim rests on the agent's phases being independent,
not on how the model happens to be hosted between them.

### 2026-08-19 — Make a result folder readable by a model that cannot hold it

Asked to run the interpretation phase on the PgDuckDB-versus-PostgreSQL rerun,
the agent failed three times before producing an answer, and the reason was the
interface rather than the model.

bexhoma's report is written for a human with a scrollbar. Its six pages come to
roughly 700,000 tokens against a 65,536-token window: the monitoring page alone
is about 150,000 and the connections page about 475,000. The pages are dense
markdown tables, which tokenise at roughly 1.9 characters per token instead of
the usual four, so they cost more than twice what their size suggests. The agent
opened three evidence pages in its first two turns and overflowed. Halving the
output reservation to buy input room only moved the failure: the model then
spent its entire per-turn budget thinking and returned no closing answer. No
setting of that budget clears both constraints at once.

The result contract already described a three-tier scheme — index first,
evidence pages only when a specific number is needed, raw folder last — and the
agent had read it. But the tiers only ever said *when* to open a file, never how
large it was, and the interpretation prompt never asked the agent to follow them.
The prompt now states the discipline directly and warns that evidence pages come
back cut short. `read_file` caps a single read at 24,000 characters and says in
the reply that it did so, and how long the file really is, so the agent is never
silently blind. The threshold sits above the index page's 19,480 characters, so
tier one always arrives whole while every evidence page is cut.

With both in place the agent opened one evidence page instead of three and
finished. Guidance shapes ordinary behaviour; the cap is the backstop, since one
justified read of the connections page would end any run whatever the window
size. The episode is the clearest evidence so far for the prototype's own claim
that AI-readiness is a property of interfaces, not of intelligence: the agent's
reasoning was sound throughout, and it drowned anyway.

### 2026-08-19 — Separate interpretation, follow-up selection, and authoring

Repeated interpretations after the read safeguards produced identical answers
but consistently declined a useful follow-up. The concise path correctly noticed
that the memory contrast was probably non-binding, yet stopped before consulting
the input catalog; it judged the follow-up from the memory knob in the previous
specification rather than from the supported design space. An earlier, longer run
had read the catalog before deciding and selected a CPU sweep, but then exhausted
the shared model window after validation.

Interpretation now records settled, partial, or unresolved status for every
explicit question in a read-only context. When budget remains, a fresh context
must read the complete catalog and present environment before recording a finish
or follow-up decision. Only an approved follow-up opens a third fresh context
with write, validate, and submit. The cumulative 80,000-character allowance
resets at each context boundary, while validation state survives. This keeps the
large-report safeguards and makes design-space consultation a prerequisite of
the decision rather than an accidental consequence of a long trajectory.

### 2026-08-19 — Keep same-system treatments in separate agent experiments

Asked for a final end-to-end agent run on a new question, preferably including
a follow-up, with the model server released while benchmarks use the cluster.
The first design compared PgDuckDB's forced executor and default routing as two
same-named entries in one specification. Validation counted two treatments,
but a pre-load runtime check showed that Bexhoma reduces repeated DBMS names to
one configuration and applies the force-execution flag globally. Such a run
would look valid while measuring only one arm.

No Bexhoma code was changed. The agent-facing validator now rejects repeated
system names with an actionable instruction to run one treatment first and use
the follow-up budget for the other. A focused regression test covers the exact
forced-versus-routed shape that exposed the gap. This keeps the host manager
untouched while making the agent's accepted design space agree with what the
runtime can faithfully execute.

### 2026-08-20 — Automate the local lifecycle and consolidate final documentation

Asked to verify the standalone lifecycle wrapper, clarify why the definitive
specifications are cluster-bound, replace overlapping pipeline notes with an
annotated visual, and keep only one full agent description plus one quick start.
Also identified that the final agent answer lacked the original question,
hypothesis, experiment history, follow-up rationale, and a structured verdict.

The local wrapper now owns the complete server/design/wait/interpret/follow-up
loop, resumes durable investigations, waits for actual pod deletion, and
retries vLLM startup while shared GPU capacity is unavailable. A live check
confirmed noninteractive login and shutdown; restart correctly remained Pending
when the compatible GPU pool had no free GPU, which is now an automatic wait
rather than a terminal lifecycle failure. Placement accepts either Hopper GPU,
so a packed H200 no longer blocks startup while an H100 is free.

`agent/ARCHITECTURE.md` now contains the single complete pipeline description,
annotated Mermaid flow, module sequence, lifecycle boundary, replay options,
and evidence. `agent/README.md` is the single quick-start guide. The separate
two-sided-contract workflow note was removed after its current material was
merged. The historical answer remains unchanged, but future interpretation
prompts require a self-contained study report with question, hypothesis,
experiments, validity, results, interpretation, follow-up, and verdict sections.
The structured follow-up decision is carried into the final context. A new
investigation now owns one append-only trajectory across design, interpretation,
and any follow-up; phase accounts and submission artifacts remain separate,
while top-level `answer.md` is created only as the final aggregated report.

The original placement is the literal node name `cl-worker36` for the SUT,
loader, and benchmarker. Replaying elsewhere requires target-node substitution
or omission of the optional placement block, followed by validation against a
fresh target environment. The local hard-coded template `nodeSelector` edits
must remain outside the portable repository.

### 2026-08-23 — Let the model server release its own GPU

Asked to finish the in-pod idle-shutdown implementation after the local wrapper
crashed and left vLLM holding a GPU long after the experiment had finished.

The cause was that shutdown lived only in the wrapper's cleanup path, so it
happened only when the wrapper itself was the thing that started the phase. The
last three interpretation phases were launched by hand, so nothing ever asked
for the GPU back. Daemonizing was rejected: it would have survived only a closed
terminal, still lost the GPU to a hard kill or a reboot, and added a lock file,
detachment, log redirection, and supervision for the sake of switching one pod
off. It also keeps the authority over an idle GPU on the operator's machine
rather than in the pod that holds it.

The model server pod is now self-cleaning. A watchdog runs beside the server in
the same container and releases the GPU once nothing has sent a request for
`IDLE_SHUTDOWN_SECONDS` (20 minutes by default, tunable through the pod
environment, zero to disable). It reads the server's own metrics endpoint and
treats both in-flight gauges and monotonic completion counters as use, so
neither a single long request nor a burst of short ones between polls is
mistaken for silence. Unreadable metrics, or metric names a future vLLM does not
publish, keep the server up rather than shutting it down on an unexplained
absence of evidence. The pod's restart policy became `OnFailure`, which lets a
crashed server come back while allowing the watchdog's clean exit to actually
end the pod; every non-idle exit is forced non-zero so only the idle path can
end it. An idle server gets thirty seconds to stop cleanly before the watchdog
forces it down, so a hung serving process cannot defeat the resource release.
Because a finished pod keeps its name, the server switch now clears a
pod that is neither Running nor Pending before applying the manifest, and leaves
a healthy current-generation one alone so an `up` on a live server stays cheap.
An explicit pod-generation annotation makes the one-time replacement of an
older running manifest deterministic, since Kubernetes cannot update a Pod's
command or restart policy in place.

The wrapper additionally converts `SIGTERM` and `SIGHUP` into its normal
interruption path, so a polite kill or a terminal hangup now stops the agent
child and shuts the server down instead of ending the process outright. Prompt
shutdown through the wrapper remains the fast path; the watchdog is the backstop
for every launch the wrapper did not drive.

### 2026-08-24 — Full prototype review, and the three findings acted on

Asked for a verdict on the whole prototype: whether it is still compact and
readable, whether it meets what the paper describes, whether it would run on
another cluster, and what could be refactored. The review found no correctness
bugs, one latent trap, two duplications, and two illustrated-but-unbuilt items
that the contracts already declare as gaps. The first three findings were then
applied.

The tool schema lists are no longer shared between phases. Follow-up authoring
held the very same list object as design, and the dry-run path edited that
object in place to withhold submission, so both names changed together for the
life of the process. Nothing failed in practice, because a design process never
reaches follow-up authoring, but a second call in one process would have
silently disarmed a real run. Authoring now holds a copy, withholding is a
function that returns a new list, and the design phase takes a `dry_run`
argument instead of mutating imported state. Two regression tests cover it, one
of which also covers the previously untested design dry-run path.

A submission that could not be confirmed now says what it actually left behind.
Previously, if the result folder did not appear within the wait, submission
raised a single message and the detached benchmark carried on running, holding
the run lock, with nothing left to interpret it. The wait now distinguishes a
child that exited from one that is still working, and the still-working case
reports the process id and the fact that the lock is held, so the run can be
followed or stopped deliberately. The child is deliberately not killed, since
that would discard real cluster work over a slow start.

Interpretation was split into the three phases it already was. `run_interpret`
had grown to 204 lines carrying three nested handlers, and the rule that a fresh
context must reread the whole design space before acting was written out twice,
once for the follow-up decision and once for authoring. Evidence interpretation,
follow-up decision, and follow-up authoring are now separate functions, the
duplicated rule lives in one `_DesignSpaceGate`, and the orchestrator is 99
lines. Behaviour is unchanged and the existing staged-context tests continue to
pass unmodified.

Left deliberately: the shared conversation loop's parameter count, which reflects
real per-phase differences; the duplicated resource-cell counting and the shape
checker's repetition, both contained and cosmetic; and the personal absolute path
that defaults the result root, which is the single most likely obstacle for
anyone cloning this elsewhere and is recorded here as outstanding.

### 2026-08-24 — Take the result folder from Bexhoma instead of hardcoding it

Asked to fix the last portability item from the review, and whether a relative
path could be used.

The agent and the lifecycle wrapper both defaulted the result root to an
absolute path belonging to this cluster, so a fresh checkout elsewhere pointed
at a directory that does not exist. A relative default would have been no better,
because the value is not the agent's to choose: it has to name the directory
Bexhoma actually writes into, and Bexhoma takes that from the `resultfolder`
entry of `cluster.config` — the file every user already creates as their first
setup step, and the only one the experiment path the agent submits through will
read. The agent now reads the same entry, so the two agree on any cluster
without a second setting. Relative values are supported and resolve against the
repository, which lets a checkout keep its results beside itself; Windows-style
values are normalised the way Bexhoma normalises them. A checkout with no
configuration is told to create one instead of being defaulted anywhere.

Precedence is `--results`, then `AGENT_RESULTS`, then the configured folder,
then a clear error.

The wrapper needed the same directory in order to poll for a report, but it is
run as a script from a subdirectory and so cannot import the agent package. It
now reads each run's directory from the status file the agent already writes at
submission, which is both simpler and stronger: the wrapper observes what the
agent recorded rather than recomputing it, so the two cannot drift. It forwards
`--results` to the agent only when an operator actually overrode it, and its own
`--results` survives as a fallback for status files written before that field
existed. Four new tests cover configured, relative, Windows, absent, and
recorded-directory resolution.

### 2026-08-24 — Make the quick start sufficient for a stranger

Asked whether `agent/README.md` alone is enough for another person or a coding
agent to start an experiment. It was not. Walking it against a clean checkout
found two instructions that fail outright and three per-cluster values it never
mentions.

The agent's model client was not a declared dependency of anything, so following
"install the repository dependencies" produced an environment in which the very
first agent command dies on an import. It is now an optional extra, installed
with `pip install -e ".[agent]"`, so ordinary bexhoma users do not inherit a
package they have no use for. The published metadata was checked to confirm the
extra resolves.

The documented namespace override could not work. The manifest pinned a
namespace on all three of its objects, and the switch applied it without a
namespace flag, so the file's value won while every other command in the switch
looked in the configured namespace instead; kubectl also rejects a conflicting
flag outright. The manifest now pins no namespace and the switch supplies one on
apply, which makes `MODEL_SERVER_NAMESPACE` genuinely decide where the server is
created. Verified against the cluster with a client-side dry run in both a
foreign namespace and the usual one.

Three values remain necessarily per-cluster and are now named where someone will
look: the storage class for the weights volume and the GPU node labels are
commented in the manifest and listed in the quick start, and the OIDC login
helper — which defaults to a script path on this machine only — is documented
with a no-op override for clusters reached through an ordinary kubeconfig. The
GPU-label case is called out specifically because it fails silently: a
mislabelled cluster leaves the pod unschedulable, and startup waits for capacity
by design rather than reporting an error, so the quick start now recommends a
bounded `--server-start-attempts` when first bringing this up somewhere new.

The prerequisites also now create the virtual environment they had been assuming,
and state that `cluster.config` must be copied from the template before anything
runs.

Checked end to end against a checkout containing only committed files: the
prerequisites complete, a relative `resultfolder` resolves beside the checkout,
the design phase proceeds through configuration, catalog, and workspace setup to
the model call, and the quick start's own verification command passes.

### 2026-08-24 — Report an unreachable model endpoint as a setup mistake

Asked to make a wrong `--base-url` read like the harness's other startup errors
instead of a stack trace. It was the one remaining place where an ordinary
misconfiguration surfaced as an unhandled exception from the client library.

The model adapter now converts a connection failure into its own
`ModelUnreachable`, which keeps the client library's exception types inside the
only module that is supposed to know which server is behind the endpoint. The
command line catches it around both phases and prints the same shape of message
as the missing-model and missing-result-folder errors: what failed, which
endpoint, and how to correct it, including the `/v1` suffix that most
OpenAI-compatible servers expect and that is easy to omit. It exits 2, as every
other misconfiguration in that entry point does, and records an `aborted` event
so a phase that never reached the model is still auditable rather than leaving
an empty directory. Timeouts are covered too, being a subclass of the same
failure. One test covers the exit code, the message, and the recorded event.

### 2026-08-24 — The two remaining review refactors

Asked to finish the two tidying items the review had left outstanding. Both are
behaviour-preserving; the existing validation tests cover them unchanged.

The run counter and the repetitions rule each worked out independently how many
systems, resource-sweep cells, rounds, and repetitions an experiment expands to.
They now share one measurement. The duplication had already produced a
disagreement: on an empty sweep list the counter read one cell while the
repetitions rule read zero, which would have made it conclude the experiment
compares nothing and skip its own check. Shape validation rejects an empty list
before either sees it, so this was never reachable, but the two can no longer
drift.

The shape checker was a hundred-line ladder repeating the same three lines
twelve times. It is now five named checks — workload, systems, resources,
declared factors, and the top-level walk that sequences them — none longer than
twenty-eight lines, and the top-level function reads as the list of checks it
performs. Nothing about what is accepted or rejected changed, and the first
error found is still the one returned.

While there, the factor-mismatch error now reports which factors actually
disagree. It had computed exactly that set and then discarded it, leaving the
agent to diff two lists itself in order to repair its specification.

### 2026-08-27 — Put the bexhoma package out of bounds

Asked to record in both instruction files that the bexhoma code base is not to
be modified, and that active work belongs to the agent implementation alone.

The scope section of `CLAUDE.md` and `AGENTS.md` now states this before its
existing rules: `bexhoma/`, the top-level experiment drivers, `k8s/` and
`contracts/` are a fixed external dependency the agent is written against, and
a bexhoma bug that blocks the agent is to be reported with a proposed change
rather than fixed in place without being asked.

The immediate occasion was a genuine bexhoma defect found while looking into
long-lived monitoring pods: stopping without naming an experiment deletes the
cluster-wide monitoring service while leaving its daemon set running, which
strands the collectors and makes the next run redeploy on top of them. Under
the new rule that stays a report, not a patch.

### 2026-08-27 — Double the served context window to 128k

Asked whether 128k tokens is achievable on the H100/H200 model server, and to
raise the setting if it does not put the server at risk.

The served window in `agent/k8s/vllm-qwen38-27b.yml` goes from 65536 to 131072
tokens. Reading the model's own `config.json` off the weights volume settled the
two questions that mattered. Its native position limit is 262144 with plain
rotary encoding and no scaling factor, so 128k needs nothing enabled and loses
no quality. And it is a hybrid: of 64 layers only every fourth is full
attention, the other 48 keeping a fixed-size linear-attention state that does
not grow with sequence length. A full 128k sequence therefore costs roughly
4 GiB of KV cache rather than the ~16 GiB a dense 27B model would need, which
fits the H100's 80 GB many times over and the H200's 141 GB with far more room.

The occasion is that interpretation prompts already reach about 49k tokens,
three quarters of the old window, and the harness aborts a phase rather than
compacting when the window runs out. No other knob changed: concurrency stays
nominal because the agent runs one sequential conversation per phase.

### 2026-08-27 — Merge bexhoma v0.10.12 and adapt the agent to it

Asked to merge the upstream master branch into the prototype branch, review the
differences, and say whether the agent's own code has to change because of them.

Upstream brought two releases. The first adds concurrent-SUT caps to the catalog
contract, so an experiment can state how many systems under test may share the
cluster, with a documented default of one at a time. The second adds YCSB as a
second catalog workload, which means a catalog-driven experiment is no longer
necessarily a TPC-H experiment and each workload now runs through its own entry
script.

Both sides had independently fixed the same defect, where two swept resource
cells that share a memory request collapsed onto one configuration identity.
Upstream's fix names a cell by its position alone; the local one wrapped the same
idea in a shared helper. The merge keeps upstream's version, because the bexhoma
package is a fixed dependency here, and drops the local helper and the assertion
that expected its naming.

Two things in the agent did have to change, both in the module that launches a
validated specification. It no longer passes a concurrency cap of its own, since
the contract now emits that cap for every experiment and restating it would let
the agent's copy drift from the contract's. And it now selects the entry script
from the experiment's workload rather than always calling the TPC-H one, opting a
YCSB run into the resource limits its entry script otherwise ignores — without
this, an experiment the agent is now free to author from the catalog would have
been fed to the wrong parser.

One pre-existing gap surfaced while checking that path, and was closed straight
after in a follow-up request. The agent's launcher never applied per-system
post-load selection, so an experiment asking for indexes on one system but not
another silently got the shared default on both. That choice has no command-line
form, because the index, constraint and statistics switches are global, so the
supported entry point attaches it to the parsed arguments in memory and the
agent's launcher now does the same. A test covers it by giving two systems
different post-load selections and asserting they no longer resolve alike.
