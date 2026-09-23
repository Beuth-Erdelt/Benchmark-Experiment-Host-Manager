# Agent harness — design decisions

Status: design settled, no harness code written yet. Last updated 2026-08-17.

Companion to `prototype-architecture.md` in this directory. That document is the
*interface agreement* between the bexhoma side and the agent side — directory
layout, the five tools, file formats, the phase loop. This document records the
*decisions and their reasons*: why the harness is built the way it is, what was
considered and rejected, and what order to build it in. Where the two disagree,
`prototype-architecture.md` wins on interface questions and this file wins on
rationale.

## The three contract files

There is one catalog, not two. Three files with three different jobs, and
confusing them makes the rest of the design hard to reason about.

`contracts/contract_catalog.yml` is the **input contract**. It is internally
split along two axes: `workloads:`, meaning what to run, and `systems:`, meaning
what to run it on. It also carries the shape of the experiment file itself in its
`experiment_schema:` section, which is why an agent needs no separate schema
document. It is read-only from the agent's point of view.

`environment.yml` is not a catalog at all. It is the set of physical facts about
one particular cluster — which nodes exist, how much memory and CPU each has,
which are tainted, which storage classes are declared. It is generated per
cluster rather than written by hand, and it exists specifically to ground
experiment designs in the actual machines rather than in assumptions a model
inherited from its training data.

`contracts/contract_result.yml` is the **output contract**. It describes what a
finished result folder contains: the declared entry point, how files group into
tiers, what the naming convention encodes, which metrics matter for which
benchmark type, and which validity checks must be read before any metric is
believed. It is a document, not a library — it contains no functions.

## What the paper claims

The vision paper (`paper/Towards_AI_Conducted_Benchmarking.pdf`, EDBT 2027)
argues that the reason no agent conducts benchmark studies today is not a
shortcoming of the models but an interface gap in benchmarking infrastructure,
which was built for human experimenters. Its thesis, in its own words, is that
AI-readiness is a property of interfaces, not of intelligence. The running loop
is offered as a feasibility demonstration that the two-sided contract is
sufficient — the contract is the contribution, not the agent.

This matters for harness design in one concrete way, which drives several
decisions below: anything that smuggles knowledge into the agent through a
channel other than the contract weakens the claim the prototype is meant to
support.

## Decisions

### 1. Reuse the existing validator; do not rebuild it

`validate_experiment.py` at the repository root, backed by `bexhoma/spec.py`, is
already the dry-run validator. It resolves an experiment file against the catalog
by actually building the command line bexhoma would run, then separately checks
it against the environment descriptor for node existence, taints, CPU and memory
ceilings, and storage-class availability. Roughly thirty distinct checks exist
with specific messages.

Rejected: rebuilding validation with pydantic or a similar schema framework. A
schema framework validates the *shape* of a document — types, required fields,
enumerated values — which is perhaps a fifth of what needs checking here. The
rest is cross-file semantic resolution: whether the named profile permits the
requested storage class, whether a memory limit fits under the allocatable
ceiling of the node it was placed on, whether a derived tuning formula evaluates.
None of that is expressible as a shape. Worse, the catalog already carries the
document shape as data, so a second schema model would be a second and silently
diverging source of truth for the one part it could cover.

What is missing is only the envelope. The validator prints human-readable prose
and returns an exit code; the agent needs the structured verdict fixed in
`prototype-architecture.md` — a boolean `valid`, a list of errors each carrying
the offending field path, the violated constraint, the value given, and a
human-readable hint, plus an `estimate` block with run count and expected
duration.

Open: the resolver raises on the first problem and stops, so an agent with three
mistakes needs three round trips. Collecting all errors before returning would
cut that. Deliberately not done yet — see decision 10, measure before hardening.

### 2. Inline the catalog in the design prompt; read results through tools

The catalog is roughly twenty-one kilobytes and the result contract about ten,
so about six thousand and three thousand tokens. The catalog is therefore small
enough to place directly in the design-phase prompt, and the agent needs
essentially all of it, so there is nothing to navigate. A prompt that changes
when the contract changes is correct behaviour, not a maintenance problem;
version-stamp the prompt with the contract version to keep the run auditable.

The result side is different and keeps the file-reading tool. A finished result
folder holds per-query timing tables, monitoring time series, and per-phase logs,
and is far too large to inline. Selective reading is exactly the capability the
result contract claims to enable, and logging which files the agent chose to open
turns context economy into a measured variable rather than an assertion.

This reverses an earlier recommendation in this project's discussion to read the
catalog through a tool as well. That recommendation over-applied the result-side
argument to a file small enough not to need it.

### 3. The prompt holds only what the contract cannot state about itself

Namely: who the agent is, which phase of the loop it is in, the tool list and the
path policy, the stopping condition for that phase, and the two budgets. It
should stay identical across runs apart from the phase.

If a workload-specific or system-specific hint seems necessary in the prompt,
that hint belongs in the catalog instead — and discovering such a hint is a
finding worth recording, because it marks a place where the contract was
insufficient.

### 4. Domain knowledge lives in the catalog, not the prompt

Rejected: injecting PostgreSQL and DuckDB expertise into the system prompt so the
agent designs better experiments.

Two reasons. First, it would quietly invalidate the experiment being run: the
paper's claim is that the catalog's `why:` and `when:` fields carry the domain
knowledge, and a prompt-injected shortcut tests the prompt rather than the
contract. The catalog already states which TPC-H queries are multi-way joins and
which are scan-dominated, that a given workload is inappropriate for join
questions, and what a profile is intended for. Second, pretrained domain
knowledge is a hazard as much as an asset — the environment descriptor exists
precisely to override assumptions inherited from training data.

