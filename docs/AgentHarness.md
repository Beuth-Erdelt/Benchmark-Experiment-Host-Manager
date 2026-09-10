# Agent Harness: Running the Prototype

## What this is

[`AgentWorkflow.md`](AgentWorkflow.md) describes the loop that turns a
benchmarking question into an evidence-backed answer: read the two contracts,
build an `experiment.yml`, validate it without touching a cluster, run it, then
read the tiered report and answer according to the result contract. This
repository ships a program that performs that loop with a language model driving
each step. It lives in the repository's `agent/` directory, and this page is the
operator guide to running it, with a command for every stage.

The harness is deliberately narrow. It demonstrates a *bounded autonomous
experimenter*, meaning a language model that may only design, validate, submit,
interpret, and follow up on experiments the catalog already allows, and that
never receives a shell, a Kubernetes client, or general filesystem access. The
implemented slice is TPC-H (the analytical decision-support benchmark) with
PostgreSQL and PgDuckDB, and YCSB (a key-value workload) with PostgreSQL. The
full annotated pipeline, the capability boundary, and the enforcement rules are
in `agent/ARCHITECTURE.md`; the command reference is `agent/README.md`; this
page merges the two into a task-by-task walkthrough for the documentation site.

The pieces you will invoke:

| Command | What it does |
|---|---|
| `python -m agent.harness.agent` | One phase — `design`, `interpret`, or `baseline` — of one investigation. This is the model-facing agent itself. |
| `python -m agent.harness.validate` | Dry-run validation of a hand-written `experiment.yml`, no model and no cluster. |
| `python -m agent.lifecycle` | The local wrapper that chains the phases end to end, starting and stopping a self-hosted model server around each one. |
| `agent/k8s/lifecycle-controller.yml` | The same chained loop as an unattended Kubernetes Job with in-cluster credentials. |

All four of the runnable ones are also reachable through the `bexhoma` CLI:
`bexhoma agent design`, `bexhoma agent interpret`, `bexhoma agent baseline`,
`bexhoma agent validate`, and `bexhoma agent lifecycle` each forward their
remaining arguments unchanged to the module above, so the two forms are
interchangeable and this page uses the `python -m ...` spelling throughout. The
`bexhoma agent` command needs the same `agent` install extra and reports plainly
when it is missing.

## Six commands, start to finish

A fresh checkout reaches an answered question in six steps. Each is explained in
full below; the wrapper in step 5 is the shortest path and the phase-by-phase
commands after it are only needed when you want to drive the stages yourself.

```sh
# 1. install with the agent extra — an ordinary bexhoma install omits it
python3 -m venv .venv && .venv/bin/pip install -e ".[agent]"

# 2. point bexhoma at the cluster, then edit the copy
cp k8s-cluster.config cluster.config

# 3. snapshot the cluster the agent will design against
.venv/bin/python -m bexhoma.environment --output dev/catalog/environment.yml

# 4. choose the model endpoint, then edit the copy
cp .env.example .env

# 5. answer a question end to end: design, benchmark, interpretation, follow-up
.venv/bin/python -m agent.lifecycle --task "<benchmark question>" --followups 1

# 6. continue an investigation whose benchmark was already submitted
.venv/bin/python -m agent.lifecycle --resume <result-folder>/agent/<run-id>
```

The run prints the investigation directory it writes to and, at the end, the
path of the final answer. To check the installation with no cluster at all, run
the test suite shown under "Verification" at the end of this page.

## 1 — Install with the agent extra

The agent needs a client library for its OpenAI-compatible model server that
ordinary bexhoma use does not, so a plain `pip install -e .` will not run it.
Install the `agent` extra:

```sh
python3 -m venv .venv
.venv/bin/pip install -e ".[agent]"
```

## 2 — Configure bexhoma for the cluster

```sh
cp k8s-cluster.config cluster.config   # then edit it
```

The agent reads this same file, and only for one thing: the `resultfolder` it
declares, which decides where results and all investigation artifacts land. The
agent and the benchmark therefore cannot disagree about that location. A
relative `resultfolder` resolves against the repository. See the repository's
main quick start and configuration guide for the rest of the file.

