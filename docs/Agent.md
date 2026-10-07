# Agent

The agent turns a benchmark question into a validated experiment, submits it
through Bexhoma, interprets the finished report, and may submit a budgeted
follow-up. This runs that lifecycle end to end against a self-hosted model
server:

**What you need before running it:**

- A Kubernetes cluster with a working `kubectl` context: the agent reads it
  both to snapshot the environment (`bexhoma environment create`) and to
  start the self-hosted model server.
- A free GPU node (H200 or B200) for the model server. The
  `vllm-qwen38-27b.yml` manifest below requests one `nvidia.com/gpu` and up to
  96Gi of memory for the vLLM pod itself — separate from the database node
  the benchmark runs on.
- At least one benchmarking node with 64 GB of RAM available (matching what
  the example task describes), since that is what the agent sizes the
  PostgreSQL/pg_duckdb placement and the 10 GB dataset's scale factor against;
  run `bexhoma environment create` after any cluster change so the agent sees
  current, not stale, capacity.
- A `.env` in the repository root: `cp .env.example .env`, then uncomment the
  block for the local, port-forwarded self-hosted vLLM server (`AGENT_MODEL`,
  `AGENT_BASE_URL=http://localhost:8001/v1`, `AGENT_API_KEY`) to match the
  `--model-server-manifest` used below — leave `AGENT_MODEL_SERVER` unset
  (`bundled`) unless you are running more than one lifecycle at once, which
  needs `shared` instead (see
  [Choose the model endpoint](#4-choose-the-model-endpoint)). Also set
  `MODEL_SERVER_CONTEXT` and `MODEL_SERVER_NAMESPACE`: neither has a default,
  so `agent/model_server.sh`/`.ps1` refuses to start the server without them —
  they must name the kubeconfig context and namespace this cluster is reached
  under (see [Self-hosted model server](#self-hosted-model-server)).

```sh
bexhoma agent lifecycle --task "Is pg_duckdb faster than PostgreSQL for aggregation under concurrency, and does that depend on how many cores we give it? We have a 10 GB dataset, and our servers have 64 GB of RAM." --followups 3 --max-tokens 65536 --model-server-manifest agent/k8s/vllm-qwen38-27b.yml --attempts 10 --enable-thinking --allow-parallel-runs
```

- `--task` is the question to investigate; the agent designs a catalog-valid
  experiment to answer it.
- `--followups 3` allows up to three budgeted follow-up experiments once the
  first result is interpreted, if the model finds the answer still open.
- `--max-tokens 65536` raises the per-turn output budget for a model and
  context that can use it.
- `--model-server-manifest agent/k8s/vllm-qwen38-27b.yml` picks the
  self-hosted vLLM deployment (Qwen3.8 27B) that the lifecycle brings up and
  tears down around each model phase.
- `--attempts 10` raises how many validation retries the design and
  follow-up phases get before giving up.
- `--enable-thinking` turns on the served model's hybrid reasoning mode.
- `--allow-parallel-runs` lets this investigation submit even while another
  agent-started experiment is still benchmarking on the cluster.

Before running it, complete the prerequisites covered below: install the
`agent` extra, configure `cluster.config`, generate `environment.yml`, and
point the agent at a model endpoint — here, the
[self-hosted model server](#self-hosted-model-server) named by
`--model-server-manifest`, which the lifecycle starts and stops around each
model phase.

```{toctree}
:hidden:

AgentWorkflow
AgentHarness
AgentCatalogContract
AgentResultContract
AgentReport
```

```{include} AgentWorkflow.md
:heading-offset: 1
```

```{include} AgentHarness.md
:heading-offset: 1
```

```{include} AgentCatalogContract.md
:heading-offset: 1
```

```{include} AgentResultContract.md
:heading-offset: 1
```

```{include} AgentReport.md
:heading-offset: 1
```
