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
| Six-call default validation budget for initial designs and follow-up authoring, with every prior verdict retained in the same model conversation | `agent/harness/agent.py`, `dev/agent_lifecycle.py` | Done and regression-tested |
| Catalog, shape, environment, and methodology validation | `agent/harness/validation.py`, `contracts/contract_catalog.yml` | Done |
| Experiment design handbook: navigable chapters of methodological guidance, read from its Navigation chapter at design and follow-up authoring, hashed into provenance, with its four decidable principles enforced and cited by identifier | `agent/experiment_design_handbook.md`, `agent/harness/agent.py`, `agent/harness/prompts.py`, `agent/harness/validation.py` | Done and regression-tested |
| Handbook switched off in one setting, for the with/without ablation | `agent/harness/agent.py`, `dev/agent_lifecycle.py`, `.env.example` | Done and regression-tested |
| Handbook reachable and required during interpretation: named chapters must be read before a verdict may be recorded, and a renamed chapter is dropped rather than demanded | `agent/harness/agent.py`, `agent/harness/prompts.py`, `agent/harness/tools.py` | Done and regression-tested |
| Cluster session renewed at submission time, after the phase that can run long | `agent/harness/submit.py`, `.env.example` | Done and regression-tested |
| Full coverage of the parameter types the catalog declares, including YCSB's throughput sweeps | `agent/harness/validation.py` | Done and regression-tested |
| Phase-scoped tools, path policy, immutable submission, and deterministic query comparison | `agent/harness/tools.py` | Done |
| Exact one-result selection, link-reachable evidence reads, and result-contract answer structure | `agent/harness/prompts.py`, `agent/harness/tools.py`, `contracts/contract_result.yml` | Done and regression-tested |
| Model adapter with single-model endpoint discovery for portable server naming | `agent/harness/model_client.py` | Done and regression-tested |
| Per-turn output sized to the served context window, with an exhausted window reported like other setup errors | `agent/harness/model_client.py`, `agent/harness/agent.py` | Done and regression-tested |
| Design, one-result interpretation, bounded follow-up authoring, durable lineage, phase reports, standalone `--report` operation, and CLI | `agent/harness/agent.py` | Done and regression-tested |
| Human-readable completed-investigation names containing scale factor and served model | `agent/harness/agent.py`, `agent/trajectories/` | Done and regression-tested; incomplete designs remain timestamp-only, and so does a completed design on Windows when the running Bexhoma child locks the directory against rename |
| Phase completeness decided by work done, not by closing prose: a submitted (or dry-run-validated) design succeeds even when the model returns an empty final message, with a substituted plain-sentence report | `agent/harness/agent.py` | Done and regression-tested |
| Finish reason and per-turn generation budget recorded on every assistant turn, and a turn truncated at the token ceiling with nothing to show re-prompted for a decisive step instead of ending the phase | `agent/harness/model_client.py`, `agent/harness/agent.py` | Done and regression-tested |
| Model server manifest with idle GPU release | `agent/k8s/vllm-qwen38-27b.yml` | Done |
| Durable Kubernetes lifecycle controller with in-cluster authentication and restart recovery | `agent/lifecycle_controller.py`, `agent/k8s/lifecycle-controller.yml`, `agent/Dockerfile.lifecycle` | Done and regression-tested; image publication and target-cluster values remain deployment steps |
| Sequential isolation of agent-submitted SUT configurations | `agent/harness/submit.py`, `contracts/contract_catalog.yml` | Done and regression-tested through BeXhoma's public one-SUT option |
| Result-contract disclosure of unverified loading and of the warnings check's real scope | `contracts/contract_result.yml`, `docs/AgentResultContract.md` | Done |
| Result root taken from Bexhoma's `cluster.config` | `agent/harness/tools.py` | Done |
| Environment refresh with local cluster facts | `dev/catalog/refresh_environment.py` (gitignored) | Done |
| Repeated same-system treatments rejected before Bexhoma collapses them | `agent/harness/validation.py` | Done and regression-tested |
| Distinct identities for every CPU or memory resource-sweep cell | `bexhoma/spec.py`, `tpch.py` | Done and regression-tested |
| Resolved resource configurations reported on every validation verdict, and factors that never vary alone refused as unattributable | `agent/harness/validation.py`, `agent/harness/prompts.py` | Done and regression-tested |
| Per-configuration CPU and memory reported beside the result assessor's coverage figures | `agent/harness/tools.py` | Done and regression-tested |
| Component-aware peak resource validation for pinned benchmarker placement | `contracts/contract_catalog.yml`, `agent/harness/validation.py` | Done and regression-tested; mirrors the current BeXhoma template limits |
| Stable upstream BeXhoma integration | repository history, `bexhoma/experiments/tpch_catalog.py` | v0.10.10 merged; local agent and loading safeguards preserved and regression-tested |
| Environment-checked submission gate and recoverable slow-start state | `agent/harness/tools.py` | Done and regression-tested |
| Agent-exposed per-configuration loading timeout and automatic failure diagnostics | `contracts/contract_catalog.yml`, `bexhoma/spec.py`, `bexhoma/experiments/base.py`, `bexhoma/configurations/lifecycle.py` | Done and regression-tested |
| Enforced initial catalog/environment consultation | `agent/harness/agent.py` | Done and regression-tested |
| Validity-first evidence gate, read-path citations, and result-contract-driven answer | `agent/harness/agent.py`, `agent/harness/tools.py` | Done and regression-tested |
| Deterministic query coverage, throughput comparability, and repetition-anomaly disclosure | `agent/harness/tools.py`, `agent/harness/agent.py`, `agent/harness/prompts.py` | Done and regression-tested without changing BeXhoma |
| Workload-independent result characterization for every declared system, concurrency, CPU, and memory factor across every throughput and latency metric, with variance-aware typed shapes, rankings, and failed-check scope enforced before interpretation is accepted | `agent/harness/tools.py`, `agent/harness/agent.py`, `agent/harness/prompts.py` | Done and regression-tested without changing BeXhoma |
| Conservative timeout-cost estimate and enforced focused-query follow-ups | `agent/harness/validation.py`, `agent/harness/agent.py`, `agent/harness/prompts.py`, `contracts/contract_catalog.yml` | Done and regression-tested |
| Exact `follow_up_of` lineage and rejection of execution-identical follow-ups | `agent/harness/agent.py` | Done and regression-tested without changing BeXhoma |
| Portable per-experiment hypothesis verdict and compact ancestor memory for follow-up authoring | `agent/harness/agent.py`, `agent/harness/prompts.py`, `contracts/contract_result.yml` | Done and regression-tested without changing BeXhoma |
| Installable agent and TPC-H launcher package | `pyproject.toml` | Done and wheel-smoke-tested outside the checkout |
| Maintained-suite test discovery | `pyproject.toml` | Done; plain `pytest` runs `tests/` |
| Local server/benchmark lifecycle, retry, resume, signal-safe cleanup, namespace restoration, restart of a self-finished pod, and exact failed-experiment cleanup | `dev/agent_lifecycle.py`, `dev/model_server.sh` | Local-only; unit- and cluster-checked |
| Windows PowerShell port of the low-level model-server switch (`up`/`down`), behaviour-for-behaviour with the shell version, selected automatically by the lifecycle wrapper on Windows | `dev/model_server.ps1`, `dev/agent_lifecycle.py` | Local-only operator helper; parse-, usage-, and unit-checked |
| Unattended phase chaining for endpoints we do not host, including hosted APIs and a local Ollama | `dev/agent_lifecycle.py`, `.env.example` | Done and regression-tested |
| Secret-safe model credential handoff from the lifecycle wrapper to agent phases | `dev/agent_lifecycle.py`, `tests/test_agent_lifecycle.py` | Done and regression-tested; `.env` remains local and the key is absent from child command lines |
| Collision-safe experiment-code allocation for parallel submissions | `agent/harness/tools.py`, `tests/test_agent_harness.py` | Done and regression-tested |
| Configuration that rejects a typo instead of failing open | `dev/agent_lifecycle.py`, `agent/harness/agent.py`, `dev/model_server.sh` | Done; `AGENT_MODEL_SERVER` and `AGENT_METHOD` regression-tested, the account-free `MODEL_SERVER_NAMESPACE` checked against a stubbed kubectl |
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
the shell has not already exported them. The same file carries the two settings
that decide how a run is conducted rather than who answers it:
`AGENT_MODEL_SERVER`, which says whether the wrapper starts and stops that pod
or leaves an endpoint it does not own alone, and `AGENT_METHOD`, which names the
experiment design handbook and, left empty, designs without one. A fourth,
`AGENT_INTERPRET_MODEL`, names a separate model for the interpretation phase, so
the verdict can be read by a larger model than the one that designed the run;
left unset, both phases use `AGENT_MODEL`. Both phases still share one endpoint
and one key, so the override selects a different model from the same provider. An exported
variable overrides the file, and the corresponding command-line flag overrides
both. `.env.example`
documents a block per backend — the bundled vLLM server through a port forward,
the same server by its in-cluster service name, a local Ollama, OpenAI, and
Mistral — and `.env` itself is gitignored so keys stay out of the history. The
loader is `python-dotenv`, added to the `agent` extra alongside the OpenAI
client.

