# Agent

The agent answers a benchmarking question end to end. A language model designs
an experiment, Bexhoma runs it, the model interprets the report and may run a
follow-up. The model is bounded: it can only design experiments the catalog
allows, it never gets a shell, a Kubernetes client or general file access, and
the harness checks every step it takes.

Implemented scope: TPC-H with PostgreSQL and PgDuckDB, and YCSB with PostgreSQL.

## Prerequisites

| You need | Why | How |
|---|---|---|
| A Kubernetes cluster and a working `kubectl` context | Bexhoma runs the benchmarks there | see [Config](Config.md) |
| `cluster.config` | Bexhoma's settings; the agent reads its `resultfolder` | `cp k8s-cluster.config cluster.config`, then edit |
| The `agent` install extra | the model client is not part of a plain install | `pip install -e ".[agent]"` |
| `environment.yml` | what the cluster has right now: nodes, free capacity, storage classes, monitorable metrics | `bexhoma environment create`; rerun after cluster changes |
| A model endpoint | the model that designs and interprets | either a GPU node (H200 or B200) for the bundled vLLM server, or any OpenAI-compatible API |
| `.env` | which endpoint, which handbook | `cp .env.example .env`, uncomment one block |

For the bundled vLLM server, `.env` must also set `MODEL_SERVER_CONTEXT` and
`MODEL_SERVER_NAMESPACE`. They have no default, so the server switch refuses to
start without them. With a hosted API instead (OpenRouter, OpenAI, Mistral,
Ollama), set `AGENT_MODEL_SERVER=external`; no GPU is needed.

## First demo

```sh
python3 -m venv .venv && .venv/bin/pip install -e ".[agent]"
cp k8s-cluster.config cluster.config            # edit: context, namespace, resultfolder
.venv/bin/bexhoma environment create            # writes environment.yml
cp .env.example .env                            # edit: model endpoint
.venv/bin/bexhoma agent lifecycle \
  --task "Is pg_duckdb faster than PostgreSQL for aggregation under concurrency? We have a 10 GB dataset, and our servers have 64 GB of RAM." \
  --followups 1
```

The run prints its investigation directory, `<resultfolder>/agent/<run-id>/`.
When it ends, `answer.md` there holds the answer. The benchmark itself lands in
`<resultfolder>/<code>/` with its report under `report/`.

If the terminal disconnects after the experiment was submitted, continue
without submitting again:

```sh
.venv/bin/bexhoma agent lifecycle --resume <resultfolder>/agent/<run-id>
```

## What happens

1. **Design.** The model reads the catalog contract, `environment.yml` and the
   experiment design handbook, writes an `experiment.yml` and validates it.
   Validation checks the catalog, decidable handbook principles and whether the
   design fits the cluster. The model has `--attempts` tries.
2. **Submit.** The harness hands the exact validated file to Bexhoma. The
   bundled model server is stopped so the GPU is free while the benchmark runs.
3. **Benchmark.** Bexhoma runs the experiment and writes the result folder and
   its tiered report.
4. **Interpret.** The model reads the report, the result contract and the
   handbook's interpretation chapters. The harness computes the comparisons
   itself and checks the model's structured verdict before accepting it.
5. **Follow-up.** If the model asks for one and `--followups` allows it, a fresh
   context designs a follow-up experiment, and the loop continues at step 2.

| Input | Answers | Kind |
|---|---|---|
| `contracts/contract_catalog.yml` | what can be asked for | contract, versioned |
| `contracts/contract_result.yml` | what comes back, and how to answer | contract, versioned |
| `environment.yml` | what this cluster has right now | snapshot, regenerate |
| `agent/handbook/handbook.md` | what makes an experiment sound | guidance, optional |

Everything else the harness enforces on its own is listed in
[Agent Harness](AgentHarness.md#rules-the-harness-adds).

## Doing it by hand

The contracts are self-contained, so the same loop works without a model:

```sh
python validate_experiment.py experiment.yml        # catalog and placement check, no cluster
python -m agent.harness.validate experiment.yml --environment environment.yml   # stricter: also handbook rules, run estimate
python experiment.py experiment.yml                 # run; always writes the report
bexhoma summary -e <code> -rp                       # regenerate the report from local files
```

[`dev/catalog/experiment.yml`](../dev/catalog/experiment.yml) is a maintained,
runnable example. Then answer from `<resultfolder>/<code>/report/index.md`
following the result contract's `answer_contract`.

## Pages

```{toctree}
:maxdepth: 2

AgentHarness
AgentCatalogContract
AgentResultContract
AgentReport
```

- [Agent Harness](AgentHarness.md): all options, model servers, Kubernetes,
  internals, and the rules the harness adds.
- [Catalog Contract](AgentCatalogContract.md): what an `experiment.yml` may contain.
- [Result Contract](AgentResultContract.md): what a result folder contains, and how to answer.
- [Agent Report](AgentReport.md): the tiered report the interpretation reads.
