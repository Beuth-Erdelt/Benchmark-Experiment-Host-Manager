# Agent Harness

Options, model servers, deployment, and internals of the agent in `agent/`.
For a first run, start at [Agent](Agent.md). The design rationale is in
`agent/ARCHITECTURE.md`.

## Commands

| Command | Does |
|---|---|
| `bexhoma agent lifecycle` | a whole investigation: design, benchmark, interpretation, follow-ups; starts and stops the bundled model server |
| `bexhoma agent design` | one design phase |
| `bexhoma agent interpret` | one interpretation phase |
| `bexhoma agent baseline` | the bare model's answer, without catalog, handbook or tools |
| `bexhoma agent validate` | validate a hand-written `experiment.yml`; no model, no cluster |

`bexhoma agent <x>` forwards its arguments unchanged to `python -m
agent.lifecycle` (lifecycle) or `python -m agent.harness.agent --phase <x>`
(design, interpret, baseline) or `python -m agent.harness.validate`.

## Configuration

A command-line flag overrides an exported variable, which overrides `.env`.

| Variable | Flag | Default | Meaning |
|---|---|---|---|
| `AGENT_MODEL` | `--model` | – | model name the endpoint serves |
| `AGENT_BASE_URL` | `--base-url` | `http://localhost:8001/v1` | OpenAI-compatible endpoint |
| `AGENT_API_KEY` | `--api-key` | `EMPTY` | credential; `EMPTY` for a server that checks none |
| `AGENT_INTERPRET_MODEL` | `--interpret-model` | `--model` | a different, usually stronger, model for interpretation |
| `AGENT_MODEL_SERVER` | – | `bundled` | who owns the endpoint, see [Model servers](#model-servers) |
| `AGENT_ENABLE_THINKING` | `--enable-thinking` | off | ask a hybrid reasoning model (Qwen3, GLM-4.5) for thinking mode |
| `AGENT_EXTRA_BODY` | `--extra-body` (phase CLI only) | – | JSON added to every request, e.g. OpenRouter provider routing |
| `AGENT_METHOD` | `--method` | `agent/handbook/handbook.md` | design handbook; empty means none (the ablation arm) |
| `AGENT_BASELINE` | `--baseline` / `--no-baseline` | off | also answer with the bare model, as a separate investigation |
| `AGENT_RESULTS` | `--results` | `resultfolder` of `cluster.config` | Bexhoma's result root |
| `AGENT_ALLOW_PARALLEL_RUNS` | `--allow-parallel-runs` | off | submit while another agent experiment still runs |
| `AGENT_CLUSTER_LOGIN` | – | – | command that renews cluster credentials just before submission; stopped after 120 s |

The shipped `.env.example` sets `AGENT_BASELINE=1`, so a copied `.env` turns
the baseline on.

### `agent.lifecycle`

| Flag | Default | Meaning |
|---|---|---|
| `--task TEXT` / `--resume DIR` | required, one of | new question, or continue a submitted investigation |
| `--followups N` | 1 | follow-up experiments allowed in the whole investigation |
| `--attempts N` | 3 | validation calls per design or follow-up |
| `--max-tokens N` | 16384 | tokens per reply, thinking included |
| `--temperature T` | 0.0 | sampling temperature |
| `--catalog PATH` | `contracts/contract_catalog.yml` | input contract |
| `--environment PATH` | `environment.yml` | cluster snapshot; `""` skips placement checks (dry runs only) |
| `--dry-run` | off | design and validate, never submit |
| `--model-server-manifest PATH` | `MODEL_SERVER_MANIFEST` | vLLM manifest to deploy |
| `--server-script PATH` | `agent/model_server.sh` (`.ps1` on Windows) | server switch |
| `--server-start-attempts N` | 0 = until capacity | fail a stuck server start; use 3 on a new cluster |
| `--server-retry-seconds S` | 60 | wait between start attempts |
| `--poll-seconds S` | 30 | how often a running benchmark is checked |
| `--benchmark-timeout-seconds S` | 0 = wait forever | give a benchmark up after S; failed benchmarks are cleaned up by experiment code |
| `--unschedulable-timeout-seconds S` | 0 = wait forever | give a benchmark up once its pods were unschedulable for S |
| `--root`, `--trajectories`, `--status`, `--inbox` | repository, `<results>/agent/…` | working locations |

### `agent.harness.agent` (one phase)

Takes the same model, endpoint, catalog, environment, method, location,
`--attempts`, `--followups`, `--max-tokens`, `--temperature`, `--dry-run` and
`--allow-parallel-runs` options, plus:

| Flag | Meaning |
|---|---|
| `--phase design\|interpret\|baseline` | which phase |
| `--task TEXT` | the question; for interpret it defaults to the archived hypothesis |
| `--run DIR` | continue this investigation (interpret) |
| `--report PATH` | interpret exactly this `report/index.md`, without trajectory or status |
| `--extra-body JSON` | request-body additions |
| `--run-record FILE` | write the investigation directory here; used by the lifecycle |

```sh
bexhoma agent design    --task "<question>" --followups 1
bexhoma agent interpret --run <resultfolder>/agent/<run-id> --followups 1
bexhoma agent interpret --report <resultfolder>/<code>/report/index.md --followups 0
```

A `--report` interpretation can only read that one result and the files its
report links to.

### `agent.harness.validate`

```sh
bexhoma agent validate experiment.yml --environment environment.yml [--catalog PATH] [--indent 2]
```

Prints the verdict the design agent receives: `valid`, `{stage, message}`
errors, `environment_checked`, and an estimate of runs and declared-timeout
budget. Exit code 0 when valid. `--environment` is required; `""` skips the
placement checks and says so in the verdict. Needs no model and no `agent`
extra.

## Model servers

`AGENT_MODEL_SERVER` decides who owns the endpoint:

- `bundled`: the lifecycle starts a vLLM Job on the cluster for each model
  phase and stops it while the benchmark runs.
- `external`: the endpoint already exists (hosted API, local Ollama); the
  lifecycle never touches a server.
- `shared`: several lifecycles run at once and share one server. Each starts it
  if it is down; none stops it. The pod's idle watchdog releases the GPU after
  20 minutes without a request.

With any endpoint, the agent resolves the model name against the endpoint's
model list (an endpoint serving exactly one model may name it freely), and
retries quota refusals with a growing wait.

**Bundled manifests** in `agent/k8s/`, selected with `--model-server-manifest`
or `MODEL_SERVER_MANIFEST`. Edit the storage class and GPU node labels in the
manifest for your cluster.

| Manifest | Model | GPU | Temperature |
|---|---|---|---|
| `vllm-qwen38-27b.yml` (default) | Qwen3.8 27B | H200, B200 | 0 |
| `vllm-glm45-air-int4.yml` | GLM-4.5-Air INT4 | H200, B200 | 0 |
| `vllm-llama33-70b-int4.yml` | Llama-3.3-70B INT4 (one tool call per reply) | H100, H200, B200 | 0 |
| `vllm-muse-glimmer-30b.yml` | Muse Glimmer 30B | H200, B200 | 0 |
| `vllm-gemma4-31b.yml` | Gemma 4 31B | H200 | 0 |
| `vllm-nex-n25-mini.yml` | Nex-N2.5-mini | H200, B200 | 0.7 |
| `vllm-ornith-15-35b-a3b.yml` | Ornith-1.5-35B-A3B | H200, B200 | 0.6 |

`agent/model_server.sh` (`.ps1` on Windows) reads:

| Variable | Default | Meaning |
|---|---|---|
| `MODEL_SERVER_CONTEXT`, `MODEL_SERVER_NAMESPACE` | none, required | where the server runs; the namespace must match `cluster.config` |
| `MODEL_SERVER_MANIFEST` | `k8s/vllm-qwen38-27b.yml` | manifest |
| `MODEL_SERVER_JOB`, `MODEL_SERVER_SERVICE` | `bexhoma-agent-model` | object names |
| `MODEL_SERVER_PORT` | 8001 | local port forward |
| `MODEL_SERVER_BASE_URL` | `http://localhost:$PORT/v1` | endpoint |
| `MODEL_SERVER_IN_CLUSTER` | 0 | 1 inside the cluster (no port forward) |
| `MODEL_SERVER_SHARED` | 0 | 1 never stops; set by `AGENT_MODEL_SERVER=shared` |
| `MODEL_SERVER_STOP_TIMEOUT_SECONDS` | 300 | wait for the Job to go |
| `KUBE_LOGIN_SCRIPT` | – | login refresh before kubectl calls |

`agent/model_server.sh down` releases the GPU at once. `IDLE_SHUTDOWN_SECONDS`
in the manifest changes the watchdog window (0 disables it).

**Hosted APIs.** `.env.example` has blocks for OpenRouter, OpenAI, Mistral,
local Ollama and the BHT API. For OpenRouter, pin one full-precision provider
through `AGENT_EXTRA_BODY`, as the block shows; otherwise OpenRouter may route
to a reduced-precision provider or one without tool calls. Tested models and
token limits are in `agent/README.md`.

## Running in Kubernetes

`agent/k8s/lifecycle-controller.yml` runs the lifecycle as a Job with its own
service account and a persistent volume for trajectories, status and results.
After a restart it resumes the newest submission instead of submitting again.

```sh
docker build -f agent/Dockerfile.lifecycle -t <registry>/bexhoma-agent:<tag> .
docker push <registry>/bexhoma-agent:<tag>
kubectl -n <ns> create configmap agent-lifecycle-input \
  --from-file=cluster.config=cluster.config --from-file=task.txt=task.txt
kubectl -n <ns> apply -f agent/k8s/lifecycle-controller.yml
kubectl -n <ns> logs -f job/<job-name>
```

Before applying, edit in the manifest: the image, the Job name and
`AGENT_LIFECYCLE_ID` (same new value), the ClusterRoleBinding subject
namespace, the state PVC storage class, and the model server's storage and GPU
labels. The Job's environment sets `AGENT_MODEL_SERVER`, `AGENT_METHOD`,
`AGENT_FOLLOWUPS`, `AGENT_ATTEMPTS` and `AGENT_MAX_TOKENS`; `AGENT_ROOT`,
`AGENT_STATE_ROOT`, `AGENT_INPUT_DIRECTORY` and `AGENT_TASK_FILE` only change
with the volume mounts.

## Parallel investigations

An agent-started benchmark holds a lock on the result root, so a second
investigation refuses to submit while the first one runs: two benchmarks on one
cluster measure each other. To run several anyway, pin them to different nodes
with `placement:` and start each with

```sh
AGENT_MODEL_SERVER=shared bexhoma agent lifecycle --allow-parallel-runs --task "<question>"
```

All shells must use the same manifest. A draft name already taken in the shared
inbox is saved as `name_01.yml`, `name_02.yml`, …

## Internals

### Phases and budgets

| Phase | Context | Turn budget | Tools |
|---|---|---|---|
| design | fresh | 6 × attempts + 2 | `read_file`, `write_file`, `validate`, `submit` |
| interpret | fresh | 24 + 2, plus up to 4 repair turns | `read_file`, `assess_comparison_quality`, `record_interpretation` |
| follow-up authoring | fresh | 6 × attempts + 2 | as design |
| baseline | fresh | 4 | none |

- A reply with only reasoning (no tool call, no answer) is nudged; three in a
  row end the phase.
- File text per context is capped at 60% of (context window − `--max-tokens`),
  at about 3.5 characters per token, or 110,000 characters when the server does
  not publish its window. Rereading unchanged text is free.
- A Markdown file over 24,000 characters can only be read by section (at most
  12,000 characters per read, continued by offset). Contracts and
  specifications are returned whole, up to 56,000 characters, or refused.

### Rules the harness adds

These are enforced by the harness itself. The contracts say what is legal and
claimable; the handbook says what is sound; the rules below say what the
harness lets the model do with them.

**Design**

- Before writing a specification the context must read the catalog, the
  environment, and the handbook's `## Navigation` chapter.
- Drafts can only be written into the inbox, as `.yml` or `.yaml`.
- `validate` may be called `--attempts` times. When the budget is spent, tools
  are withdrawn, except `submit` when the last validation passed.
- `--dry-run` removes `submit` from the tool list.

**Validation**, beyond the catalog's own schema:

- Every structural problem is reported in one verdict, not one per attempt.
- `discriminates` must name exactly the factors the experiment varies (M2.6).
  An experiment varying nothing is refused.
- The hypothesis must name an outcome a measurement could contradict (M1.1).
  It is refused when it uses only adequacy words ("handle", "acceptable",
  "scale well", …) with no direction, comparison or number.
- CPU and memory `request` must equal `limit` (M2.3).
- When both CPU and memory are declared factors, each must vary alone in some
  pair of configurations (M2.1). The lists are paired by position, not crossed.
- An experiment that compares anything needs `repetitions` at least the
  workload's `minimum_for_conclusions` (TPC-H: 3), otherwise at least 2 (M5.1).
- Against `environment.yml`: storage class exists; pinned nodes exist and are
  not tainted out; resource ceilings hold; a pinned benchmarking node can host
  the benchmarker pods of the largest round.
- Every verdict carries an estimate: number of runs and a declared-timeout
  budget, which assumes every query hits its timeout.

**Submission**

- Only the exact bytes that passed a full validation (catalog and environment)
  can be submitted, and only while catalog and environment are unchanged.
- A lock on the result root refuses a second agent-started benchmark while one
  runs, unless parallel runs are allowed.
- `AGENT_CLUSTER_LOGIN` runs first; a failure or a hang stops the submission.
- The experiment, catalog, result contract and environment are archived in the
  result folder; Bexhoma runs detached, so the agent can exit.

**Follow-up authoring**

- Runs in a fresh context that must reread catalog, environment and handbook.
- Receives the interpretation, the decision, and ancestors' `agent_summary.yml`
  only, never their reports.
- `follow_up_of` must equal the parent's experiment code.
- At least one execution-relevant field must change (everything except title,
  hypothesis, discriminates, follow_up_of). An approved independent repeat
  must change none of them.
- When the decision names `target_queries`, `active_queries` must equal them.

**Interpretation**

- Reads start at the report index, the archived `experiment.yml`, the result
  contract and the handbook; any other file becomes readable only once a page
  already read links to it.
- Before a verdict can be recorded, the context must have read the report index
  and its Tests, the result contract, and the handbook chapters `Navigation`,
  `M2`, `M3`, `M5`, `M7`, and must have run `assess_comparison_quality`.
- The assessor, not the model, computes the claims: sweeps over concurrency,
  CPU and memory, rankings of systems, query coverage, suspect repetitions,
  validity scope. They are filed with the record; the model can only dispute
  them with a reason.
  - A sweep needs every declared level present. A step counts only when it
    exceeds both levels' standard errors (with a 5% noise floor), so shapes are
    descriptive, not significance tests.
  - Rounds with 0 or NaN in a metric measured nothing and are excluded.
  - A repetition 3× away from its peers' median is flagged, never dropped.
  - Any failed query withholds all claims. When the report has a completion
    table, claims are built from the complete phases instead, only if every
    level kept at least 2 complete repetitions; they carry `scope:
    complete_phases_only` and the completion per level.
  - YCSB summed throughput is checked against a common-duration approximation;
    above 20% excess the claim is withheld.
  - A failed monitoring check is scoped to its phases; query-failure checks to
    the incomplete phases; every other failed check counts against the whole
    result.
- The record is checked: verdict status and conclusion; every cited path read
  and inside this result; a validity scope when checks failed, naming every
  incomplete phase when complete-phase claims are used; one assessment per
  explicit question ("settled" needs supported evidence and nothing missing);
  a consistent finish-or-follow-up decision.
- A refused record gets the reason back. After 4 refusals it is accepted
  incomplete: failing parts are dropped and no follow-up starts. A refusal on
  the last turn earns a repair turn.

**Answer**

- The harness appends its own qualifications to the answer: withheld summed
  throughput, and an incomplete record.
- It writes `agent_summary.yml` into the result folder: code, parent,
  hypothesis, verdict, technical validity, unresolved question, and any
  qualification.

### What a run writes

```
<resultfolder>/agent/
  <timestamp>-sf<scale>-<model>/       one investigation; renamed once a design validates
    task.txt                           the question
    trajectory.jsonl                   every prompt, reply, tool call, budget and outcome
    phases/<n>-<phase>/                submitted specification, validation inputs, bexhoma.log
    reports/<n>-<phase>.md             each phase's account
    reports/<n>-<phase>-reasoning.md   the model's reasoning, verbatim
    answer.md                          the final answer
  inbox/                               drafts
  status/<code>.json                   running | finished | failed, for resume
<resultfolder>/<code>/agent_summary.yml
```

A benchmark the lifecycle gave up on stays `running`, since its process may
still use the cluster.

### Replay on another cluster

The maintained examples pin nodes by name. Elsewhere, keep the original file
for auditing, or copy it, replace `placement` with nodes from the new
`environment.yml` (or drop it), and revalidate. Or ask the original question
again and let the agent design for the new cluster. This working tree also
carries local `nodeSelector` edits in some Kubernetes templates; they must not
ship.

### Verification

```sh
python -m unittest tests.test_agent_harness tests.test_agent_query_evidence tests.test_harness_partial_results
```

No cluster and no model server are needed.