Three adjustments in the model adapter make a hosted endpoint usable in place of
the self-hosted one. Before the first prompt, a dedicated endpoint's sole
advertised model identifier replaces a stale configured alias; a multi-model
endpoint still requires an exact match. This prevents a server implementation's
naming choice from breaking an otherwise portable deployment. The context-length
probe accepts either spelling a server
publishes it under (`max_model_len` for vLLM, `max_context_length` for
Mistral), so the per-turn budget guard keeps working off the cluster. And a
turn refused for rate limiting is retried with a doubling wait, honouring a
`retry-after` header when one is sent, before the phase reports the endpoint as
unusable. A self-hosted server queues requests rather than refusing them, so
this engages only against a metered API, where a per-minute quota would
otherwise end an investigation mid-design.

### Trajectory provenance

Each phase records the model, its sampling parameters, the digests of the
catalog, result contract and cluster descriptor it read, and the harness itself
— the commit at HEAD plus a fingerprint of the harness sources, so an
uncommitted edit to the validator or the prompts is visible in the record. Two
trajectories are comparable only when both the model and that fingerprint are.

### Concurrency between agent runs

An agent-started experiment holds an exclusive lock on the result root for as
long as it benchmarks, so a second run refuses to submit. The lock expresses a
measurement policy rather than a filesystem need — BeXhoma already isolates
every experiment in its own code-named directory — and `--allow-parallel-runs`
on the agent CLI lifts it for one run. The submitted run then records in its
trajectory that it started alongside another, so the timings are never read
later as if the cluster had been quiet. Because that lifted lock is the one
situation in which two submissions can allocate a code at once, the experiment
code is reserved atomically: the status file is created exclusively, so of two
runs racing for the same rounded second exactly one wins it.

The lock itself (`agent.harness._runlock`) records the holding process's PID
in the lock file rather than relying on an OS advisory lock handed down to the
detached child, because Windows' `subprocess.Popen` has no equivalent of
POSIX's `pass_fds` to inherit one. "Locked" means the recorded PID is still
alive, checked through `os.kill(pid, 0)` on POSIX and `OpenProcess` on
Windows; a short-lived same-process lock (`fcntl` on POSIX, `msvcrt` on
Windows) only brackets the read-check-write around that PID, so two runs
claiming at the same instant cannot both succeed. This is what makes the
`agent/` harness runnable from a Windows workstation as well as Linux.

---

## Part 2 — Request log

### 2026-09-01 — Recover a turn cut off while the model was still thinking

A design phase for a pg_duckdb-versus-PostgreSQL join question ran out of turns
having submitted nothing, and the user asked whether a timeout was to blame and
whether more could be logged. It was not a timeout. The model's second turn was
truncated at the token ceiling while it was still inside its hidden reasoning
channel: it came back with no tool call, no visible text, and a reasoning trace
that stopped mid-sentence. The conversation loop treats any turn with no tool
calls as the model's closing answer, so a single truncated think-only turn ended
the whole phase before any specification was written. The eight minutes between
turns was just generation time for forty thousand reasoning tokens, well under
the ten-minute client timeout.

Two things now make this visible and recoverable. The model adapter records the
server's finish reason and the token budget the turn was actually given — the
budget is the served context window minus the conversation size, not the
configured ceiling, which is why raising `--max-tokens` would not have helped
here. And the conversation loop now recognises a turn that ended for length with
nothing to show: instead of accepting the empty turn as an answer, it tells the
model its last turn was cut off and asks it to be decisive, then spends another
turn. The per-phase turn ceiling still bounds the loop, so a model that truncates
every turn still terminates rather than looping forever.

### 2026-08-29 — Name the hardware each configuration ran on

Asked to carry the resource labels next to the measurements, after a failed
interpretation showed why their absence matters. Bexhoma labels its
configurations `postgresql-1`, `postgresql-2` and so on, and neither the key
metric table nor the per-phase table says what hardware each of those labels
received; the only place the mapping exists is the connections page, whose name
does not announce that it holds the answer. The interpreting model never opened
it. Holding a question about three hardware scenarios and a table of two
unlabelled configurations, it assigned the labels itself, and its verdict
compared a machine that had never been built while calling the machine that had
run untested.

The result assessor already decoded that mapping internally, to decide which
factors its typed claims can support, but it kept the answer to itself. Each
entry of its per-configuration coverage record now carries the CPU and memory
that configuration ran with, written the way the specification wrote them, so
the mapping arrives in the same reply as the coverage figures that use those
same labels. Where the archived specification is missing or a label does not
decode, the field is reported as null rather than guessed, since a wrong
mapping is worse than an absent one. The resolution reuses the same pairing
function validation uses, so what a design was told it would run and what the
assessor says it did run cannot drift apart.
### 2026-08-29 — Run the Bexhoma cleanup command through the interpreter, not the installed wrapper

