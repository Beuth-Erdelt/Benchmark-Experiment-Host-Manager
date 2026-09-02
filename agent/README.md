# Benchmark agent quick start

The prototype turns a research question into a catalog-valid benchmark,
submits it through Bexhoma, interprets the finished report, and may submit a
budgeted follow-up. See [ARCHITECTURE.md](ARCHITECTURE.md) for the full annotated
pipeline, contracts, module map, replay rules, and limitations.

## The short path

Six commands take a fresh checkout from nothing to an answered question. Each
one is explained in full further down; the sections after
[One-command local lifecycle](#one-command-local-lifecycle) are operator
reference material — self-hosting the model server, the unattended Kubernetes
Job, driving the phases by hand, and replaying a run elsewhere — and are not
needed for a first run.

```sh
# 1. install with the agent extra, which ordinary bexhoma use does not include
python3 -m venv .venv && .venv/bin/pip install -e ".[agent]"

# 2. point bexhoma at the cluster, then edit the copy
cp k8s-cluster.config cluster.config

# 3. describe the cluster the agent will design against
.venv/bin/python -m bexhoma.environment --output dev/catalog/environment.yml

# 4. choose the model endpoint, then edit the copy
cp .env.example .env

# 5. answer a question end to end: design, benchmark, interpretation, follow-up
.venv/bin/python dev/agent_lifecycle.py --task "<benchmark question>" --followups 1

# 6. continue an investigation whose benchmark was already submitted
.venv/bin/python dev/agent_lifecycle.py --resume <result-folder>/agent/<run-id>
```

The run prints the investigation directory it writes to and, at the end, the
path of the final verdict. To check the installation without a cluster, run the
test suite in [Verification](#verification).

## Prerequisites

1. Create an environment and install the repository **with the agent extra**.
   The agent needs a client for its OpenAI-compatible server that ordinary
   bexhoma use does not, so a plain install will not run it:

   ```sh
   python3 -m venv .venv
   .venv/bin/pip install -e ".[agent]"
   ```

2. Configure bexhoma for the target cluster:

   ```sh
   cp k8s-cluster.config cluster.config   # then edit it
   ```

   The agent reads this file too, for the `resultfolder` that decides where
   results land. See the repository's configuration guide for the rest.

3. Provide an OpenAI-compatible model endpoint and the name it serves. The
   bundled self-hosted server below is one way; any such endpoint works.

4. Generate a current descriptor of the target cluster. Run this again whenever
   the cluster changes, since it is what grounds the agent's placement and
   sizing choices in reality:

   ```sh
   .venv/bin/python -m bexhoma.environment \
     --output dev/catalog/environment.yml
   ```

The active catalog is `contracts/contract_catalog.yml`. The current prototype
supports TPC-H with PostgreSQL and PgDuckDB, and YCSB with PostgreSQL.

Three documents govern a run. The catalog says what an experiment may express.
The result contract, `contracts/contract_result.yml`, says what may be claimed
from a finished result. The experiment design handbook, `agent/experiment_design_handbook.md`, says
what makes a design sound rather than merely legal: it is read before every
design and every follow-up, its digest is recorded in the trajectory, and the
few principles a machine can decide are enforced by the validator, which cites
them by identifier. `AGENT_METHOD` in `.env` says which handbook that is, and an
empty value designs without one, which is the other arm of the with/without
ablation. `--method` overrides the file for a single run, on the agent CLI and on
the lifecycle wrapper alike; any path that is not a file means no handbook.

## Choosing the model server

Three settings decide which server answers the agent: `AGENT_MODEL` is the name
the server serves the model under, `AGENT_BASE_URL` is its OpenAI-compatible
endpoint, and `AGENT_API_KEY` is the credential (the placeholder `EMPTY` for a
server that checks none). Copy `.env.example` in the repository root to `.env`
and edit it; the agent CLI and the local lifecycle wrapper both read that file
at startup. It is ignored by git, so real API keys stay out of the history. The
lifecycle wrapper also keeps the key in the child process's inherited
environment rather than copying it into a command-line argument visible to
process-listing tools.

An exported shell variable overrides the file, and a command-line flag
(`--model`, `--base-url`, `--api-key`) overrides both, so one run can use a
different server without editing anything.

`.env.example` carries a ready block for each backend we use: the bundled vLLM
server through a local port forward, the same server reached by its in-cluster
service name, a local Ollama, OpenAI, and Mistral. Ollama and Mistral serve the
same protocol under a `/v1` path, so nothing but these three values changes.

Two differences are worth knowing when you leave the self-hosted server. The
agent first resolves the configured model name against the endpoint's model
list. A dedicated endpoint advertising exactly one model may choose its own
identifier, which the agent adopts; an endpoint advertising several models
requires an exact configured match. The agent then asks how long a context it
accepts and shrinks each turn's
output budget to fit; servers name that figure differently, so both the vLLM
spelling and the hosted one are read. A server that publishes neither leaves the
agent on the fixed per-turn ceiling `--max-tokens` sets, which still works but
loses that safety margin. And a metered API refuses turns once a per-minute
quota is reached, where a self-hosted server would simply queue them, so a
refused turn is retried with a widening wait before the phase gives up.

One more setting decides who owns the endpoint. `AGENT_MODEL_SERVER=bundled`,
the default, means the lifecycle wrapper below starts and stops the vLLM server
around every phase. `AGENT_MODEL_SERVER=external` means the endpoint is already
there — a hosted API, or an Ollama running on your machine — so the wrapper
only chains the phases and never touches a server. Each block in `.env.example`
already carries the right value, and an exported `AGENT_MODEL_SERVER` overrides
the file for one shell, exactly as the three settings above do. The agent CLI
itself never starts a server in either case.

## Self-hosted model server

`agent/k8s/vllm-qwen38-27b.yml` and `dev/model_server.sh` run a vLLM server on
the cluster. They are a convenience, not part of the pipeline: any
OpenAI-compatible endpoint does. If you use them, four values are specific to
the cluster they were written for.

**Context and namespace** are environment variables, and the manifest itself
pins neither, so these decide where the server objects are created.

```sh
export MODEL_SERVER_CONTEXT="<kubeconfig context>"
export MODEL_SERVER_NAMESPACE="<writable namespace>"
```

The context defaults to the one on this development machine. The namespace has
no default and `dev/model_server.sh` refuses to run without it, because the
switch writes it into the kube context as well, where every later
namespace-less `kubectl` call inherits it; a default would quietly place both
the model server and the benchmark in whichever account that default named.
Export it for a direct call, or put `MODEL_SERVER_NAMESPACE` in `.env` when
`dev/agent_lifecycle.py` is driving the switch. The in-cluster lifecycle Job
needs neither: it reads its own namespace and passes that down.

Bexhoma must use the same namespace: set
`credentials.k8s.context.<kubeconfig context>.namespace` in `cluster.config` to
the same value. See the repository's main quick start and the configuration
guide for creating that cluster entry.

**Login** defaults to an OIDC helper script that exists on this machine only.
On a cluster reached through an ordinary kubeconfig there is nothing to refresh,
so point it at a no-op:

```sh
export KUBE_LOGIN_SCRIPT=/bin/true
```

**Storage class and GPU labels** are edited in the manifest, because no default
can be right for both clusters. Set `storageClassName` to one your account can
claim 150Gi from, and change the node affinity to match how your cluster labels
its GPU nodes. Both are commented in the file.

Getting the GPU labels wrong fails quietly rather than loudly: the pod stays
unschedulable, and startup waits for capacity by design instead of reporting an
error. When first bringing this up on a new cluster, pass
`--server-start-attempts 3` so a misconfiguration surfaces as a failure, and
check `kubectl describe pod` if it does.

## One-command local lifecycle

For this cluster's local testing, the wrapper starts vLLM for model phases,
stops it while benchmarks run, waits for the exact report, repeats the cycle for
a follow-up, and leaves the server down after the final answer:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python dev/agent_lifecycle.py \
  --task "<benchmark question>" \
  --followups 1
```

With `AGENT_MODEL_SERVER=external` in `.env` the same command drives Mistral,
OpenAI, or a local Ollama end to end: design, benchmark, interpretation, and an
approved follow-up run without anyone starting a phase by hand, and no server is
started or stopped along the way.

```sh
.venv/bin/python dev/agent_lifecycle.py --task "<benchmark question>"
```

The ablation's other arm is the same command with the handbook switched off,
either by leaving `AGENT_METHOD` empty in `.env` or for one run:

```sh
AGENT_METHOD= .venv/bin/python dev/agent_lifecycle.py --task "<benchmark question>"
```

Before the design phase, the wrapper also answers the question with the bare
model — no catalog, handbook, or tools — as its own investigation, so the full
pipeline's answer can be read against what the model alone would have said. Its
`answer.md` path is printed and referenced from the design trajectory. Skip it
with `--no-baseline`, or set `AGENT_BASELINE=0`. The same phase is available on
its own with `python -m agent.harness.agent --phase baseline --task "..."`.

Results land wherever `cluster.config` declares its `resultfolder`, which is the
same setting bexhoma itself reads, so the two cannot disagree. A relative value
there resolves against the repository. Override it for one run with `--results`,
or for a shell with `AGENT_RESULTS`.

The model pod accepts either the shared H100 or H200, whichever schedules first.
Startup retries indefinitely when neither has a free GPU. To fail
after a bounded number of attempts, add for example
`--server-start-attempts 3`. A zero benchmark timeout waits indefinitely; use
`--benchmark-timeout-seconds <seconds>` when unattended work needs a deadline.
If the submitted benchmark process is definitively failed or has exited without
a report, the wrapper invokes Bexhoma's experiment-scoped cleanup for that exact
code. It does not remove shared monitoring, dashboard, or message-queue objects.

After a terminal disconnect, resume an investigation that already submitted an
experiment without resubmitting it:

```sh
AGENT_MODEL=qwen3.8-27b \
.venv/bin/python dev/agent_lifecycle.py \
  --resume <result-folder>/agent/<run-id>
```

`dev/agent_lifecycle.py` and `dev/model_server.sh` remain usable as local
operator commands. The autonomous Job described below packages the same tested
phase loop and server switch behind in-cluster credentials; neither path changes
the model-facing agent interface.

If you run phases by hand instead of through the wrapper, nothing shuts the
model server down at the end. The pod covers that case itself: it releases the
GPU once twenty minutes pass without a request. Set `IDLE_SHUTDOWN_SECONDS` in
the manifest to change that window, or to `0` to keep the server up until
something deletes it. Running `dev/model_server.sh down` is still the quickest
way to hand the GPU back.

## Running two investigations at once

An agent-started run takes an exclusive lock on the result folder, so a second
run refuses to submit while the first is still benchmarking. That is a
measurement policy, not a filesystem constraint: BeXhoma already gives every
experiment its own directory, named by the experiment code. Serial execution is
the default because two benchmarks sharing a cluster measure each other.

Pass `--allow-parallel-runs` to the agent CLI to submit anyway. The run then
starts alongside the one already in flight and records that it did so in its
trajectory, so a later reader knows the timings were not taken on a quiet
cluster. Pin the two investigations to different nodes with `placement:` before
doing this, or the numbers will describe the interference rather than the
systems.

## Autonomous Kubernetes lifecycle

For an unattended investigation, use the Kubernetes Job in
`agent/k8s/lifecycle-controller.yml`. A Job is used instead of a bare Pod so
Kubernetes restarts the controller after a node or process failure. Its
persistent volume stores trajectories, status, and results. On restart, the
controller resumes the newest durable submission instead of designing and
submitting it again. If Kubernetes replaced the Pod during a benchmark, the
controller reacquires the shared run lock and resumes BeXhoma orchestration with
the same experiment code and immutable submitted specification.

Build and publish the controller image from the repository root:

```sh
docker build -f agent/Dockerfile.lifecycle \
  -t <registry>/bexhoma-agent:<tag> .
docker push <registry>/bexhoma-agent:<tag>
```

Put the question alone in `task.txt`. Create the two input files as a ConfigMap
in the writable namespace:

```sh
kubectl -n <namespace> create configmap agent-lifecycle-input \
  --from-file=cluster.config=cluster.config \
  --from-file=task.txt=task.txt
```

The supplied `cluster.config` remains the source of cluster-specific service,
port, storage-class, and monitoring settings. At startup, the controller writes
a private runtime copy with the Pod's namespace, service-account context, and
persistent result directory. If the source file contains more than one context,
set `AGENT_SOURCE_CONTEXT` in the Job to the entry whose cluster-specific
settings should be copied.

Before applying the manifest, edit these explicit portability values:

1. Replace the controller image placeholder.
2. Give the Job and `AGENT_LIFECYCLE_ID` the same new investigation name.
3. Set the ClusterRoleBinding subject namespace from `replace-me` to the target
   namespace. This read-only cluster permission lets the environment refresh
   list nodes, storage classes, and priority classes.
4. Set the lifecycle-state PVC's storage class if the cluster has no suitable
   default. Also apply the model-server storage and GPU-label choices described
   above.

Then apply and follow the controller log:

```sh
kubectl -n <namespace> apply -f agent/k8s/lifecycle-controller.yml
kubectl -n <namespace> logs -f job/<job-name>
```

The controller uses its service account directly, so it does not depend on a
workstation's expiring Keycloak or OIDC login. Its write authority is limited
to the selected namespace. The language model still receives only the catalog,
environment, result contract, and phase tools; it never receives Kubernetes or
terminal access.

Agent-submitted experiments also force BeXhoma's existing maximum active SUT
count to one. System configurations therefore load and benchmark sequentially.
This prevents comparison systems from sharing benchmark resources and prevents
two cold-cache generators from writing the same raw TPC-H directory. Query
streams within one active system remain concurrent according to `rounds`.

## Portable phase-by-phase operation

Design and submit:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase design \
  --task "<benchmark question>" \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

After the emitted experiment code has a finished `report/index.md`, continue
the same investigation:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase interpret \
  --run <result-folder>/agent/<investigation-id> \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

To interpret a result independently of local trajectory, status, or cluster
configuration files, point at its exact entry point. This is the portable form
of the supervisor's one-result workflow:

```sh
.venv/bin/python -m agent.harness.agent \
  --phase interpret \
  --report /path/to/results/<experiment-code>/report/index.md \
  --task "<question this experiment tests>" \
  --model "<served model>" \
  --base-url "<OpenAI-compatible endpoint>" \
  --followups 1
```

When `--task` is omitted, the harness uses the archived experiment's hypothesis
or title. Interpretation starts from that one report, follows only its local
links, and cannot read another experiment merely because it shares the same
result root.

Design and `--run` continuation take the result root from `cluster.config`
unless `--results` or `AGENT_RESULTS` overrides it. Standalone `--report`
interpretation derives the root from the selected result path when none is
configured.

If interpretation submits a follow-up, wait for that report and invoke the same
command with the same investigation path. Otherwise the investigation's
top-level `answer.md` contains the interpretation of the current result only.
Earlier result interpretations remain separate phase reports and are not
aggregated. Follow-up authoring receives only each ancestor's compact
`agent_summary.yml`, which records its hypothesis and bottom-line verdict; it
does not receive the earlier reports or their metrics. Use `--dry-run` to
design and validate without submission.

Validation reports both the expanded benchmark-phase count and a conservative
declared-timeout budget. The latter assumes every active query reaches its
per-query deadline, so it is a cost ceiling for comparing designs rather than a
prediction of elapsed time. When only particular queries remain unresolved, the
follow-up decision records those query numbers and authoring is required to use
the same `active_queries` subset. A full-workload follow-up remains possible,
but its decision must state why the broader cost is scientifically necessary.

Interpretation runs a deterministic quality and result assessment before
accepting the model's conclusion. Where query-level data exists, it separates
completion of the planned query set from speed on the common successful
queries, marks whole-workload throughput non-comparable when a planned query
errored, and surfaces unusually different repetitions as warnings. Independently
of workload name, it uses the archived `discriminates` factors to compute
ordered concurrency, CPU, and memory shapes and categorical system rankings.
The structured interpretation must reproduce those shapes, rankings, and
factor-level means exactly; it cannot call a measured rise a plateau or quote a
different value. Failed monitoring checks also carry exact affected phases and
whether performance metrics remain usable.

## Outputs

Investigations are written under the `agent/` subdirectory of the result folder
`cluster.config` declares, beside the benchmark results themselves, so a
checkout keeps no run artifacts of its own. Override the location with
`--trajectories`.

The design invocation first creates a timestamp-only working directory there.
After the design produces a valid experiment, the harness renames it to
`<result-folder>/agent/<timestamp>-sf<scale>-<model>/`, with characters that are
unsafe in a directory name replaced by hyphens. For example,
`20260827T111847490995-sf2-qwen3.8-27b` identifies the experiment scale and the
served model without opening the trajectory. An incomplete design remains
timestamp-only because it has no trustworthy scale factor. Every
interpretation and follow-up appends to the same directory:

- `trajectory.jsonl`: the append-only record of all phases, prompts, reasoning,
  tool calls, stages, hashes, budgets, and outcomes;
- `task.txt`: the original question;
- `phases/<number>-<phase>/`: immutable submitted specification, validation
  inputs, and Bexhoma log for that phase, when it submitted an experiment;
- `reports/<number>-<phase>.md`: each phase's own account;
- `answer.md`: created only after the final interpretation and containing its
  one-result answer according to the archived result contract.

Each submitted result folder archives the exact experiment, input catalog,
result contract, and environment descriptor used for validation.
After successful interpretation, it also contains `agent_summary.yml`: the
experiment code, `follow_up_of`, hypothesis, scientific verdict, technical
validity, and unresolved next question. Its evidence paths are relative to that
result folder so the lineage remains portable to another machine.
If Bexhoma takes longer than the startup wait to create that folder, the design
phase still returns its assigned code and records `starting`; the staged inputs
are copied into the folder when it becomes observable.

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
