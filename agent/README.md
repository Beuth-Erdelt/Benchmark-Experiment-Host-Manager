# Benchmark agent quick start

The prototype turns a research question into a catalog-valid benchmark,
submits it through Bexhoma, interprets the finished report, and may submit a
budgeted follow-up. See [ARCHITECTURE.md](ARCHITECTURE.md) for the full annotated
pipeline, contracts, module map, replay rules, and limitations.

## Prerequisites

- Install the repository dependencies in a Python environment.
- Configure Bexhoma for the target cluster and writable result root.
- Provide an OpenAI-compatible model endpoint and model name.
- Generate a current target-environment descriptor:

  ```sh
  .venv/bin/python -m bexhoma.environment \
    --output dev/catalog/environment.yml
  ```

The active catalog is `contracts/contract_catalog.yml`. The current prototype
supports TPC-H with PostgreSQL and PgDuckDB.

## One-command local lifecycle

For this cluster's local testing, the wrapper starts vLLM for model phases,
stops it while benchmarks run, waits for the exact report, repeats the cycle for
a follow-up, and leaves the server down after the final answer:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python dev/agent_lifecycle.py \
  --task "<benchmark question>" \
  --results /home/ll/benchmarks \
  --followups 1
```

Startup retries indefinitely when the shared H200 has no free GPU. To fail
after a bounded number of attempts, add for example
`--server-start-attempts 3`. A zero benchmark timeout waits indefinitely; use
`--benchmark-timeout-seconds <seconds>` when unattended work needs a deadline.

After a terminal disconnect, resume an investigation that already submitted an
experiment without resubmitting it:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python dev/agent_lifecycle.py \
  --resume agent/trajectories/<run-id> \
  --results /home/ll/benchmarks
```

`dev/agent_lifecycle.py`, `dev/model_server.sh`, and the vLLM manifest are local
operator conveniences. They are not required by the agent pipeline or intended
for the portable release.

## Portable phase-by-phase operation

Design and submit:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase design \
  --task "<benchmark question>" \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --results "<result root>" \
  --followups 1
```

After the emitted experiment code has a finished `report/index.md`, continue
the same investigation:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase interpret \
  --run agent/trajectories/<investigation-id> \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --results "<result root>" \
  --followups 1
```

If interpretation submits a follow-up, wait for that report and invoke the same
command with the same investigation path. Otherwise the investigation's
top-level `answer.md` is the final aggregated report. Use `--dry-run` to design
and validate without submission.

## Outputs

The design invocation creates one `agent/trajectories/<investigation-id>/`.
Every interpretation and follow-up appends to that directory:

- `trajectory.jsonl`: the append-only record of all phases, prompts, reasoning,
  tool calls, stages, hashes, budgets, and outcomes;
- `task.txt`: the original question;
- `phases/<number>-<phase>/`: immutable submitted specification and Bexhoma log
  for that phase, when it submitted an experiment;
- `reports/<number>-<phase>.md`: each phase's own account;
- `answer.md`: created only after the final interpretation and containing its
  required full-study aggregation.

Each submitted result folder archives the exact experiment, input catalog,
result contract, and environment descriptor used for validation.

## Replay on another cluster

The example runs pin `sut`, `loading`, and `benchmarking` to the local node
`cl-worker36`. For another cluster, generate its environment and either replace
those three values with valid target nodes or omit the `placement` block before
revalidation. Do not ship this working tree's local hard-coded Kubernetes
`nodeSelector` overrides; portable templates must remain unpinned.

## Verification

```sh
.venv/bin/python -m pytest \
  tests/test_agent_harness.py \
  tests/test_agent_lifecycle.py -q
```