A local lifecycle run on Windows reached a benchmark that Bexhoma marked failed
and tried to remove its cluster resources, but crashed with
`FileNotFoundError: [WinError 2]` before running anything. The wrapper located
the `bexperiments` command by taking the running interpreter's path and
swapping the final component for `bexperiments`. That is where `pip` puts the
console script on Linux, but on Windows console scripts go into a `Scripts\`
subdirectory and carry a `.exe` suffix, so the path the wrapper built named a
file that does not exist.

The cleanup call now runs the same code the console script runs — Bexhoma's
`manage()` entry point — through `python -c`, using the interpreter already
running the wrapper. This is the pattern the harness uses everywhere else it
starts a child (`sys.executable` with `-m` or `-c`), needs nothing on `PATH`,
and does not depend on where or under what name `pip` placed the wrapper. The
one test that pinned the old path now pins the new command line.

### 2026-08-29 — Do not fail a design phase on a denied directory rename

A design run on Windows submitted its experiment successfully — the detached
Bexhoma child started and the experiment code was assigned — but the phase then
crashed with `PermissionError: [WinError 5]` while renaming its own trajectory
directory to add the scale factor and model name to it.

The rename is denied because the detached Bexhoma child inherits the handle to
the `bexhoma.log` file that lives inside that directory and keeps it open for
the whole benchmark, and Windows refuses to rename a directory that another
process has a handle into. POSIX allows the move, which is why this never
surfaced before. The directory label is cosmetic, and a timestamp-only
directory is already a documented, resumable state, so the rename is now
best-effort: a failed rename records an `investigation_label_skipped` event and
the phase carries on and exits successfully with the timestamp-only directory,
exactly as it already did when the target name was already taken. On Windows a
completed design therefore keeps its timestamp-only name; on POSIX nothing
changes. A unit test drives the denied-rename path.

### 2026-08-29 — Provide a PowerShell version of the model-server switch

Asked for a PowerShell version of `dev/model_server.sh`, the shell helper that
brings the self-hosted vLLM model server up or down. The shell script depends on
tools that are not present on a Windows workstation — `setsid`, `nohup`,
`pkill`, and a POSIX shell — so running it under Git Bash there fails partway
through rather than cleanly.

`dev/model_server.ps1` is a behaviour-for-behaviour port. It keeps the same two
verbs, the same environment-variable overrides (`MODEL_SERVER_CONTEXT`,
`MODEL_SERVER_NAMESPACE`, `MODEL_SERVER_PORT`, and the rest), the same login
refresh before every operation, the same replace-if-stale rule for a pod left in
a finished or older generation, and the same wait loop that does not return
until the endpoint answers a `/models` request. The three POSIX-only pieces are
replaced with native equivalents: the detached port-forward is started with
`Start-Process` writing to a log file under `%TEMP%`, the port-forward is torn
down by matching `kubectl` command lines through `Win32_Process` instead of
`pkill`, and the health check uses `Invoke-WebRequest` instead of `curl`.

Running `dev/agent_lifecycle.py` on Windows with `AGENT_MODEL_SERVER=bundled`
then failed anyway, because the wrapper always started the switch with `bash`,
which a Windows workstation does not have. The wrapper now chooses the switch
script by platform — the PowerShell port on Windows, the shell script
elsewhere — and picks the interpreter from the script's suffix, so a `.ps1`
switch runs through `powershell` and a `.sh` switch through `bash`. The
in-cluster lifecycle controller is on Linux and is unaffected. A unit test
covers the PowerShell path; the existing shell-path test is unchanged.

### 2026-08-28 — Do not fail a design phase that submitted an experiment

A design run submitted a YCSB-on-PostgreSQL experiment successfully — the
detached BeXhoma child started, the result folder appeared, and the experiment
code was recorded — but the phase still exited with a failure, reporting that
it had "submitted no experiment" and quoting a methodology refusal from an
earlier validation attempt that a later attempt had already fixed. The user
asked whether Windows process-watching was at fault. It was not: the submission
path worked end to end.

The real cause was that a reasoning model spent its entire per-turn token
budget on the hidden thinking channel when asked for its closing account, and
returned an empty visible message. The command-line entry point decided whether
a phase was complete by requiring that free-text summary to be non-empty, so an
empty summary forced the phase to "incomplete" even though an experiment code
existed. That path then skipped the investigation-labelling step, wrote an
empty phase report, and printed a misleading explanation.

Completeness of a design phase is now decided by its actual work: an experiment
reached the cluster, or — under `--dry-run` — a specification passed
validation. `run_design` records this as `phase_complete`, mirroring what the
interpretation phase already did. When the closing message is empty but the
phase is complete, the harness now substitutes a short plain-sentence account
of what was submitted so the report is not blank, while still printing the
"raise --max-tokens" warning. Separately, the helper that explains why an
incomplete phase stopped no longer cites a refusal that a subsequent successful
validation superseded; it now says plainly that a specification passed but was
not submitted before the phase ended.

### 2026-08-28 — Make the agent harness run on Windows

Asked to make the `agent/` folder runnable under Windows: conform to its path
syntax and replace `fcntl`, which does not exist there, with something that
does. Told to keep the change as small as possible, and separately that the
harness must also work with files that live at UNC paths
(`\\server\share\...`), since a Windows workstation reaches network storage
that way.

`fcntl.flock` was used for exactly one thing: keeping a second agent-started
benchmark from submitting while an earlier one still runs. That guard relied
on a Windows-incompatible trick to survive the handover to a detached BeXhoma
child — the locked file descriptor was passed into the child via
`subprocess.Popen(pass_fds=...)`, which Windows' `Popen` does not support at
all. A literal swap of the locking primitive could not fix that half of the
mechanism, so the guard was redesigned rather than patched: the shared
`agent.harness._runlock` module now records the holding process's PID in the
lock file, and "locked" means that PID is still alive, checked with
`os.kill(pid, 0)` on POSIX and the Win32 `OpenProcess` API on Windows. A
short-lived, same-process lock — `fcntl` on POSIX, `msvcrt` on Windows — only
brackets the read-check-write around that PID, so two runs claiming at the
same instant cannot both succeed. Both call sites that used the old
descriptor-inheritance trick (`Workspace.submit` and the in-cluster lifecycle
controller's resume path) now claim the lock before launching BeXhoma and hand
it to the child's real PID once the process exists, and both were previously
tested by directly `flock`-ing the lock file to simulate a held lock; those
tests now write the test process's own (guaranteed-live) PID into the file
instead, which works the same way on either platform.

A second, unrelated instance of the POSIX-only liveness check
(`os.kill(pid, 0)` used as "is this PID still running") turned up in
`Workspace.list_results` and, once pointed out, in `dev/agent_lifecycle.py`'s
own watchdog. Both now use the same cross-platform check.

The rest of the folder's path handling needed no change: every path in
`agent/` already goes through `pathlib.Path`, whose `resolve()` and
`is_relative_to()` already understand UNC roots the same way they understand
drive letters, so the containment checks that scope what the model may read
and write keep working unchanged. The one place that hand-parses a path string
— reading BeXhoma's own Windows-path normalisation of its configured result
folder, so the agent agrees with BeXhoma about where results land — mirrors
BeXhoma's behaviour deliberately and was left as is.

### 2026-08-28 — Reflect back what a resource sweep actually resolves to

Asked to build the reflection step, after a live design run walked into a
confound the harness could not see. The investigation had been given a
right-sizing question: a reporting job runs on sixteen cores and sixty-four
gibibytes, finance wants to halve the machine, and the answer has to say which
of the two resources the job actually depends on. The agent reported that it had
built a two-by-two factorial design, meaning all four combinations of the two
settings, and named each of the four machines in its summary. What it had
written was a list of two core counts beside a list of two memory sizes, and
those lists are paired by position rather than crossed, so the specification
resolved to two machines and not four: the full-size one and the halved one,
with both cuts applied together and neither applied alone. Nothing in the
validation objected, the benchmark ran, and no measurement it produced could
attribute a slowdown to either resource.

The existing rule that the declared factors must be exactly the varied ones was
satisfied, because both resources genuinely varied. What was missing is that
varying two factors in lockstep isolates neither. Validation now resolves the
sweep the way Bexhoma resolves it and checks, for every resource factor the
specification declares, that some pair of resolved configurations differs in
that factor alone. When none does, the design is refused as unattributable
against handbook rule M2.1, and the refusal prints the configurations it
resolved to, so an author holding the wrong picture of four machines sees the
two that will actually run. Both repairs are named: repeat entries in both lists
until every combination appears, which does give the full factorial, or sweep
one resource here and the other in a follow-up.

The resolved configurations are now reported on every verdict rather than only
on a refusal, since an author who believes the lists cross has no other way to
find out that they pair, and the design prompt says to read them back. Only
these two resources need the check: systems and concurrency levels are crossed
with the resource sweep by construction, so neither can move in lockstep with
anything. The check is static and costs no cluster time, which is the point —
the run that prompted it had already spent an hour proving nothing.

Amended 2026-08-29, on the objection that a refusal must not be worded for
the run that prompted it. The message had illustrated the repair with the
very core counts and memory sizes this task asks about, which a refused
author could copy without understanding the pairing, and which would have
made the next attempt at the same question meaningless as a test. The
example is now stated as a shape rather than as values: two levels of each
resource need four entries in both lists, one alternating and the other
changing every second entry. Nothing else about the check was task-specific,
since it reads whatever the specification declares and prints whatever it
resolves to.

### 2026-08-28 — Refuse to run the model server in a defaulted namespace

Asked how the short vLLM block in `.env` knows it belongs to the `lliu` account,
whether another person using it would fail, and then to make the namespace fail
loudly when it is unset, portably.

The endpoint in `.env` carries no identity at all. `http://vllm-qwen38-service/v1`
is an unqualified Kubernetes service name, and Kubernetes resolves such a name
against the namespace of whatever pod is looking it up, so the same three lines
mean a different server depending on where the caller runs. The account entered
through four other places instead: the kube context, the namespace declared in
`cluster.config`, the login command in `AGENT_CLUSTER_LOGIN`, and one default in
`dev/model_server.sh`. The first three are gitignored or carry placeholders in
their tracked templates, which left the switch's default as the only account
name in shipped code.

That default was worse than a wrong address, because the switch writes the
namespace into the caller's kube context before using it. A colleague who never
set the variable would have had their context repointed at this account for the
rest of the session, and bexhoma issues its object creation without naming a
namespace, so the benchmark itself would have followed the model server there —
succeeding and displacing a running pod where the account had write access, and
failing confusingly where it did not.

`MODEL_SERVER_NAMESPACE` is now required. The switch checks it before its first
kubectl call and exits with a message naming the three ways it can be supplied,
so neither `up` nor `down` can touch a cluster without it. Portability was
already most of the way there: the in-cluster lifecycle controller reads the
Job's own namespace from the downward API and passes it down, so that path never
sees the error, and the manifests still declare no namespace of their own. What
was missing was the local path, where `.env` now carries the value and the
lifecycle wrapper hands it to the switch through the environment it already
loads. The example file lists it commented out, so an unedited copy triggers the
new message rather than guessing.

### 2026-08-28 — Review the arithmetic gate and repair what it got wrong

Asked to review the result-characterization change for whether it fixes the
wrong verdict, and to correct anything over-engineered, hardcoded, or specific
to the one experiment that failed. The architecture held up: keying the
characterization to the contract's own `discriminates` vocabulary covers every
experiment the contract can express, the factorial handling holds peer factors
fixed correctly, and every degraded path fails closed rather than inventing a
claim. Four repairs followed.

The shape classifier decided plateaus against a fixed five percent of the mean
while ignoring the repetition spread it had already computed. On the incident's
own data the 16-client level ranged over 14,023 around a mean of 22,059, so the
boundary sat far inside the noise. Resolution is now derived per level from its
repetitions, floored at five percent, and a step counts only when it clears the
combined resolution of both ends. The incident still classifies as
`rises_throughout`; a step inside its own spread is now reported as no movement.

Only throughput was characterized, although the question that started this asked
where response time begins to suffer. Every throughput and latency column is now
characterized, each tagged with the direction that is an improvement, and the
shape vocabulary was made descriptive rather than evaluative so it reads
correctly in both directions.

Requiring the model to retype the computed means was the one genuinely
over-engineered part: four hundred bytes of digit-perfect floating point for the
simplest single-factor case, which is what had pushed the validation budget from
three attempts to six. The model now records the conclusion only, the harness
files the measurements itself, and the budget is back to three.

The claim builder was one 177-line function doing four jobs; it is now five
functions of at most 67 lines. The factor-unit lookup degrades instead of
raising when the vocabulary grows, and the deliberate coupling between the
validity scoper and Bexhoma's English check labels is documented where it lives.

### 2026-08-28 — Make interpretation claims checkable against the measurements

Asked to verify the erroneous first interpretation in investigation
`20260828T094350918414-sf1-mistral-small-2603`, assess a proposed deterministic
repair, and implement the parts that hold up. The repair had to generalize
across experiment types instead of replacing the YCSB blind spot with another
workload-specific rule.

