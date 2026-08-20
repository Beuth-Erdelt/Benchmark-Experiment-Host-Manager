# Contract-driven benchmark agent

This is the complete description of the prototype pipeline: its two contracts,
phase and context boundaries, tools, deterministic enforcement, optional local
lifecycle wrapper, replay rules, evidence, and known limits. For commands only,
see [README.md](README.md).

The prototype demonstrates a bounded autonomous experimenter, not a general
agent framework. Its implemented catalog slice is TPC-H with PostgreSQL and
PgDuckDB. Bexhoma executes experiments through its normal entry point; agent
policy remains in `agent/`.

## Annotated end-to-end flow

```mermaid
flowchart TB
    classDef human fill:#eef2ff,stroke:#4f46e5,color:#111827
    classDef model fill:#ecfeff,stroke:#0891b2,color:#111827
    classDef guard fill:#fff7ed,stroke:#ea580c,color:#111827
    classDef backend fill:#f0fdf4,stroke:#16a34a,color:#111827
    classDef artifact fill:#f8fafc,stroke:#64748b,color:#111827
    classDef local fill:#fdf4ff,stroke:#a21caf,color:#111827

    Q([Research question]):::human

    subgraph L[Optional local test lifecycle · dev/agent_lifecycle.py]
        direction TB
        L0[Start or resume one investigation]:::local
        LU[Ensure vLLM is UP<br/>retry until shared GPU is available]:::local
        LD[Ensure vLLM is DOWN<br/>wait until pod is deleted]:::local
        LW[Poll exact experiment code<br/>report or failed process]:::local
        LF[Final cleanup: vLLM DOWN<br/>also on error or Ctrl-C]:::local
    end

    subgraph D[1 · DESIGN context · agent.py + prompts.py]
        direction TB
        D1[Read the complete input contract<br/>catalog + target environment]:::model
        D2[Author one experiment YAML<br/>inside the inbox only]:::model
        D3{validate_spec<br/>parse → catalog → environment → methodology}:::guard
        D4[Repair first reported error<br/>bounded validation attempts]:::model
        D5{submit exact validated bytes}:::guard
        D1 --> D2 --> D3
        D3 -- rejected --> D4 --> D2
        D3 -- accepted --> D5
    end

    subgraph B[2 · EXECUTE · existing Bexhoma path]
        direction TB
        B1[experiment.py<br/>catalog resolution and dispatch]:::backend
        B2[Detached benchmark<br/>serialized by result-root lock]:::backend
        B3[Write raw evidence and tiered report]:::backend
        B1 --> B2 --> B3
    end

    subgraph I[3 · INTERPRET evidence context · fresh model window]
        direction TB
        I1[Read report/index.md first<br/>consult archived result contract]:::model
        I2[Establish validity before metrics<br/>open targeted evidence only]:::model
        I3[Optional deterministic table reduction<br/>compare_query_latency]:::guard
        I4{Record every explicit question<br/>settled · partial · unresolved}:::guard
        I1 --> I2 --> I3 --> I4
    end

    subgraph F[4 · FOLLOW-UP gate · two fresh model windows]
        direction TB
        F0{Useful unresolved question<br/>and budget remaining?}:::guard
        F1[Decision context<br/>reread catalog + environment]:::model
        F2{record_followup_decision<br/>finish or followup}:::guard
        F3[Authoring context<br/>reread inputs; write → validate → submit]:::model
        F0 -- yes --> F1 --> F2
        F2 -- followup --> F3
    end

    A([Final aggregated answer.md]):::artifact
    P[(reports/<br/>one report per phase)]:::artifact
    T[(one trajectory.jsonl<br/>append-only across all phases)]:::artifact
    C[(Input contract<br/>contract_catalog.yml + environment.yml)]:::artifact
    R[(Result folder<br/>experiment + archived contracts + report + provenance)]:::artifact

    Q --> L0 --> LU --> D1
    C -. read by model .-> D1
    C -. enforced by code .-> D3
    D5 --> B1
    D5 -. immutable copy + hashes .-> T
    B3 --> R
    B3 -. submitted code .-> LD --> LW
    LW -- report finished --> LU --> I1
    R -. authoritative evidence .-> I1
    I4 --> F0
    F0 -- no --> A --> LF
    F2 -- finish --> A
    F3 -- new code --> B1

    D1 -. logged .-> T
    I1 -. logged .-> T
    F1 -. logged .-> T
    F3 -. logged .-> T
    D5 -. phase account .-> P
    I4 -. phase interpretation .-> P
```

The purple lifecycle lane is local operator automation. It is not visible to
the model, imported by the agent, or required by the paper prototype. Without
it, an operator or scheduler invokes the same durable phases separately.

## The two-sided contract

The input side defines what may be run. The output side defines what may be
concluded.