## 3 — Snapshot the target cluster

The design step is grounded in a description of the cluster as it is right now —
which nodes exist, how much CPU and memory each can still allocate, which
storage classes are available, what the namespace resource limits are. That
description is a file the agent reads, not a contract, and it can only be
produced by connecting to a live cluster:

```sh
.venv/bin/python -m bexhoma.environment --output dev/catalog/environment.yml
```

Regenerate it whenever the cluster changes. It carries a `collected_at`
timestamp and goes stale the moment capacity moves after that. The checked-in
[`dev/catalog/environment.yml`](../dev/catalog/environment.yml) is one such
snapshot from a fixed point in time — a starting example, not a live view.

## 4 — Choose the model endpoint

Three settings decide which server answers the agent. `AGENT_MODEL` is the name
the server serves the model under, `AGENT_BASE_URL` is its OpenAI-compatible
endpoint, and `AGENT_API_KEY` is the credential — the placeholder `EMPTY` for a
server that checks none. Copy [`.env.example`](../.env.example) to `.env` in the
repository root and edit it; both `python -m agent.harness.agent` and
`agent/lifecycle.py` read that file at startup. It is ignored by git, so
real keys stay out of the history.

An exported shell variable overrides the file, and a command-line flag
(`--model`, `--base-url`, `--api-key`) overrides both, so a single run can use a
different server without editing anything.

`.env.example` carries a ready block for each backend in use: the bundled vLLM
server reached through a local port forward, the same server reached by its
in-cluster service name, a local Ollama, OpenAI, and Mistral. Ollama and Mistral
serve the same protocol under a `/v1` path, so nothing but these three values
changes.

Two behaviours differ once you leave the self-hosted server. First, the agent
resolves the configured model name against the endpoint's model list: an
endpoint that advertises exactly one model may name it whatever it likes and the
agent adopts that name, while an endpoint advertising several requires an exact
match. Second, a metered API refuses a turn once a per-minute quota is reached
where a self-hosted server would simply queue it, so a refused turn is retried
with a widening wait before the phase gives up.

One more setting, `AGENT_MODEL_SERVER`, decides who owns the endpoint. The
default `bundled` means the lifecycle wrapper in step 5 starts and stops a
self-hosted vLLM server around every phase. `external` means the endpoint is
already there — a hosted API, or an Ollama on your machine — so the wrapper only
chains the phases and never touches a server. Each block in `.env.example`
already carries the right value. The agent CLI itself never starts a server in
either case.

## 5 — The one-command lifecycle

[`agent/lifecycle.py`](../agent/lifecycle.py) chains every phase of one
investigation. With `AGENT_MODEL_SERVER=bundled` it also starts the vLLM server
for the model phases, stops it while the benchmark runs so the GPU is free,
waits for the exact report, repeats the cycle for an approved follow-up, and
leaves the server down after the final answer:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python -m agent.lifecycle \
  --task "Is PgDuckDB faster than PostgreSQL on join-heavy TPC-H queries at SF10, and does that hold as concurrency rises?" \
  --followups 1
```

With `AGENT_MODEL_SERVER=external` in `.env` the same command drives a hosted
API or a local Ollama end to end, with no server started or stopped along the
way:

```sh
.venv/bin/python -m agent.lifecycle --task "<benchmark question>"
```

`--followups N` is the budget for follow-up experiments: after interpreting a
result, if the question is not fully resolved, the agent may author and submit
one new experiment that continues it, and `N` caps how many times that can
happen across the whole investigation. `--followups 0` interprets the first
result and stops.

Useful flags:

- `--interpret-model NAME` runs the interpretation phase on a different, usually
  stronger model than the one that did the design.
- `--server-start-attempts 3` makes a stuck model-server startup fail after
  three tries instead of retrying until a shared GPU frees up. Use it when first
  bringing the server up on a new cluster, so a misconfiguration surfaces as an
  error rather than an indefinite wait.
- `--benchmark-timeout-seconds S` gives an unattended run a deadline; the
  default of zero waits for the report indefinitely. If the submitted benchmark
  is definitively failed or has exited with no report, the wrapper invokes
  bexhoma's experiment-scoped cleanup for that exact experiment code and leaves
  shared monitoring and message-queue objects alone.
- `--dry-run` designs and validates but never submits.

After a terminal disconnect, resume an investigation that already submitted its
experiment without submitting it again:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python -m agent.lifecycle --resume <result-folder>/agent/<run-id>
```