The diagnosis is confirmed. Mean throughput across the three repetitions was
2,012.98, 2,779.54, 6,153.67, 14,873.10, 22,058.87, and 53,580.99 operations
per second at 1, 2, 4, 8, 16, and 32 clients. It rose at every tested level;
the 32-client mean was 2.429 times the 16-client mean. The accepted verdict
nevertheless called the latter increase a plateau, marked the hypothesis
supported, and submitted an 18–28-client follow-up to locate a saturation point
the experiment had not observed. The single failed check was also narrower
than the interpretation's attention implied: one SUT CPU monitoring cell was
zero in phase `postgresql-1-3-6-1`, one of eighteen benchmark phases, while the
throughput and latency measurements remained in scope.

The existing deterministic assessor now derives dimensions from the archived
`discriminates` declaration and the report's summary table, never from a
workload name. It handles all four factors the contract permits. Concurrency,
CPU, and memory produce ordered series with the other declared factors held
fixed; system produces a categorical ranking at each fixed context. Every
throughput and latency column the table carries is characterized separately and
tagged with the direction that counts as an improvement, so a question about
response time is grounded in the same way as one about throughput, and a
system ranking on a latency metric puts the fastest system first. Each ordered
series reports repetition mean, minimum, maximum, spread, resolution, the ratio
from the highest tested level, marginal metric gain per added factor unit, a
shape, and a turning level only when the data establish one. A report that
cannot expose a declared factor names it as unsupported rather than inventing
an order or blocking the rest of the interpretation.

Shapes are decided against each level's own repetitions rather than a fixed
tolerance. A step is movement only when it exceeds the combined resolution of
the two levels it joins, where a level's resolution is half its observed
repetition range, floored at five percent of its mean so that a single
repetition cannot claim perfect precision. This matters on real data: the
incident's 16-client level had a 14,023 spread around a 22,059 mean, so a
five-percent rule was deciding shapes inside its own noise. The vocabulary is
descriptive rather than evaluative -- `rises_throughout`, `falls_throughout`,
`saturates_at_level`, `reverses_beyond_level`, `flat`, `non_monotone` -- because
a latency series that rises throughout is bad news while a throughput series
that does is good.

The interpretation record now carries a typed projection of those results. The
model records the conclusion alone: the shape and its turning level, or the
system ranking. It is never asked to copy the measurements back, because the
harness already holds them and files them with the record, so requiring the
transcription would only cost a repair round per slipped digit. The harness
checks every factor, context, metric, shape, turning level and ranking against
the computed characterization, and its refusal returns the expected and claimed
records together. A regression test recreates the incident:
`saturates_at_level` at 16 clients is refused against a 26,000 to 54,000
operations-per-second rise, and the corrected `rises_throughout` record is
accepted. Separate coverage proves the same parser on an unknown future
workload name, on combined system-and-memory factors, on latency columns, and
on a step that sits inside its own repetition spread.

Failed-check scope is part of the same deterministic response. For monitoring
failures, the assessor follows the failed Tests row to the matching monitoring
table, lists zero or non-finite phase rows, counts them against all benchmark
phases, and records whether throughput or latency is affected. The model must
copy the affected phase list and the performance-scope Boolean into its record.
This gives validity and findings symmetrical, typed attention without adding a
second model or a per-workload checker.

The Universal Scalability Law was evaluated but not added. It is an appropriate
two-parameter model for controlled throughput-versus-load data, but this run's
unconstrained fit gives a negative coherency coefficient; enforcing the model's
non-negative physical coefficients puts the coherency term at zero and yields
no finite peak. The unusually wide 16-client spread further makes a numerical
peak estimate false precision. The deterministic result can soundly say that
no peak was observed in range; a USL fit should wait for data that identify its
parameters and should remain specific to concurrency claims. Hypothesis
blinding was likewise not added: doing it honestly needs a staged reveal or a
separate interpretation context, while merely moving the same prediction lower
in one prompt is not blinding. The arithmetic gate addresses the demonstrated
failure directly and makes a later blinding experiment measurable.

### 2026-08-28 — Give design validation six attempts and audit wasted calls

Asked to raise the default validation budget from three calls to six, confirm
whether a repair sees the preceding rejection without overfilling the model's
context, and inspect the failed investigation for incorrect handbook headings
and other invalid calls. No catalog or handbook values were to be removed as a
shortcut.

Both the direct agent command and the lifecycle wrapper now default to six
validation calls. Initial design and follow-up authoring already share the same
bounded conversation loop, so each validation verdict remains in the model's
message history in full; only the trajectory copy removes large file contents.
The failed verdicts are small beside the catalog, environment and selected
handbook chapters. In the inspected Mistral run, prompt use reached about 21,700
tokens after three validations, leaving enough room for three further concise
repair cycles under the served context limit. Explicit `--attempts` values
continue to override the default.

The heading audit found eighteen failed reads of the current handbook, all from
`mistral-small-2603`. After opening `## Navigation`, that model repeatedly
treated the chapters listed inside it as child sections and guessed headings
such as `### M1. The claim`; the chapters are sibling `##` sections. Each
refusal returned the exact available headings and the model then corrected
itself. Those reads spent turns and context but did not spend validation calls.
The failed design also wasted one real validation on a file that the earlier
read-before-write gate had refused to create, then used its other two checks on
`local-hdd` and unavailable literal `ssd`. The retry increase is shipped here;
the contracts and Markdown selector retain their existing values and exact
heading semantics pending a separate decision about making section lookup more
forgiving.

### 2026-08-28 — Run the verdict on a larger model than the design

Asked, after an interpretation contradicted its own results table, to look
through the sibling `spektrum-news` repository for larger models, check which
were actually reachable, and put one behind the verdict.

Five providers are configured there. Cerebras, Groq, NVIDIA NIM and OpenRouter
all authenticate; the Mistral key in that repository is out of credit. Probed
with a tool-calling request carrying the six throughput measurements the failed
interpretation misread, OpenRouter's `nemotron-3-ultra-550b-a55b:free` answered
correctly but took longer than five minutes for a single turn, which no
twenty-turn phase can absorb. This repository's own Mistral key turned out to
serve the large models as well, so `mistral-large-latest` — the fallback model
that same sibling repository already names — is the one integrated: a larger
model reached through the endpoint and key that are already configured, with no
second provider's credentials copied into this repository.

The wrapper gained `--interpret-model`, defaulting from
`AGENT_INTERPRET_MODEL`, and passes it as a second `--model` after the base
command's own when it invokes an interpretation; argparse keeps the last one it
parses, so the design phase is untouched. Left unset, both phases run on
`AGENT_MODEL` exactly as before.

This addresses only one of the four causes found for the wrong verdict, and the
weakest-evidenced one: probed in isolation on those same six numbers, the small
model that got it wrong in the real run answers correctly. The other three —
that the harness checks the procedure an interpretation followed but never
compares its claim against the numbers, that the deterministic assessor covers
only the analytical workload and returned "not applicable" for this one, and
that the design phase's hypothesis is in context as a prediction to confirm —
are unaddressed and are the larger part of the fix.

### 2026-08-28 — Act on the pre-handover review

Asked to work through an outside review of the branch that is about to be
handed over, apply the findings that hold up, and say where they do not.

Three of them were defects and are fixed. The experiment code is a rounded
wall-clock second, and allocation only checked whether the result directory
already existed, so two submissions started in the same second could take the
same code, overwrite each other's status file and both name one result folder.
That window is only reachable when the run lock has deliberately been lifted,
which is exactly the feature that was asked for the day before, so the fix
keeps the feature and makes the allocation atomic instead of removing it: the
status file now doubles as the reservation and is created exclusively, so of
two runs racing for a code exactly one wins it and the other moves on. A
submission that fails before launching releases the code it took, and a
reservation that is somehow left behind carries no specification path, which is
what every reader already skips on.

Two settings failed open, meaning a typo changed behaviour instead of being
reported. Any value of `AGENT_MODEL_SERVER` other than `bundled` was treated as
an external endpoint, so a misspelling of `bundled` silently stopped the
wrapper from starting and stopping the model server; only the two real answers
are accepted now. A handbook path that named no file silently designed without
a handbook, which is the other arm of the with/without ablation and therefore a
different experiment from the one that was asked for; an empty value still
means that deliberately, but a non-empty path that names no file is refused, by
the wrapper before it starts a server and by the phase itself.

The YCSB experiment the schema-dispatch test loads was missing from a clean
checkout, because `.gitignore` excludes every `experiment*.yml`. It is now
tracked through an explicit force-add, exactly as `dev/catalog/experiment.yml`
already was, so the repair follows the convention already in the repository and
changes no test. A tracked-files-only export of the tree now runs the whole
suite with one expected failure, the harness-revision test, which has no commit
to read because an export carries no `.git`.

Two documentation findings were correct. The architecture document still
described the implemented slice as TPC-H only while the README and the code
also covered YCSB, and the README reached its main command only after a hundred
and forty lines of model-server and cluster material. The architecture document
now names both workloads, and the README opens with the six commands that take
a fresh checkout to an answered question, saying which of the later sections are
operator reference rather than part of a first run. The detailed sections were
left where they are: moving them into the architecture document would scatter
the operator material across two files rather than shorten it.