| Side | Authoritative artifacts | Guarantee |
|---|---|---|
| Design | `contracts/contract_catalog.yml`, `dev/catalog/environment.yml` | Legal schema, supported workloads/systems/knobs, experimental guidance, node and storage availability, resource ceilings |
| Result | Archived `contract_result.yml`, `report/index.md`, linked evidence and raw provenance | Result layout, validity checks, metric meanings, identifiers, versions, and interpretation rules |

Prompts contain role, phase, tools, budgets, and stopping conditions. Domain and
deployment facts remain in files the model must read, which makes contract
consultation measurable in the trajectory.

## Runtime sequence and modules

| Step | Code used | Responsibility and durable output |
|---|---|---|
| CLI setup | `agent/harness/agent.py::main` | Creates one investigation at design; later phases reopen it and append to its trajectory |
| Model exchange | `model_client.py::ChatModel` | Calls an OpenAI-compatible endpoint; parses tool calls; logs but does not replay reasoning |
| Design instructions | `prompts.py::design_messages` | Requires contract reads, one attributable design, validation, and submission |
| Tool boundary | `tools.py::Workspace` | Canonical read/write scopes; complete-file writes; structured tool errors |
| Agent validation | `validation.py::validate_spec` | Shape, catalog, environment, and methodology checks; expanded run count |
| Shared resolution | `bexhoma/spec.py` | Existing profile, override, quantity, environment, and command resolution |
| Submission | `tools.py::submit`, `submit.py` | Fingerprint check, immutable copy, code allocation, result-root lock, agent-side catalog launch adapter, provenance archive |
| Execution | Normal Bexhoma workload modules | Workload execution, raw files, validity results, tiered report; no Bexhoma code modification required |
| State recovery | `agent.py::_carry_forward` | Rebuilds question, exact specification, code, budget, and previous-result handoff from trajectory data |
| Evidence interpretation | `prompts.py::interpret_messages`, `agent.py::run_interpret` | Fresh read-only context; validity-first analysis; structured question coverage |
| Deterministic comparison | `tools.py::compare_query_latency` | Matched-run TPC-H per-query reduction without model arithmetic |
| Follow-up decision | `prompts.py::followup_decision_messages` | Fresh read-only context; complete design-space reread; finish/follow-up record |
| Follow-up authoring | `prompts.py::followup_author_messages` | Fresh mutation context; same write/validate/submit boundary as design |
| Local automation | `dev/agent_lifecycle.py`, `dev/model_server.sh` | Optional vLLM switching, result polling, retry, resume, and cleanup |

One reusable loop, `agent.py::_converse`, drives every model context with a
different prompt, tool list, stopping predicate, and budget. A text answer is
rejected when the phase still requires a structured record.

## Capability boundary

The model never receives a shell, Kubernetes client, network client, or general
filesystem access. Tools are exposed by context:

| Context | Tools |
|---|---|
| Design | `read_file`, `write_file`, `validate`, `submit` |
| Evidence interpretation | `read_file`, `compare_query_latency`, `list_results`, `record_interpretation` |
| Follow-up decision | `read_file`, `record_followup_decision` |
| Follow-up authoring | `read_file`, `write_file`, `validate`, `submit` |

Writes resolve to one YAML file directly inside the inbox. Reads resolve only
inside contracts, the inbox, the configured result root, or explicitly allowed
environment files. Canonicalization happens before authorization, blocking
`..` and symlink escapes.

Successful validation stores a fingerprint of the specification, catalog, and
environment. Submission recomputes it and refuses changed bytes. The result
folder archives those exact inputs, while the trajectory records their hashes.

## Phase state and follow-ups

Each process performs one durable phase and exits, but all processes belonging
to the same question share one investigation directory and trajectory:

1. Design ends after submission and records the experiment code.
2. Execution is detached and owns the result-root lock.
3. Interpretation reopens the investigation only after its exact report exists
   and appends its events to the same `trajectory.jsonl`.
4. With budget, evidence, follow-up selection, and follow-up authoring use
   separate context windows and separate file-read allowances.
5. A submitted follow-up ends that invocation. Its result is interpreted by a
   later process with a bounded handoff reconstructed from the same trajectory.

The follow-up count is persisted in outcomes. A successful submission consumes
one unit. The loop ends when interpretation is complete without a new code.

## User-facing answer contract

Every phase response is preserved under `reports/`. The top-level `answer.md`
is not an intermediate status file: it is written only when an interpretation
finishes without submitting another experiment. That final interpretation is
required to aggregate the complete study, and the harness copies it verbatim;
it does not silently rewrite or correct model output. Interpretation prompts
require the report to be self-contained and use this order:

1. original question;
2. hypothesis;
3. experiments performed;
4. validity;
5. results;
6. interpretation;
7. follow-up rationale and intervention, when present;
8. final verdict and remaining limitations.

The final context receives the current specification, the preceding
specification and report, the previous interpretation, and the structured
follow-up decision. This gives the model the complete study chain needed to
write those sections. The investigation also contains `task.txt`, immutable
per-phase submission/log artifacts under `phases/`, all phase accounts under
`reports/`, and one append-only `trajectory.jsonl` for the whole chain.

## Local lifecycle wrapper