If the agent needs to know something about a system, write that sentence into the
system's catalog entry, where it is versioned, shared, and visible to anyone
reading the archived run.

### 5. The hypothesis and isolated factors are required, and already enforced

Not an open question. The paper states that a specification records not only what
to run but why, with a hypothesis field declaring what the experiment is meant to
discriminate, and `bexhoma/spec.py` rejects a file missing any required header
field before producing a command.

The purpose is to force the agent to commit to an interpretation *before* the
run, so that a mismatch between the stated hypothesis and the actual design is
visible to a human reading the archived specification afterwards. This is a
weaker guarantee than validation and the paper is honest about that — how an
automated experimenter stays honest is named as open research.

### 6. Compaction between phases is deterministic, not model-generated

The interpretation phase does not need the rejected drafts that preceded the
valid specification, and dropping them matters for small models with limited
context.

Rejected: compacting by asking a model to summarize the prior conversation. That
inserts an unlogged, non-deterministic step that makes scientific judgments on
the agent's behalf, and it breaks the trajectory as a faithful replay — which
matters because the trajectory is the artifact the paper archives.

Instead, rebuild the interpretation-phase conversation from the event log by
rule: always keep the task verbatim, the final validated specification, the
submission event with its experiment code, wall-clock timing, and phase
transitions; drop the rejected drafts and their error lists. Rules like these are
reproducible, cheap, auditable, and describable in a paragraph. Nothing is lost —
the rejected drafts stay in the log for human analysis of how many attempts were
needed; they simply do not occupy the agent's context while it reads results.

### 7. Two budgets, both told to the agent

Repair attempts within the design phase, and follow-up experiments across phases.
The follow-up budget is one for the demo.

Tell the agent both numbers explicitly. An agent that believes it has unlimited
follow-ups designs an exploratory first experiment and plans to narrow later; an
agent that knows this is its only shot designs a decisive one. The difference is
large enough to be worth reporting.

### 8. `list_results` and the result contract are separate mechanisms

`list_results` reads the status directory — one small JSON file per experiment
with its code, state, title, and pointers. It answers "what exists and is it done
yet" and knows nothing about result contents.

The result contract is read like the catalog, as a document, to learn how a
result folder is organized. Navigation is then ordinary file reads guided by that
map. Keeping these apart avoids the temptation to build a result-parsing library,
which would move interpretation out of the agent and into the harness.

### 9. The critic is a separate invocation and an experimental variable

A stronger model reads the question and the candidate specification and answers
one thing: does this design discriminate the factors it claims to. Keep it
separate from the authoring agent and log its verdict.

Built this way it is a clean variable — same weak model authoring, critic on
versus off — so the effect of critique on design quality is measurable rather
than assumed.

### 10. Test weak models before hardening validator feedback

Producing a schema-conformant file from a schema given in the prompt is
form-filling, which small models handle. Choosing which queries isolate joins,
recognising that "under concurrency" means sweeping client counts rather than
fixing one, and deciding that a memory ceiling means memory should be a swept
factor — that is reasoning, and it is the likelier failure point.

There is a sharper version worth stating: the catalog already labels which
queries are multi-way joins, so a weak model does not need to know TPC-H, only to
read a field and follow it. Running the loop with a deliberately weak model is
therefore the strongest available evidence for the paper's thesis. A small model
succeeding *because the catalog told it what to pick* is the result, not a
weakness in it.

Caution on metrics: validation pass rate alone will mislead, because the
interesting failure is a specification that validates perfectly and answers
nothing. Design quality needs its own judgment alongside it.

### 11. No mocks; run against the cluster, but keep the dry-run design loop

Rejected: the mock validator and canned result folders described in
`prototype-architecture.md`. The cluster is available and lightly loaded.

Kept from that plan, though it is not a mock: the design phase needs no cluster
at all, because the validator is explicitly a dry run that touches nothing and
spawns no subprocess. Prompts, models, and critic configurations can therefore be
iterated dozens of times an hour on the question-to-validated-specification path
alone, and cluster time is spent only once the design side behaves.

## Build order

1. Generate `environment.yml` from the live cluster. `bexhoma/environment.py` has
   its own command-line entry point that connects, curates nodes, storage classes
   and resource ceilings, and writes the file.
2. Wrap `validate_experiment.py` in the JSON verdict format.
3. Build the design phase alone — prompt, tools, repair loop, event log — and run
   weak models against it offline until decision 10 is answered empirically.
4. Then submission, the status watcher, and the interpretation phase, which are
   the parts that cost cluster time.

Steps 1 and 2 are independent of each other.

## Known gaps and prerequisites

The `estimate` block in the verdict format is specified but unimplemented. Run
count is derivable from the concurrency sweep, repetitions, and resource cells; a
duration estimate would need the archive of past runs.

The harness must handle re-authentication. The cluster's OIDC login token lasts
about five minutes with a refresh window near thirty, while a benchmark run takes
roughly twenty, so a watcher that polls across a run will hit expiry mid-flight.

`environment.yml` is generated and not checked in, so it must be produced on
whichever machine will run the harness, while connected to the cluster.

## Cluster facts

Running against the BHT ds_cluster requires the university VPN from off-site,
because the API server hostname resolves only inside the university network. The
shared CephFS storage class fails to mount on several nodes, so bexhoma pods are
pinned to `cl-worker36` through local, uncommitted edits to five templates under
`k8s/` — those edits are cluster-specific and must not be committed. `cluster.config`
is gitignored and never travels through the repository.