The mechanical style findings were applied where they were real. Every
`Optional[...]` annotation and its docstring counterpart is now the `X | None`
form the repository's conventions ask for, a loop variable that shadowed an
imported name was renamed, and an assigned lambda became a function. Two were
declined. The timestamps the review wanted made timezone-aware are what name
trajectory directories, and switching them to UTC would rename runs against
more than two hundred tracked trajectories for no benefit. The export lists are
grouped by kind rather than alphabetically, which is deliberate and worth more
than sorting.

One finding was not acted on. Generated trajectories are already tracked
evidence in this repository rather than build output, so they are not excluded;
they are committed separately from the code instead, which is what makes the
code commit reviewable on its own.

### 2026-08-28 — Keep model API keys out of Git and child command lines

Asked to remove the keys held in `.env` from the backup submission and every
future submission. The backup needed no history rewrite: `.env` is ignored, was
not present in the backup tree, and has never been tracked in the repository's
reachable history. The local file remains available to run the agent and was
not read or changed.

The lifecycle wrapper did copy that local key into the command line of each
agent phase, where a process-listing tool could read it. It now leaves the key
in the inherited `AGENT_API_KEY` environment variable that the agent already
supports and omits both `--api-key` and its value from the child command. A
command-line override on the wrapper is retained for compatibility but is
transferred into that environment variable before the child starts. A regression
test checks that the override reaches the environment and that neither the flag
nor the value appears in the constructed command.

### 2026-08-28 — Say what a run is doing while it does it

A started investigation printed nothing for minutes and looked stuck. Asked for
it to be watched, and for progress messages so an operator can see what is
happening.

The run was not stuck; it was silent. A phase spends most of its time inside a
single model call and writes everything durable to the trajectory, so the
terminal stayed empty while the design was in fact progressing turn by turn.
Every phase now prints a running commentary: one line as each turn is handed to
the model, and one line per tool call naming the file it touched and, when the
call was refused, the first line of the refusal. The model client says when it
is waiting out a rate limit and for how long, which used to be an unexplained
pause of up to a minute. The wrapper names each phase as it starts it, and
repeats that a benchmark is still running every ten minutes, since that wait
lasts hours and polling silently is indistinguishable from having died.

The same run exposed a second defect. Its design ran out of validation attempts
without submitting anything, and the wrapper treated that as a finished
investigation and printed a final verdict pointing at an answer file that had
never been written. Only a dry run legitimately ends at design; any other design
that reaches that point submitted nothing and is now reported as the failure it
is.

Reporting it as a failure was still only an exit code and a directory, which
says nothing about why a question went unanswered. The trajectory did hold the
reason all along -- every refusal with the check that issued it, and the model's
own closing account, which is where a question that turns out to be unanswerable
gets described -- so both are now read back out. The agent ends an unfinished
phase by saying how many times the specification was validated, whether the
budget ran out, what the last refusal was, and what the agent itself said about
the attempt. The wrapper repeats the refusal and that account beneath its own
error, so the last thing printed is the reason rather than a path to go looking
in. Each phase also announces itself with the model and endpoint it is using and
the investigation directory it is writing to, and the validate and submit lines
now say whether validation passed and which experiment code a submission got.

The investigation itself chose correctly, which is what the question was written
to test: given an application that reads and updates single rows by primary key,
it picked the key-value workload over the analytical one without being told
which to use. It could not submit, because comparing four CPU cores against
eight means a resource sweep, and BeXhoma's YCSB launcher does not translate
sweep lists yet, while the catalog contract advertises `resources.cpu` sweeps
without excluding YCSB. The agent spent two of its three validation attempts
discovering that. Reported here rather than worked around: the catalog and the
launcher are a fixed dependency for this work.

### 2026-08-28 — Sweep the documentation and restart the investigation on Mistral

Asked to bring the documentation in line with the two simplified settings, drop
what had become legacy, and start a fresh Mistral run on a question that does not
say which workload to use.

Every place that still described the old machinery now describes the settings.
The architecture record says that the server steps of the phase chain happen only
for a server this machine owns, and that an in-cluster run chooses both the
server and the handbook through the Job's environment, since the controller
passes its environment on unchanged rather than forwarding flags. The Job
manifest carries both variables with their defaults, which is where an
in-cluster ablation arm is now selected. The inventory entry for the model server
lists the two settings beside the three that say who answers. Both environment
files carry `AGENT_METHOD` as a written-out setting rather than a commented
suggestion, so the ablation is run by emptying a line that is already there. The
two
request-log entries whose mechanism was replaced today keep their text and gain a
line saying what superseded them, since the log is a record of what was asked and
when, not of what the code looks like now.

The run started from the same one command, with Mistral `mistral-small-2603`
selected in the environment file and the handbook on. Its question describes an
application that reads and updates single rows by primary key at a high request
rate and asks whether four or eight CPU cores serve more of those requests per
second. It names no benchmark: choosing the key-value workload over the
analytical one is part of what the design is being judged on.

### 2026-08-28 — Switch the handbook on and off from the environment file

Asked for the handbook to be optional in the same way the model server now is:
one setting, changed either in the environment file or on the command line that
starts a run, so the with/without ablation costs no edit to any file.

It was already a single setting, but only for a run started in the cluster: the
handbook path was a command-line option on both the agent and the wrapper, and
only the in-cluster controller read it from `AGENT_METHOD` and forwarded it. A
local run therefore had to be given the empty path by hand. Both command lines
now take their default from `AGENT_METHOD`, so `.env` decides for every way of
starting a run, an empty value designs without a handbook, and `--method` still
overrides the file for a single run. The controller forwards nothing, because
the wrapper reads the same variable out of the environment it is handed.

The rule for what counts as no handbook is unchanged: any path that is not a
file, the empty one included, leaves the design phase without one, and the
trajectory records that absence as it always has.

### 2026-08-28 — Read who owns the model server from the environment file

Asked to make yesterday's ownership setting really basic: instead of a wrapper
per kind of endpoint, simply take the value from the environment file.

What the setting does is unchanged; the machinery around it is gone. Ownership
was a pair of interchangeable server objects, chosen by a factory from a
validated mode name, reached through a command-line flag whose default came from
the environment and which the in-cluster controller then had to forward on the
command line. It is now one boolean on the single server adapter: the lifecycle
wrapper reads `AGENT_MODEL_SERVER` once at startup, from the same `.env` it
already reads the model name, endpoint, and key from, and the adapter's switch
returns immediately when the endpoint is not ours to start. The controller
forwards nothing, because the variable is already in the environment it hands to
the wrapper, in the cluster as well as locally. An exported shell variable still
overrides the file for one run, exactly as the other model settings do.

One message had to know the difference and no longer does. The line printed
while a benchmark runs said the model server was down, which was untrue for an
endpoint we never stopped; it now only names the benchmark it is waiting for,
since the switch script announces the shutdown itself whenever there is one.

### 2026-08-28 — Stop the handbook from disclaiming the phase that reads it

Scored a replayed interpretation against five criteria and reported the result:
quoting figures at one consistent scope was fixed, stating a level as a range
across repetitions rather than as two separate facts was improved, and the false
claim about which factor had varied was gone though no more precise naming
replaced it. Two criteria were untouched — latency was never reported beside
throughput, and the headline still generalized past the two levels measured.
Observed that the required reading changed how figures are quoted while leaving
what the verdict chooses to discuss alone, and proposed the likely cause: the
Navigation chapter, which interpretation now reads first, opened by disclaiming
the task that phase is performing.

The diagnosis was right, and the contradiction was direct rather than merely a
missing note. The interpretation prompt tells the agent that the handbook's
principles govern reading a measurement as much as planning one; the first
chapter it is then required to read said the handbook does not tell you how to
read a finished result, which checks decide validity, or how a conclusion must
be structured. The agent was being pointed at a document that declined the job
in its opening paragraph.

Navigation now says the principles apply to reading a measurement as much as to
planning one, and confines the disclaimer to the mechanics that genuinely belong
to the result contract: which files a result folder holds, which checks decide
validity, and how a verdict is structured and cited. What a finished number may
be said to show, at what scope, against how much variation, and how far beyond
the measured levels a conclusion may reach, are named as questions the chapters
do answer. The routing that followed the chapter table was written entirely for
designing, so a second paragraph now says which chapters carry the weight once a
run has finished and what each one governs there. Handbook version 0.4.0.

No principle was added or reworded in the same change. The criterion about
reporting latency beside throughput has no principle behind it to route to — the
load-model chapter requires the concurrency behind a latency figure but says
nothing about the operating point behind a throughput figure — and that gap is
real. Filling it at the same time as the routing fix would leave no way to tell
which of the two changed the verdict, so it waits for the next replay.

### 2026-08-27 — Renew the cluster session at submission time

Asked to fix the expired cluster session first, as it is cross-cutting, wastes
completed model work and can invalidate any workload. A design phase that ran
for two hours handed its experiment to a cluster whose session had expired after
thirty minutes; the login helper fell back to a password prompt, and a
background run has no terminal to answer it, so the submission hung for three
and a half hours and produced nothing.

