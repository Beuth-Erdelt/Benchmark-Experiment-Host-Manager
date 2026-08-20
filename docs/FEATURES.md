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
| Tiered result reading and self-contained final study-report structure | `agent/harness/prompts.py`, `agent/harness/tools.py` | Done |
| Model adapter for the self-hosted server | `agent/harness/model_client.py` | Done |
| Design, interpretation, staged follow-up, durable carry-forward, single-investigation trajectory, phase reports, aggregated final report, and CLI | `agent/harness/agent.py` | Done |
| Model server manifest | `agent/k8s/vllm-qwen38-27b.yml` | Done |
| Environment refresh with local cluster facts | `dev/catalog/refresh_environment.py` (gitignored) | Done |
| Repeated same-system treatments rejected before Bexhoma collapses them | `agent/harness/validation.py` | Done and regression-tested |
| Local server/benchmark lifecycle, retry, resume, and cleanup | `dev/agent_lifecycle.py`, `dev/model_server.sh` | Local-only; unit- and cluster-checked |
| Quick start | `agent/README.md` | Done |
| Full pipeline, annotated visual, replay rules, and decision record | `agent/ARCHITECTURE.md` | Done; all older agent-pipeline descriptions merged here |
| Critic as a separate invocation | — | Optional evaluation, intentionally outside the prototype |

All model contexts share one bounded conversation loop but receive different
prompts and tools. Contracts are read rather than embedded, all reads and writes
are logged, and submission is bound to the exact validated specification and
contract hashes.

### Model server

`agent/k8s/vllm-qwen38-27b.yml` serves `Qwen/Qwen3.8-27B-FP8` through vLLM's
OpenAI-compatible API on the cluster's H200 node. It follows the pattern already
used for the other model servers in this namespace: one pod that downloads the
weights into a persistent volume on first start and serves them from there
afterwards. It is deliberately not placed on the node bexhoma uses for the
system under test, because a model server competing for that node's resources
would contaminate the measurements the agent is designing.

---

## Part 2 — Request log

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
when the H200 pool had no free GPU, which is now an automatic wait rather than a
terminal lifecycle failure.

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
