# Prototype Architecture — AI-Conducted Benchmarking Demo (v0.1)

Two tracks, one filesystem. Bexhoma-side (M1–M5, cluster required) and
agent-side (harness, no cluster required) meet only through the
directories and file formats below. This document IS the interface
agreement between the two tracks.

## Directory layout

```
ai-ready-bexhoma/
├── contracts/                  # static, versioned in git
│   ├── workloads.md            # M1: input contract (intent catalog,
│   │                           #     conventions, worked examples)
│   ├── results.md              # M3: result contract (entry point,
│   │                           #     tiers, naming legend)
│   ├── experiment.schema.json  # single source of truth for the spec:
│   │                           #     authored in M1, enforced by M5
│   └── VERSION                 # e.g. "0.1" — logged per trajectory
├── environment/
│   └── environment.yml         # M2: generated from the cluster
│                               #     (hand-written in mock mode)
├── inbox/                      # agent → bexhoma
│   └── <name>.yml              # specs submitted by the agent
├── status/
│   └── <code>.json             # one file per experiment, see format
├── results/
│   └── <code>/                 # bexhoma result folder per experiment
│       ├── experiment.yml      # provenance copy of the submitted spec
│       ├── summary.md          # M4: entry point with links
│       ├── query_times_<connection>.csv
│       ├── metrics/…
│       └── logs/…
├── trajectories/
│   └── <run-id>/               # one per agent run (timestamp id)
│       ├── task.txt            # the user task, verbatim
│       ├── trajectory.jsonl    # full event log (see format)
│       └── report.md           # the agent's final answer
└── harness/
    ├── agent.py                # the loop (stateless per invocation)
    ├── tools.py                # the five tools + path policy
    ├── llm.py                  # model adapter (hosted | local)
    └── mocks/                  # stub validator, canned result folders
```

## The five tools (the whole agent API)

| tool | signature | write/read scope |
|---|---|---|
| read_file | (path) → text | contracts/, environment/, results/, own trajectory dir |
| write_file | (path, text) → ok | inbox/, own trajectory dir ONLY |
| validate | (spec_path) → JSON verdict | runs M5 dry-run (or stub) |
| submit | (spec_path) → experiment code | moves spec to bexhoma (or mock) |
| list_results | () → [{code, state, title}] | reads status/ |

Rules enforced by the harness, not requested from the model:
- All paths canonicalized and checked against the scope table; no
  shell, no network, no kubectl. The whitelist IS the contract
  boundary.
- read_file calls are logged with byte counts → context economy
  becomes measurable per trajectory (which tiers did the agent read?).

## File formats

**status/<code>.json** (written by the bexhoma side / mock):
```json
{ "code": "1758291234",
  "state": "benchmarking",     // validated | loading | benchmarking
                               // | finished | failed
  "title": "join performance under memory limits",
  "spec": "results/1758291234/experiment.yml",
  "summary": null,             // path once finished
  "updated": "2026-09-20T14:03:11Z" }
```

**validate verdict** (M5 / stub — same shape):
```json
{ "valid": false,
  "errors": [
    { "path": "queries",
      "constraint": "subset of [1..22] for workload tpch",
      "got": [5, 7, 23],
      "hint": "23 is not a TPC-H query" } ],
  "estimate": { "runs": 12, "duration_min": 210 } }
```

**trajectory.jsonl** (one JSON object per line, written by harness):
```json
{"ts":"…","type":"meta","model":"<id>","params":{"temperature":0},
 "contract_version":"0.1"}
{"ts":"…","type":"llm_request","phase":"design","messages_ref":"…"}
{"ts":"…","type":"tool_call","tool":"read_file",
 "args":{"path":"contracts/workloads.md"},"bytes":8123}
{"ts":"…","type":"tool_call","tool":"validate",
 "args":{"path":"inbox/join-study.yml"},"result":{"valid":false}}
```

## Agent loop (stateless, event-driven)

```
task.txt ──► invoke(agent, transcript=[])          PHASE: design
               agent reads contracts + environment,
               writes inbox/<name>.yml, calls validate
               ├── invalid → repair (same invocation)
               └── valid   → submit → code → EXIT
status/<code>.json state=finished (watcher / cron)
        ──► invoke(agent, transcript=prior+event)   PHASE: interpret
               agent reads summary validity-first,
               drills into flagged tier-2 files,
               DECISION: report.md  → EXIT (done)
                      or one follow-up spec → submit → EXIT
status finished ──► invoke(...)                     PHASE: conclude
               report.md with file-path citations → DONE
```

- The agent has no memory between invocations; the transcript replayed
  from trajectory.jsonl is the memory. This is what makes long-running
  experiments (hours) compatible with an LLM session (minutes) — and
  it mirrors real standing-capability operation.
- Follow-up budget: max 1 iteration for the demo (hard-coded).

## Mock mode (agent track works without Bexhoma or a cluster)

- `validate` → scripted stub: first call returns a prepared rejection
  (teaches/repairs), second call valid. The agent cannot distinguish
  a scripted rejection from a real one — self-correction is fully
  testable offline.
- `submit` → writes status/<code>.json, waits N seconds, drops a
  CANNED result folder (ideally an anonymized real one from the
  archive) and flips state to finished.
- Friction found while writing the mocks ("can't tell which file has
  per-query times") is contract feedback for M1/M3 — for free.

## Integration day (late September)

Swap three things, change nothing else: stub validate → M5 CLI,
mock submit → real submission, canned folders → live results/. If the
harness needs any other change, the interface leaked — which is
itself a finding for the paper.

## Protocol decisions (fixed BEFORE the first archival run)

- Model: develop against a strong hosted model; attempt the archival
  run with pinned open-weights (temperature 0) for replayability.
  Report whichever carried the run, verbatim.
- Reporting rule: first complete trajectory is the artifact; aborted
  runs are counted and disclosed.
- Archive: trajectories/<run-id>/ + results/<code>/ folders + contract
  files at their VERSION → Zenodo DOI.