### The experiment design handbook and the ablation

Before every design and every follow-up the agent reads an *experiment design
handbook* — a document of methodological guidance on what makes a benchmark
sound rather than merely legal. Its digest is recorded in the run's trajectory,
and the few principles a machine can decide are enforced by the validator, which
cites them by identifier. The shipped handbook is `agent/experiment_design_handbook.md`, and `AGENT_METHOD`
in `.env` names it.

The other arm of the with/without comparison designs with no handbook at all.
Switch it off by leaving `AGENT_METHOD` empty in `.env`, or for one run:

```sh
AGENT_METHOD= .venv/bin/python -m agent.lifecycle --task "<benchmark question>"
```

`--method PATH` on either the agent CLI or the wrapper overrides the file for a
single run; any path that is not a file means no handbook.

### The bare-model baseline

Before the design phase, the wrapper also answers the question with the bare
model — no catalog, no handbook, no tools — as its own separate investigation,
so the full pipeline's answer can be read against what the model alone would
have said. The baseline `answer.md` path is printed and linked from the design
trajectory. Skip it with `--no-baseline`, or `AGENT_BASELINE=0`. The same phase
runs on its own:

```sh
.venv/bin/python -m agent.harness.agent --phase baseline --task "<benchmark question>"
```

## 6 — Driving the phases by hand

Each `python -m agent.harness.agent` invocation performs one durable phase and
exits. All phases of one question share a single investigation directory and a
single append-only trajectory.

Design and submit:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase design \
  --task "<benchmark question>" \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

After the emitted experiment code has a finished `report/index.md`, continue the
same investigation by pointing `--run` at its directory:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase interpret \
  --run <result-folder>/agent/<investigation-id> \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

If interpretation submits a follow-up, wait for that report and run the same
command again with the same `--run` path. Otherwise the investigation's
top-level `answer.md` now holds the interpretation of that one result.

To interpret a finished result with no local trajectory, status, or cluster
configuration in play, point `--report` straight at its report index. This is
the portable one-result form:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase interpret \
  --report /path/to/results/<experiment-code>/report/index.md \
  --task "<question this experiment tests>" \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

When `--task` is omitted here, the harness uses the archived experiment's
hypothesis or title. Interpretation starts from that one report, follows only
the local links inside it, and cannot read another experiment merely because it
shares the same result root.

`--dry-run` designs and validates without submitting. Design and `--run`
continuation take the result root from `cluster.config` unless `--results` or
`AGENT_RESULTS` overrides it; a standalone `--report` run derives the root from
the report path when none is configured.

## Validating an experiment you wrote yourself

To check an `experiment.yml` you wrote by hand, with no model involved at all,
call the validator directly:

```sh
.venv/bin/python -m agent.harness.validate experiment.yml \
  --environment dev/catalog/environment.yml \
  --catalog contracts/contract_catalog.yml --indent 2
```

It prints the same structured verdict the design agent's `validate` tool
receives — the `valid` flag, a list of `{stage, message}` errors, whether the
environment was checked, and the expanded benchmark-phase count with a
conservative declared-timeout budget — and exits 0 when the specification is
valid, 1 otherwise. It touches no cluster. `--environment` is required on
purpose; pass an empty string to skip the placement and resource-ceiling checks,
and the verdict then records that it did so in its `environment_checked` field.

[`dev/catalog/experiment.yml`](../dev/catalog/experiment.yml) is a maintained,
runnable example: a two-system PostgreSQL-versus-PgDuckDB sweep across
concurrency and memory pressure, with a header comment tracing each field back
to the phrase in the question that produced it. Copy it, edit it, and validate
your copy before running anything.

The declared-timeout budget assumes every active query reaches its per-query
deadline, so it is a cost ceiling for comparing designs, not a prediction of
elapsed time. When a follow-up decision leaves only particular queries
unresolved, follow-up authoring is required to use that same `active_queries`
subset; a full-workload follow-up stays possible but its decision must state why
the broader cost is scientifically necessary.