`dev/agent_lifecycle.py` implements the phase re-entry loop for this cluster's
testing only. It calls the public agent CLI and reads only trajectories, status
files, and reports. Neither the agent nor Bexhoma imports it.

For a new question it performs:

```text
vLLM up → design → vLLM down → wait for report
        → vLLM up → interpret
        → [follow-up code: vLLM down → wait → vLLM up → interpret]*
        → final answer → vLLM down
```

The low-level switch refreshes the local OIDC login noninteractively, applies
the pinned vLLM manifest, waits for readiness and the local API, and waits for
pod deletion on shutdown. The wrapper retries startup indefinitely by default
because releasing a shared GPU creates a race: another workload can take it
before interpretation begins. Set a finite `--server-start-attempts` to fail
instead. `--resume` continues a submitted investigation without submitting it
again. The `finally` block requests shutdown after success, failure, or
interruption; the weights PVC is retained.

Autonomous switching does not mean guaranteed immediate capacity. If every H200
is allocated, the vLLM pod remains Pending and interpretation waits until a GPU
returns. Kubernetes priority or a reserved GPU would be required for a bounded
restart time.

## Placement and replay

The definitive submitted specifications contain:

```yaml
placement:
  sut: cl-worker36
  loading: cl-worker36
  benchmarking: cl-worker36
```

These are literal Kubernetes node names selected from the original
`environment.yml`. A different cluster usually has no node named
`cl-worker36`, so its validator correctly rejects the unchanged file. This is
the local placement referred to in the reproducibility assessment.

There are three useful replay levels:

1. **Audit the original run.** Keep the submitted file unchanged beside its
   archived environment and result evidence. It records exactly what ran.
2. **Repeat the same experimental design elsewhere.** Copy the specification,
   replace each placement value with a node from the target's freshly generated
   environment, or omit `placement` so the target scheduler chooses. Revalidate
   before submission. This changes deployment binding, not the workload,
   treatment, resources, rounds, or repetitions.
3. **Let the agent adapt the design.** Generate the target environment and ask
   the original question again. The agent chooses legal placement from that
   descriptor and produces a new auditable specification.

This working tree also carries local `nodeSelector` edits in several Kubernetes
templates. They intentionally force this test cluster onto `cl-worker36` and
must not be included in a portable release. Removing placement from YAML is not
enough while those local template overrides remain. A portable repository must
leave templates unpinned and let the experiment's placement flags, or the
target scheduler, supply the binding.

An unchanged byte-for-byte specification can run elsewhere only if the target
also exposes the same node names and compatible resources. For a future
portable replay format, abstract roles such as `sut-node` would need a separate
per-cluster role-to-node binding; the current schema uses literal names.

## Evidence from the definitive run

The unedited successful chain predates the single-investigation layout and is:

| Role | Trajectory | Outcome |
|---|---|---|
| Initial design | `20260819T233939862899` | Submitted `1787175665`; one follow-up remained |
| First interpretation and follow-up | `20260820T003559431500` | Recorded comparison unresolved; submitted `1787179264` |
| Final interpretation | `20260820T015516527941` | Recorded every explicit question settled; final answer |

Both reports passed all seven validity checks. For each experiment, the
submitted YAML and archived `experiment.yml` had identical SHA-256 hashes. One
premature prose completion was rejected until the model called
`record_interpretation`, directly demonstrating enforcement rather than prompt
compliance alone.

The historical final `answer.md` predates both the self-contained answer
contract and the single-investigation layout. Its surrounding study record is
split across the three trajectory directories,
their two submitted YAML files, the first interpretation/follow-up answer, and
the two external result reports. Historical model output remains unchanged.

This supports the paper claim that, given machine-readable input and result
contracts, a tool-bounded agent can design, validate, submit, interpret, and
follow up on a supported benchmark while preserving an auditable record across
process boundaries.

## Known limits

- The catalog implements a narrow prototype surface, not every Bexhoma workload
  and system.
- Duration estimation is not calibrated.
- Environment validation checks declared capacity and may lack current free
  capacity.
- The filesystem lock serializes harness launches on one host/result root, not
  direct Bexhoma commands or cluster-wide submissions.
- Cross-experiment validity remains an interpretation responsibility.
- Exact cross-cluster numbers require pinned images and package versions plus
  captured hardware, storage, and runtime conditions.
- Temperature zero does not guarantee identical model decisions; exact model
  weights, tokenizer, and serving configuration are not archived by the
  trajectory.
- The optional local lifecycle can wait for shared GPU capacity but cannot
  create or reserve it.

## Documentation ownership

- This file is the single full pipeline and decision description.
- [README.md](README.md) is the single quick-start guide.
- `contracts/contract_catalog.yml` and `contracts/contract_result.yml` are the
  normative machine-readable interfaces.
- `docs/Design-Catalog-Contract.md` and `docs/AgentResultContract.md` explain
  the broader reusable Bexhoma contracts.
- `docs/FEATURES.md` is historical traceability, not another user guide.