The submission adapter now runs a configured shell command to renew credentials
immediately before an experiment is handed to the cluster, which is the last
moment before the session is needed and after the phase that can run long. The
command is named by an environment setting and is absent by default, so a
deployment that needs no login is unaffected. A failure stops the submission
with the login's own message, and so does a hang, since a login waiting on input
would otherwise block the submission indefinitely. Three tests cover the absent,
failing and succeeding cases.

### 2026-08-27 — Require the handbook before an interpretation may record a verdict

Asked to replay a finished YCSB result with the same model and settings but with
the handbook's Navigation section and its chapters on factors, load model,
repetition and metrics required before recording, and to score the replay on
five faults the first verdict showed: mixing per-client with aggregate figures,
misnaming the varied factor, ignoring latency beside throughput, leaving the
conclusion unbounded by the levels actually measured, and not reflecting the
spread of the two repetitions.

The first verdict could not have consulted the handbook at all. Interpretation
restricts reads to the report, the files it links to and the result contract, so
the handbook was outside the phase's reach rather than merely unrequired. It is
now reachable there, and the phase refuses to record a verdict until the named
chapters have been read by their exact headings.

The prompt names the chapters and deliberately nothing else. Listing the faults
to avoid would move the guidance out of the handbook and into the prompt, and a
better verdict would then say nothing about what the handbook is worth. A
heading absent from the current handbook is dropped rather than demanded, since
chapter titles are rewritten between revisions and requiring a missing one would
make the verdict unreachable.

The replay ran on the same report, the same model and the same settings, so the
only difference between the two verdicts is handbook access. The gate refused
the first attempt to record, the model read the five chapters, and the second
attempt was accepted. Two of the five faults are gone: the verdict no longer
mixes a single client's rate with the two-client total, quoting each level's
figure at the same scope, and it now states each level as a range across the two
repetitions rather than as two unconnected runs. One is half fixed: it no longer
calls the varied factor "threads", which was simply wrong, but it names it only
as concurrency and never says the level is a count of client pods. Two are
unchanged: latency appears nowhere, though the chapter on metrics was read, and
the headline conclusion still says throughput increases with concurrency without
bounding that to the one and two clients actually measured.

The pattern is that required reading improved how figures are quoted and left
what the verdict chooses to discuss untouched. A plausible cause sits in the
handbook itself: its Navigation chapter, which the phase now reads first, states
that the handbook does not tell you how to read a finished result folder. An
interpretation is told to read chapters that open by disclaiming the task it is
performing. Whether adding an interpretation-facing note changes the outcome is
the next thing to test.

### 2026-08-27 — Make the handbook a single on/off setting

Asked whether the handbook could be left out by changing one parameter, which is
what the planned ablation needs: the same question and model designed with and
without it, to measure what the document is worth.

It was already true of a direct agent run. The design command takes a handbook
path, treats a path that is not a file as no handbook at all, and then swaps the
prompt for a variant that tells the agent no handbook is configured and that
ordinary experimental method is its own responsibility. The gate stops requiring
a read, and the trajectory records that none was present and no digest taken, so
the two arms of an ablation are distinguishable after the fact.

It was not true of the two ways a run is actually launched. The local wrapper
forwarded the catalog and environment settings but not the handbook, and the
in-cluster controller passed neither, so both paths always got the default. Both
now forward it, the wrapper as a `--method` option defaulting to the handbook and
the controller from an `AGENT_METHOD` environment variable with the same default.
Passing an empty value at any of the three levels turns the handbook off, and
changes nothing else about the run.

*Superseded on 2026-08-28: both command lines take their default from
`AGENT_METHOD`, and the controller forwards nothing.*

### 2026-08-27 — Settle the handbook's role, and require its routing chapter

Reviewed the reframed handbook and asked for five things: keep it out of
interpretation and remove the reachability that let the model open it there
anyway, correct the inventory that claimed the validator citations were still
missing when they had shipped, finish removing "method contract" and "third
contract" from every place a reader meets them, narrow two principles that had
drifted from the science, and correct one citation.

The handbook is now unreachable during interpretation. It had been added to the
files a result-scoped context may open, justified by a comment claiming it
governs conclusions as much as designs — which is the result contract's job, not
its own. The prompt never asked for it there, so the reachability bought
nothing and blurred the division it was supposed to respect.

Reading the Navigation chapter is now what satisfies the design-space gate. The
handbook is longer than a whole-file read allows and is meant to be read one
chapter at a time, but the gate counted any successful read, so a single chapter
— or the sources list — could stand in for having consulted it at all. A
whole-file read still counts, since it contains the routing chapter by
definition. The refusal now names the chapter to read rather than only the file.

Two principles were narrowed because they overreached. The rule about resource
envelopes had been written around a container's guarantee and limit, which is a
fact about one orchestrator rather than about experiments; it now states the
general hazard — opportunistic access to a shared resource becoming an
uncontrolled factor — and leaves request-equals-limit as the local validator
policy derived from it. The rule on summarizing rates said to use the harmonic
mean, which is only correct when each observation covers the same amount of
work; it now asks for the underlying totals first and, failing those, for the
mean that matches how the observations were taken.

Terminology was finished off in the validator's comments, docstrings and
rejection messages, the design and follow-up prompts, the command-line help, the
agent README and the brief's own title. The Manolescu and Manegold tutorial now
cites the CWI record, which confirms the authors, title, tutorial status and
ICDE 2008 venue.

The two inventory rows that contradicted each other are merged into one. The
validator already cites M1.1, M2.3, M5.1 and M2.6, and the tests assert those
identifiers; the row claiming otherwise was written before that work landed.

### 2026-08-27 — Reframe the handbook as guidance and make it navigable

Reviewed the first draft of the handbook and asked for five changes: rename and
reframe it as an experiment design handbook rather than a third contract, add a
navigation section and chapter introductions so it can be read selectively,
remove the passage telling the model which principles are mechanically checked,
narrow the principles that were stated as universal laws when their applicability
depends on the question, and align the design prompt with selective reads.

Two facts found while checking those proposals set the priorities. First, the
harness was already wired for this document before it existed: the design CLI
defaults to `agent/experiment_design_handbook.md` and activates only when that file is
present, the design prompt carries a slot describing it, the design-space gate
requires it to be read before the agent may act, and the trajectory records its
SHA-256 together with whether one was configured at all. Writing the file
switched that machinery on. Second, a whole-file read of any Markdown file is
refused above 24,000 characters, and that check runs before the more generous
48,000-character allowance given to contracts, so the 25,381-character draft
could not be read whole; worse, the gate marks a required file as read only when
content comes back, so the agent could have satisfied it with one section and
proceeded having seen a ninth of the document.

The handbook is now titled *Experiment Design Handbook* and says in its own text
that it is guidance rather than a binding interface, with the three roles stated
explicitly: the catalog defines legal experiments, the result contract defines
supportable claims, and the handbook supplies method. The file name and the
`M1.1`-style identifiers are unchanged, because both are internal and renaming
the file would break the wiring described above. A `## Navigation` section now
carries the framing and a table routing a question to the chapters it needs, and
every chapter opens with its purpose, the observable features of a question that
make it relevant, a few reasoning questions rather than instructions, and
cross-references. Chapters are Markdown sections requested by exact heading; the
largest is 3,762 characters against a 12,000-character section limit, and a
load-model design reading navigation plus five chapters consumes about 17,800
characters where the single mandatory read would have cost 25,381. Which chapters
were actually read is already visible in the trajectory, since every tool call is
logged with its arguments.

Three principles were narrowed because they were wrong as stated rather than
merely strict. Requiring one factor or a full factorial outlawed fractional
factorial designs, which deliberately alias known effects and are standard
practice; the principle now asks for a design whose effects are identifiable and
whose aliasing can be stated, which still rules out an unplanned subset of
combinations. Attributing coordinated omission to closed or rate-limited
generators as such was too broad, since a closed model correctly describes a
population that genuinely waits; the error is using such measurements to describe
demand that arrives independently, and the principle now says so. Requiring a
rival explanation of every experiment contradicted the same chapter's allowance
for descriptive measurement, and is now scoped to comparative and causal claims.

The chapter on the scope of a conclusion was removed, along with the chapter
mapping principles to mechanical checks. Most of the scope chapter restated what
the result contract and the interpretation gate already enforce — read validity
before performance, report what was run, structure and cite the verdict — and two
normative sources for one rule will drift. Its genuinely design-time content
survived: include the levels you intend to conclude about, cover the conditions
where the change under test might do harm, and instrument the resource you may
later want to blame. The summary-statistics rules were kept rather than deleted,
because nothing else in the repository carries them.

The mapping from principles to decidable checks is recorded here instead of in
the handbook, so that removing it from the model's view does not lose it. A
checker can decide whether a hypothesis states any criterion a result could fail
(M1.1), whether a resource request differs from its limit in an experiment that
compares anything (M2.3), whether a comparison is attempted with too few
repetitions to separate an effect from noise (M5.1), and whether the declared
factors are exactly the varied ones (M2.6, already enforced). A rejection may
cite the identifier as its reason; the agent is no longer told in advance which
principles carry a check, because a list of what is enforced invites designing
for the checker.

One citation was corrected: the Manolescu and Manegold tutorial had been given
the URL of a different 2007 panel paper.