## What interpretation checks before it trusts the model

Interpretation runs a deterministic quality and result assessment before it
accepts any conclusion the model states. Where per-query data exists it
separates completion of the planned query set from speed on the queries that
succeeded everywhere, marks whole-workload throughput non-comparable when a
planned query errored, and flags unusually different repetitions as warnings.
Independently of the workload name, it reads the archived `discriminates`
factors — the axes the experiment set out to vary — and computes the ordered
concurrency, CPU, and memory shapes and the categorical system rankings itself.
The structured interpretation must reproduce those shapes, rankings, and
factor-level means exactly: it cannot call a measured rise a plateau or quote a
different number. Failed monitoring checks carry the exact affected phases and
whether the performance metrics remain usable.

## What a run writes

Investigations are written under the `agent/` subdirectory of the result folder
`cluster.config` declares, beside the benchmark results themselves, so the
checkout keeps no run artifacts of its own. Override the location with
`--trajectories`. Two directories sit there as siblings of the investigations:
`inbox/`, where the design and follow-up agents draft specifications before
validating them, and `status/`, the registry of `<experiment-code>.json` files
behind the resume logic. Override them with `--inbox` and `--status`.

The design step first creates a timestamp-only working directory. Once it
produces a valid experiment, the harness renames the directory to
`<result-folder>/agent/<timestamp>-sf<scale>-<model>/` — for example
`20260827T111847490995-sf2-qwen3.8-27b` — so the scale factor and served model
are visible without opening anything. An incomplete design stays timestamp-only
because it has no trustworthy scale factor. Every later interpretation and
follow-up appends to the same directory:

- `trajectory.jsonl` — the append-only record of every phase: prompts,
  reasoning, tool calls, stages, hashes, budgets, and outcomes;
- `task.txt` — the original question;
- `phases/<number>-<phase>/` — the immutable submitted specification, the
  validation inputs, and the bexhoma log for that phase, when it submitted an
  experiment;
- `reports/<number>-<phase>.md` — each phase's own written account;
- `reports/<number>-<phase>-reasoning.md` — that phase's model-authored
  turn-by-turn reasoning, rendered verbatim from the trajectory;
- `answer.md` — written only after the final interpretation, containing its
  one-result answer according to the archived result contract.

Each submitted result folder also archives the exact experiment, input catalog,
result contract, and environment descriptor used to validate it. After a
successful interpretation it gains `agent_summary.yml`: the experiment code, its
`follow_up_of` parent, the hypothesis, the scientific verdict, the technical
validity, and the unresolved next question, with evidence paths relative to that
folder so the lineage stays portable. Follow-up authoring receives only these
compact summaries of its ancestors, never their full reports or metrics.

## Running two investigations at once

An agent-started run takes an exclusive lock on the result folder, so a second
run refuses to submit while the first is still benchmarking. That is a
measurement policy, not a filesystem limit: two benchmarks sharing a cluster
measure each other. Pass `--allow-parallel-runs` to submit anyway; the run
records in its trajectory that it did so, and you should pin the two
investigations to different nodes with a `placement:` block first, or the
numbers will describe the interference rather than the systems.

## Self-hosted model server

[`agent/k8s/vllm-qwen38-27b.yml`](../agent/k8s/vllm-qwen38-27b.yml) and
[`agent/model_server.sh`](../agent/model_server.sh) run a vLLM server on the cluster.
They are a convenience, not part of the pipeline — any OpenAI-compatible
endpoint works. If you use them, four values are specific to the cluster they
were written for and must be set for yours: the kubeconfig context and namespace
(exported as `MODEL_SERVER_CONTEXT` and `MODEL_SERVER_NAMESPACE`; the namespace
has no default because the switch also writes it into the kube context), the
login refresh script (`KUBE_LOGIN_SCRIPT=/bin/true` when an ordinary kubeconfig
needs no refresh), and the storage class and GPU node labels, which are edited
directly in the manifest. Getting the GPU labels wrong leaves the pod
unschedulable and startup waits for capacity by design, so pass
`--server-start-attempts 3` the first time and check `kubectl describe pod` if
it stalls.