### 2026-08-27 — Write the experiment handbook from the public literature

Asked to act on the brief in `agent/task.md`: survey the public literature on
benchmarking method and turn it into a handbook the agent can read before it
designs, organised into chapters that each carry guidelines and the common
pitfalls those guidelines exist to prevent. Asked mid-task to keep the text
general rather than tied to the one or two workloads this deployment currently
runs, and to build it on definitive published sources — the developer's own
benchmarking papers and the wider database-benchmarking literature — rather than
on recollection.

`agent/experiment_design_handbook.md` is that handbook, versioned like the other contracts
so a run can record which text it saw. It lives in the agent's own directory
because the shared contracts directory is out of bounds for agent work, which
settles one of the brief's open questions; the remaining ones about how it is
read and hashed are untouched, since nothing in the harness reads it yet.

Nine chapters follow the order design decisions actually arise: the claim and
what would refute it, factors and parity between the things being compared, the
load model and what a throttled run may not claim, dataset size against the
memory envelope, repetition against noise, the measurement environment, metrics
and the summaries that distort them, the scope a result licenses, and cost.
Every principle has a stable identifier so a rejection can cite the principle it
enforces instead of paraphrasing it, and a closing chapter says which principles
are decidable by a checker and which are judgments no rule list can close. No
principle names a workload, a system or a value to copy, which is the brief's
guard against a handbook that turns experimental design into instruction
following.

The sources chapter records where each principle comes from: Gray's benchmark
criteria and Huppler on benchmark construction, Manolescu and Manegold on
performance evaluation in database research, the DBTest fair-benchmarking
pitfalls and their checklist, TPC's steady-state and disclosure requirements,
Jain's mistakes and games, Hoefler and Belli's reporting rules, Heiser's
benchmarking crimes, the open-versus-closed load-model result, coordinated
omission, measurement bias, rigorous repetition, cloud performance variability,
the SIGMOD reproducibility initiative, and the three TPCTC papers describing the
infrastructure this agent runs on.

### 2026-08-27 — Report every structural fault in one verdict

Asked why the input contract had not kept a locally hosted Qwen3.5 inside the
space of valid designs. Classifying every validation error recorded across the
stored trajectories showed that none of them was an illegal value drawn from one
of the catalog's enumerated menus. Roughly half were structural — a field that
exists in the schema written at the wrong depth, or given the wrong YAML type —
and the rest were relations between fields that no per-field menu can express.

The measurement also showed the validator had never once returned more than a
single error: forty-nine verdicts carried exactly one, and none carried two. An
author therefore had to discover independent faults one at a time, spending a
whole validation attempt on each. Since the design phase budgets turns per
attempt, a specification with four unrelated problems could not be repaired
inside the budget however capable its author was.

The shape check now runs every independent section and collects what each finds,
so the workload block, the systems list, the observation and placement sections
and the resource block all report together. Two ordering constraints remain,
because they are real data dependencies rather than early exits: a document whose
top level is not a well-formed object is reported on its own, since every section
check indexes into it, and the declared-factors rule is asked only once the
structure it counts is known to be sound. The environment stage now reports an
unavailable storage class alongside a placement that will not fit its node, which
previously masked each other. No rule changed, and the catalog was read, not
modified — only how many of the existing rules an author hears about at once.

A misplaced field is now pointed at the block that accepts it. The rejection
previously said only that a field was unknown where it was written, although the
schema already knew the field was legal one level up, so an author had to search
the contract to resolve a question the validator could have answered. The
unknown-field message now names the defining block, following the same principle
as the storage-class check, which exists because rejecting a value without naming
the alternatives leaves an author guessing at a closed list it cannot see. A
field the contract does not define anywhere is still reported plainly, so no
false direction is invented. This is a wording change: the rule and the set of
accepted specifications are unchanged, which the unchanged pass count over the
stored specifications confirms.

### 2026-08-27 — Report independent method violations together

A design run spent its whole validation budget learning one rule per rejection:
that a factor must be declared, that this workload runs on one system only, that
it supports no resource sweep, that the envelope must be fixed, and that a
comparison needs repetition — six attempts, each teaching one thing, ending with
no experiment. The verdict deliberately reports the first problem found, which
is right for errors that can mask one another but wrong for the method checks,
which are independent by construction.

The decidable principles of the method contract are now evaluated together and
reported in one verdict, so a design carrying three of them learns about all
three at once. The catalog and environment stages are unchanged, since a
specification that fails to resolve cannot be checked further anyway.

### 2026-08-27 — Stop discarding a design that passed on its last attempt

The first design run under the method contract reached a valid specification on
its final validation attempt and then could not submit it. Spending the
validation budget withdrew every tool, submission included, so an experiment
that was ready to run was thrown away and the phase reported that it had ended
with nothing. Individual calls to the exhausted tool were already refused one by
one, which made the blanket withdrawal both redundant and destructive.

The budget now bounds re-checking rather than handing over. When the last
validation passed and nothing has been submitted since, the tools stay available
for that one act, and the notice tells the agent to submit the exact file that
passed and edit nothing further. When there is nothing owed the behaviour is
unchanged. The same rule covers follow-up authoring, which had the same defect.

### 2026-08-27 — Survive a momentary failure of the hosted endpoint

The first design run after the method contract went in died on the model
provider's side: the endpoint answered that it was out of capacity, which the
client raised as a server error rather than a refusal. The adapter already waits
out a metered API's per-minute quota, because losing a whole investigation to a
limit that clears by itself is the wrong trade; a momentary capacity failure is
the same trade and was not covered. Both refusals are now retried with the same
widening wait, and the message says which of the two exhausted the attempts.

### 2026-08-27 — Integrate the method contract as the third contract

The handbook drafted in `agent/task.md` was written, and asked to be wired in.
It states experimental method — how a claim has to be stated to be testable,
what must be held equal, what the load model decides, which regime the data size
puts a run in, how much repetition a comparison needs, and what may be concluded
— with every principle carrying an identifier such as M2.3.

It now sits beside the other two contracts everywhere they appear. The design
phase and the follow-up author are pointed at it, must read it before writing a
specification, and are told it is normative rather than advisory and that it
gives reasons rather than values to copy. Its digest is recorded in the
trajectory beside the catalog and cluster descriptor, so two runs are comparable
only when they saw the same handbook — which is what makes the with-and-without
comparison measurable later. It stays readable during interpretation too, since
it governs what may be concluded as much as what may be designed. The
per-context read allowance grew to fit three contracts and a cluster descriptor
in one design conversation.

The document names four principles a machine can decide, and the validator now
enforces exactly those and cites them: a hypothesis that states adequacy instead
of an outcome any measurement could contradict (M1.1), a resource envelope whose
guarantee is below its limit while a comparison is being made (M2.3), declared
factors that are not the varied ones (M2.6, already enforced and now cited), and
a comparison with too few repetitions to separate an effect from noise (M5.1).
The repetition rule previously applied only where the catalog named a minimum,
which silently exempted YCSB; the handbook binds every comparison, so a workload
that names no minimum now falls back to the fewest runs from which any spread
can be estimated. Everything else in the handbook is left to the agent by
design, since the space of ways to mismatch a claim and a design is not
enumerable.

### 2026-08-27 — Make interpretation reachable for a non-analytical workload

The first YCSB investigation to reach interpretation could not finish it. Before
recording conclusions the agent must run the deterministic comparison-quality
check on the benchmarking page, and that check reads only the analytical
benchmarker's per-query tables. Handed a key-value report it answers that there
are no recognisable comparison tables, which the gate read as "the check has not
been run" rather than "there is nothing here to check". The model, which had
read the measurements correctly, was refused four identical times and ran out of
turns. The phase then failed on the first field the missing record would have
carried, so an unmet precondition surfaced as an internal error.

A benchmarking page with no comparison tables now counts as assessed, with the
comparison judgments marked not applicable — the same answer the code already
gave when there is no benchmarking page at all — so the record stays reachable
for any benchmarker that does not write per-query tables. A phase that ends
without its structured record now reports that in a sentence instead of
breaking. The wrapper also stops announcing the state of a model server it does
not own, now that it can drive an endpoint it never starts.

Both defects are the same shape as the validator gaps found earlier today: the
harness was written against the analytical workload and assumes it in places
that only surface when another workload is driven end to end.

### 2026-08-27 — Write down the experiment-handbook idea as a brief

Observed that more validator rules will not fix what the YCSB design got wrong,
because the two contracts describe what an experiment may express and what may
be claimed from a result, while neither describes how to turn a question into a
sound design. Asked for the idea to be written down for a future session rather
than built now.

`agent/task.md` records it: the evidence from this session's designs, the split
between defects a checker can decide and judgments it cannot, the proposal to
add a handbook of experimental method as a third hashed contract, the two risks
worth designing against — prescriptiveness that turns design into instruction
following, and the context budget the existing contracts already consume — and
the open questions. Nothing was implemented; the file is a brief, and it is not
the benchmark question the lifecycle controller reads.

### 2026-08-27 — Chain the phases for models we do not host

Asked for Mistral and a local Ollama to run the full investigation
automatically, the way the self-hosted model already does, instead of having
each phase started by hand. The gap was real and narrow. Everything that makes
an investigation unattended — waiting for the exact report, resuming after a
restart, cleaning up a failed experiment, carrying an approved follow-up
through a second cycle — lives in the local wrapper and was already independent
of which model answers. What the wrapper could not do was leave the model alone:
it started and stopped the bundled vLLM server at every phase boundary, so
pointing it at an endpoint somebody else runs would have tried to raise a pod
that nothing needed.

Ownership of the endpoint is now a setting rather than an assumption. The
default keeps today's behaviour and starts and stops the bundled server; the
other value says the endpoint is already there and reduces the wrapper to the
phase chain it always was underneath. Each backend block in the example
environment file carries the right value, so choosing a backend chooses this
too, and the in-cluster controller passes the choice through instead of
assuming the bundled server. The agent itself is unchanged and still starts no
server in any configuration.

*Superseded on 2026-08-28: the setting is read straight from the environment
file into one boolean, and the controller forwards nothing.*

### 2026-08-27 — Teach the validator the throughput-sweep type YCSB uses

Asked to run a quick YCSB example against PostgreSQL with the hosted Mistral
model. The design phase spent all three of its attempts on a single rejection
the model could do nothing about: the agent's validator did not recognise the
type the catalog declares for YCSB's two throughput-sweep fields, a list of
multipliers on the target operation rate, and reported it as a typo in the
contract. That type arrived with the YCSB workload in the merged upstream
release, and the agent's list of known types had never been extended to match.

The validator now knows that type and checks it the way it checks the other
list types: the value has to be a non-empty list of numbers, and a bare number
is rejected with a message saying so. The author is told what shape to write
instead of being told the contract is broken. Only the agent's validator
changed; the catalog was read, not modified.

The second attempt then stalled on that same contract rule from a different
side. The contract requires every experiment to isolate at least one factor,
and the validator requires the declared factor to be one the experiment
actually varies, so a run with a single system, a single round and no resource
sweep cannot be expressed at all. The rejection said only that the declaration
and the varied factors disagreed, which is unhelpful precisely in this case:
the declaration cannot be emptied to match, because the catalog requires it to
name something. The model read the message as an instruction to add a system
and picked one the workload does not support.

That rejection now says what to do when nothing is varied — add a second
system the workload supports, a second round to vary concurrency, or a list of
resource cells — while the ordinary mismatch message is unchanged. The rule
itself is untouched; only what it tells the author is different.

### 2026-08-27 — Discover the model identifier served by an endpoint

Asked to restart an independent SF1 study with three minutes per query and up
to three follow-ups. The local vLLM server came up, but the launch had overridden
only the model name while the active `.env` still selected Mistral's hosted base
URL. Model discovery exposed the mixed configuration before the first prompt;
no benchmark was submitted.

The agent now checks the endpoint's advertised model list before recording
provenance or sending a prompt. It keeps an exact match, adopts the sole model
identifier exposed by a dedicated endpoint, and refuses to guess when a
multi-model endpoint has no match. Completed trajectory names and provenance
therefore carry the identifier that actually handled the investigation. The
change is confined to the agent; BeXhoma is untouched.

### 2026-08-27 — Record which harness drove each trajectory

Asked for the harness revision to be recorded in trajectories, after the
validator improvements above made two runs by different models no longer
strictly comparable. A trajectory already named the model, the sampling
parameters, and the exact contracts and cluster descriptor it saw, but nothing
about the code that posed the task and judged the answers.

Every phase now opens by recording the commit at HEAD together with a
fingerprint of the harness sources. The commit alone would not settle it,
because phases are routinely run with uncommitted work in the tree, so the
sources are hashed directly and the commit stands beside them as the readable
label. The commit is read from the checkout's own files rather than by running
git, which keeps it working in an installed copy without a checkout and free of
side effects.

### 2026-08-27 — Stop the validator from rejecting a correct specification

Four Mistral-driven design attempts failed on the same field, and three of the
failures were the validator's fault rather than the model's. The catalog states
that a null storage class means the field is unset, and the profiles that allow
node-local storage list null among their permitted values, but the agent's own
type check rejected an explicit null as a type error. A model that had
correctly worked out that the field should carry no value was told it was
wrong. An explicit null now reads exactly as an omitted optional field does.

The second change is to what a rejection says. The shared resolver refuses a
storage class the cluster does not offer without naming the ones it has, so the
author is guessing at a closed list. The agent now checks the requested class
against the cluster descriptor first and quotes the available names back, along
with the fact that omitting the field takes node-local storage instead. Only the
agent's validator changed; the shared resolver and the contracts were not
touched.

Note for comparisons: this improves the quality of the feedback a model gets
during design, so trajectories recorded after it are not strictly comparable to
the archived Qwen runs, which faced the older, less informative validator.

### 2026-08-27 — Allow two agent investigations to run at once

Asked why a validated specification could not be submitted while another
investigation was benchmarking, and pointed out that BeXhoma gives every
experiment its own result directory anyway. That is correct: the refusal came
from the harness's own lock on the result root, which exists to keep two
benchmarks from measuring each other, not to keep their files apart.

The lock stays the default and now has an explicit way out. `--allow-parallel-runs`
lets one run submit while another is still benchmarking, and the submission
result carries a flag saying it did, so the trajectory records the choice
instead of leaving a reader to guess why the timings look noisy. The interim
workaround used during this session — pointing the second run at its own result
folder — is no longer needed and splits the archive for no benefit.

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

### 2026-08-27 — Offer the local Qwen3.5 tags as Ollama options

Asked what context window the locally installed Qwen3.5 9B has, whether this
machine can run it, and to add the 4B alongside it as an option without making
it active.

Both models are listed as commented blocks in the local-Ollama section of `.env`
and `.env.example`. The Mistral block stays the active one; nothing was
switched over.

The measurements behind the note in that section were taken on this machine.
Ollama serves whichever window a tag pins in its `num_ctx` parameter rather than
the model's architectural maximum, which for Qwen3.5 is 262144 tokens. Both
`ctx64k` tags pin 65536. The plain `qwen3.5:9b-q4_K_M` tag pins nothing and so
loads at Ollama's 4096-token default, which would silently truncate an agent
conversation, and the previously listed `qwen3:8b` had the same problem. Recent
trajectories peak near 26k prompt tokens, so 64k leaves roughly two and a half
times the observed need.

The 9B runs but does not fit: its weights are 6.6 GB against 8 GB of card, so at
a 64k window Ollama places 38% of it in system memory. Generation falls from
18 tokens per second on an empty context to 9.3 at a 25k-token prompt and 5.3
near the full window, while prompt processing stays fast at roughly 1300 tokens
per second. The 4B fits the card entirely at the same 64k window and generates
at about 100 tokens per second, which is why it is worth having listed.

### 2026-08-30 — Remove the loader-split knob that deadlocked synchronized loading

A design run on 2026-08-29 asked for two parallel loader pods and set the
catalog's `loading.split` field to two. That field drove the `-xnls` flag,
which the TPC-H entry script divides the total loader-pod count by to decide
how many pods run at once, so any value above one makes the Kubernetes loading
job run its pods in sequential waves. The same entry script always turns on
synchronized loading, where every loader pod waits at a barrier until all of
them have checked in. Sequential waves plus an all-pods barrier cannot both be
satisfied: the first wave blocks on the barrier, Kubernetes never schedules the
later waves, and the run sits idle until the loading timeout tears it down. The
downstream evaluation and result-upload steps then failed on the empty result
folder and crashed the run, which the lifecycle wrapper reported only as
"process exited before producing the report".

Because synchronized loading can only ever use a split of one, the field could
not express anything valid. It was removed from both places it appeared in the
catalog contract, and the catalog-to-command translator no longer emits the
`-xnls` flag. The contract version moved from 1.2.0 to 1.3.0, with
`bexhoma.spec.CATALOG_CONTRACT_VERSION` kept in step. An experiment
specification that still carries `loading.split` is now rejected as an unknown
field. This is a catalog-surface removal only: the entry script's own `-xnls`
argument and the separate self-specified-YAML path that also reads `split` are
left as they were.

### 2026-08-31 — Give every TPC-H `why` a motivating second sentence

Asked that each `why` field in the TPC-H workload block of the catalog contract
carry two sentences: the first stating neutrally what the parameter does, as
before, and a second that motivates why an experiment would use it, in the way
constraints guarantee integrity or indexes speed up lookups at the expense of
writes.

Every `why` under `workloads.tpch` was rewritten to that shape — the workload
description, the resource and component notes, the out-of-scope note, all ten
`params` entries, both loading knobs, the three post-load switches, the round
and repetition counts, and the three produced-output descriptions. The one
field that already read this way, the resource profile rationale, was left
unchanged. Nothing but the prose in these fields moved: no field name, type,
default, legal value, or neighbouring `when`/`out_of_scope` text changed, and no
code reads these strings.

The contract version moved from 1.3.0 to 1.4.0 with
`bexhoma.spec.CATALOG_CONTRACT_VERSION` kept in step, as the version-match test
requires, and the mirrored version string in `docs/AgentCatalogContract.md` was
updated to match.