The pod carries its own idle watchdog: it releases the GPU once twenty minutes
pass with no request, so a phase run by hand does not strand a GPU node. Set
`IDLE_SHUTDOWN_SECONDS` in the manifest to change that window, or `0` to keep
the server up until something deletes it. `agent/model_server.sh down` hands the
GPU back immediately.

## Autonomous Kubernetes lifecycle

For an unattended investigation, use the Kubernetes Job in
[`agent/k8s/lifecycle-controller.yml`](../agent/k8s/lifecycle-controller.yml). A
Job rather than a bare Pod so Kubernetes restarts the controller after a node or
process failure; a persistent volume holds its trajectory, status, and results.
On restart the controller resumes the newest durable submission through the
ordinary `--resume` path instead of designing and submitting again.

Build and publish the image from the repository root:

```sh
docker build -f agent/Dockerfile.lifecycle -t <registry>/bexhoma-agent:<tag> .
docker push <registry>/bexhoma-agent:<tag>
```

Put the question alone in `task.txt`, then create the inputs as a ConfigMap:

```sh
kubectl -n <namespace> create configmap agent-lifecycle-input \
  --from-file=cluster.config=cluster.config \
  --from-file=task.txt=task.txt
```

Before applying the manifest, edit its explicit portability values: the
controller image placeholder, the Job name and `AGENT_LIFECYCLE_ID` (the same
new investigation name for both), the ClusterRoleBinding subject namespace (from
`replace-me` to the target namespace — this read-only cluster permission lets
the environment refresh list nodes, storage classes, and priority classes), and
the lifecycle-state PVC storage class plus the same model-server storage and
GPU-label choices as above. Then:

```sh
kubectl -n <namespace> apply -f agent/k8s/lifecycle-controller.yml
kubectl -n <namespace> logs -f job/<job-name>
```

The controller authenticates as its own service account, so it does not depend
on a workstation's expiring login, and its write authority is limited to the one
namespace. The Job's environment block is where an in-cluster run picks its
model server (`AGENT_MODEL_SERVER`) and its handbook (`AGENT_METHOD`), exactly as
`.env` does locally. The language model still receives only the catalog,
environment, result contract, and phase tools — never Kubernetes or terminal
access.

## Replay on another cluster

The maintained examples pin `sut`, `loading`, and `benchmarking` to a local node
name. On another cluster there is usually no node by that name, so its validator
correctly rejects the unchanged file. There are three replay levels:

1. **Audit the original run.** Keep the submitted file unchanged beside its
   archived environment and result evidence; it records exactly what ran.
2. **Repeat the design elsewhere.** Copy the specification, replace each
   `placement` value with a node from the target's freshly generated
   environment (or omit `placement` and let the target scheduler choose), and
   revalidate before submitting. This changes deployment binding only, not the
   workload, treatment, resources, rounds, or repetitions.
3. **Let the agent adapt the design.** Generate the target environment and ask
   the original question again; the agent chooses legal placement from that
   descriptor and produces a new auditable specification.

This working tree also carries local `nodeSelector` edits in several Kubernetes
templates that force this test cluster onto one node. They must not ship in a
portable release — removing `placement` from the YAML is not enough while those
template overrides remain.

## Verification

```sh
.venv/bin/python -m pytest \
  tests/test_agent_harness.py \
  tests/test_agent_lifecycle.py -q
```

Neither test needs a cluster or a model server.

## See also

- [`AgentWorkflow.md`](AgentWorkflow.md) — the question-to-answer loop this
  harness automates.
- [`AgentCatalogContract.md`](AgentCatalogContract.md) — what a valid
  `experiment.yml` may contain.
- [`AgentResultContract.md`](AgentResultContract.md) — what a finished run's
  result folder holds, and how to answer from it.
- [`AgentReport.md`](AgentReport.md) — the tiered report the interpretation
  phase reads.
- `agent/ARCHITECTURE.md` — the full annotated pipeline, capability boundary,
  enforcement rules, and known limits.
- `agent/README.md` — the terse command reference.
