# Plan: publication bundle (redacted export of runs)

Status: **planned, nothing implemented** (2026-10-10). This is a future
extension, separate from the study plan (`dev/plan-studies.md`) and not
required by it. Related to issue #795.

## Goal

Turn one or more runs into a directory that can be published, e.g. on Zenodo
with a DOI (#795):
- nothing secret in it;
- no local or personal identifiers;
- no absolute paths;
- every file accounted for with a hash.

The uploading itself stays a manual step.

Issue #795 asks for a bundle of:
- the input contracts and the generated `experiment.yml`;
- the answer;
- the full result folder;
- the trajectories;
- a README framing the work as feasibility, not reliability.

## Decoupling

The exporter is a standalone tool. It does not import `agent.harness`, and
it does not need the study program.

- **Input is a list of directories, each with a role.** A role decides how
  the directory is copied:
  - `--result <dir>`: a Bexhoma result folder, copied in full;
  - `--trajectory <dir>`: an agent investigation or study directory, copied
    in full;
  - `--summary-only <dir>`: a result folder from which only
    `agent_summary.yml` is copied. Use it for cited experiments, which are
    context.
- **`--from-study <dir>` is a convenience, not a dependency.** If a study
  directory has a `study.yml` (from the study plan), the exporter fills the
  lists from it:
  - the study directory as a trajectory;
  - each experiment as a result;
  - each citation as summary-only.

  It depends only on the documented file format, not on code. Without
  `study.yml` (every run today, including the #795 demo chain split across
  three trajectory directories), the lists are given explicitly.
- **It works on plain Bexhoma results too.** A result folder without any
  agent can be exported the same way, so the tool is useful beyond the agent.
- **Location:** `scripts/publish_bundle.py`, with its rules in
  `scripts/publish_rules.yml` and tests in `tests/test_publish_bundle.py`.
  No changes to `bexhoma/` or `agent/` are needed.

## Bundle layout

```text
<name>/
  README.md               # generated skeleton; feasibility framing filled in by hand
  BUNDLE.yml              # what was included, with which role, from which source name
  MANIFEST.yml            # every file: bundle path, sha256, size, redacted/filtered yes/no
  REDACTIONS.md           # categories and counts replaced, never the values
  trajectories/<dir name>/
  results/<code>/
  summaries/<code>/agent_summary.yml
```

Never included, whatever the input:
- the shared status registry;
- the inbox, which holds drafts of other runs;
- `cluster.config`;
- kubeconfig files;
- `.env`.

## What is sensitive: findings from a real run

From study `20261010T192117351586` and its result `1791653201` (277 files):

| category | example found | where | handling |
|---|---|---|---|
| **Credentials** | none found. The DB auth is `['postgres', '']`, the stock default; `BEXHOMA_PASSWORD` is set empty; the model `api_key` is not logged | `connections.config`, pod `*.yml`/`describe.log` | **fail closed:** a scan refuses the export on any credential pattern (below) |
| **Absolute local paths** | `C:\data\benchmarks\agent\…`, `C:\data\benchmarks/1791653201` | `trajectory.jsonl` (submit, outcome, artifact, baseline events), `bexhoma.log`, reasoning traces | rewritten to `<results>/…`, `<trajectories>/…`, `<repo>/…` |
| **Personal identifier** | namespace `perdelt` (a user handle), ~3,500 hits in 194 files, including pod names, service DNS and Prometheus queries | almost everywhere | replaced by `<namespace>` |
| **Public node IPs** | `cl-worker24/141.64.3.224` | every `*.describe.log` | replaced by `<node-ip>` |
| **Cluster inventory** | `environment.yml` lists all 17 nodes, with labels, capacity, occupancy, kernel and OS | result `environment.yml`, `phases/*/submitted-environment.yml` | **only the nodes the run used are kept** (decided 2026-10-10; see below) |
| **Node names** | `cl-worker24`, `cl-worker36`; the reasoning also names `cl-worker27`, which was considered but not used | environment, placement, describe logs, trajectory, reasoning | pseudonymized **consistently** across all files (`cl-worker24` → `node-01`), so "same node" still reads correctly; this also covers names in prose |
| **Kube context, storage secrets** | context `oidc_ds_cluster`; CSI secret *names* in storage-class parameters | `environment.yml` | context → `<context>`; secret-name parameters dropped, the rest of the storage class kept |
| **Pod IPs** | `10.244.21.106`, … (private cluster range) | describe logs | replaced by `<pod-ip>` |
| **Internal endpoints** | `http://localhost:8001/v1` (model server), `*.svc.cluster.local` | trajectory `meta.params.base_url`, connection configs | host replaced by `<model-endpoint>`, `<service>`; the path is kept |
| **Process data** | PIDs, Kubernetes `Audit-Id` headers in a 401 response | trajectory submit result, `bexhoma.log` | kept; not sensitive |
| **Free text** | the question (`task.txt`), the model's reasoning and answers | trajectory, `reports/` | same replacements, and flagged in `REDACTIONS.md` for **manual review**: a question can contain anything |
| **Kept on purpose** | image tags and `sha256:` digests (describe logs), harness commit and source hashes, model id, contract hashes | — | kept as reproducibility evidence. The digests even fill a `known_gaps` entry in `contract_result.yml` |

Credential patterns that refuse the export:
- JWT-shaped strings (`eyJ…`) and `Bearer …`;
- PEM blocks (`-----BEGIN … KEY-----`);
- kubeconfig keys (`client-key-data`, `token:`, `client-certificate-data`);
- non-empty values of `password`, `api_key`, `AGENT_API_KEY`,
  `BEXHOMA_PASSWORD` or `POSTGRES_PASSWORD`;
- known cloud key prefixes (`AKIA…`, `sk-…`).

A hit names file and line, never the value. The operator removes the file or
passes a reviewed `--allow <file:line>`.

**Licensing, not secrecy:** the bundle contains TPC-H query text and results,
and the TPC EULA does not allow presenting them as TPC-H benchmark results.
The README skeleton states that the workload is derived from TPC-H and that
its numbers are not comparable to published TPC-H results.

## Only the nodes the run used

- **The used set is derived from where pods actually ran**, not from the spec.
  In the example, `placement` pins `cl-worker36`, but the benchmarker pods
  ran on `cl-worker24`. The used set is the union of:
  - every `Node:` line in the result folders' `*.describe.log`;
  - every `placement` value in the included `experiment.yml` and
    `submitted-experiment.yml` files. A pinned node that never got a pod is
    still part of the design.
- **What is filtered:** every `environment.yml` copy in the bundle keeps
  `nodes[]` entries for the used set only. The rest of the descriptor stays
  as it is, with the redactions above: contract version, `storage_classes`,
  `monitoring`, priority classes.
- **What is recorded:** `BUNDLE.yml` and `REDACTIONS.md` record how many
  nodes were removed, not which ones.
- **Prose is not filtered.** Node names elsewhere, such as in the model's
  reasoning, are pseudonymized like every other name. Their details are gone
  with the filtered descriptor.

## Cleanup routine

One routine, driven by the rule table in `publish_rules.yml`, runs over every
copied text file **and over every file and directory name**. No names hit in
the example run, but pod and job names can carry the namespace in other
setups.

### What it replaces

| target | how it is matched | replacement |
|---|---|---|
| namespace | the value from the run's own records (`environment.yml` `cluster.namespace`), as an exact token with word boundaries. Not a guess from a pattern | `<namespace>` |
| node names | the list of **all** `nodes[].name` in the original `environment.yml`, plus every `Node:` and `kubernetes.io/hostname` value in the describe logs. Driven by that list, so other clusters' naming schemes work too; a regex like `cl-worker\d+` would not | `node-01`, `node-02`, … in a stable order, consistent across all files |
| node IPs | the IP after `Node: <name>/` and in Prometheus `instance=` labels; any IPv4 or IPv6 outside the pod range | `<node-ip>` |
| pod IPs | addresses in the pod CIDR (`10.244.0.0/16` here, taken from the describe logs) | `<pod-ip>` |
| kube context | `environment.yml` `cluster.context` | `<context>` |
| storage secret names | storage-class parameters whose key contains `secret` | removed |
| endpoints | the model server's `base_url` host from the trajectory; `*.svc.cluster.local`; any other URL host not on a short allowlist (`postgresql.org`, `github.com`, …) | `<model-endpoint>`, `<service>`, `<host>` |
| absolute paths | the input directories, the result root, the checkout and the home directory as prefixes | `<results>/…`, `<trajectories>/…`, `<repo>/…`, `<home>/…` |

### What it keeps on purpose

- **Author and copyright headers.** The SQL scripts in the result folder carry
  `-- Authors: Patrick K. Erdelt` / `-- Copyright (C) 2020 …`. That is
  licence attribution, not leaked identity. This is also why the namespace
  rule is an exact token: `perdelt` must not touch `Erdelt`.
- **Kubernetes UIDs and container IDs** (369 UIDs and 156 `containerd://` IDs
  in the example). They are random, identify nothing outside the run, and tie
  the logs to each other.
- **Image tags and digests, commits, model ids, contract hashes.** These are
  reproducibility evidence.
- **Timestamps.** They are needed to read the run, and the trajectory's order
  depends on them.
- **Occupancy of the used nodes** (`free`/`requested` in `environment.yml`).
  It is what the design saw. It aggregates other workloads on those nodes,
  but names none of them.
- **Hardware labels** such as `cpu: e5-2630` or `gpu: k80`. They describe
  what the numbers were measured on.

### Leftover checks: refuse unless allowed

After redaction, the copies are scanned again. Any hit stops the export, names
file and line but never the value, and the output directory is deleted. A
reviewed `--allow <file:line>` lets a single hit through.

- **Credentials:** the patterns listed above.
- **Absolute paths:** any drive-letter path, `/home/…` or `/Users/…` that no
  prefix rule covered.
- **The exporting machine's identity:** the computer name (`COMPUTERNAME`,
  `HOSTNAME`) and the login name (`USERNAME`, `USER`) as tokens, excluding
  author and copyright lines. None were found in the example, but a
  traceback or a pod's environment could carry them.
- **Any redaction target still present**, e.g. a node name that appeared in a
  form the rules missed.
- **Binary files:** the same targets as bytes. Today's result folders are
  text only (`.log`, `.yml`, `.config`, `.json`, `.md`, `.txt`, `.jsonl`).
  A future binary such as a pickle, parquet or archive cannot be redacted, so
  a hit in one refuses the export instead of shipping it unchanged.

### Manual review, always

`REDACTIONS.md` lists the files that need a human read whatever the scan
says:
- `task.txt`, because a question can contain anything;
- the reasoning traces and answers, because the model paraphrases;
- any file with an `--allow`.

## Rules

- **No absolute paths in the bundle.** Every absolute path whose prefix is a
  given input directory, the result root or the checkout is rewritten to a
  placeholder plus a relative path. Any remaining drive-letter or
  `/home/`/`/Users/` path is a **refusal**, like a credential, until it is
  covered by a rule or an `--allow`.
- **One pseudonym mapping per export.** The mapping (`cl-worker24` →
  `node-01`, …) goes to `redaction-map.yml` **beside** the output directory,
  never inside it, so only the owner can reverse it.
- **Integrity across redaction.** Trajectories carry hashes of the original
  catalog and environment, and a redacted or filtered file no longer matches
  them.
  - `MANIFEST.yml` lists the exported hash of every file and marks
    redacted/filtered ones.
  - The private `redaction-map.yml` keeps the original hashes, so the owner
    can prove the bundle derives from the archived originals.
  - The README states that hashes inside trajectories refer to the
    unredacted originals.
- **Read-only on the sources.** The tool copies, then redacts only the
  copies.
- **Text files only are redacted.** Binary files are copied as they are and
  listed in `REDACTIONS.md` as not redacted. Each one is still scanned for
  credential patterns as bytes.
- **Output is a directory, not an upload**, so it can be reviewed before it
  leaves the machine.

## Implementation sketch

`scripts/publish_bundle.py`, standard library plus PyYAML:

```text
python scripts/publish_bundle.py --out <dir> --name <bundle name>
    [--from-study <dir>]
    [--trajectory <dir>]... [--result <dir>]... [--summary-only <dir>]...
    [--allow <file:line>]...
```

1. **Collect.** Resolve the inputs, through `study.yml` when `--from-study`
   is given. Refuse an input that doesn't exist. Apply the never-include
   list.
2. **Copy** into `<out>/<name>/` under the role directories.
3. **Scan** the copies for credentials and leftover absolute paths. Stop on
   any hit not in `--allow`.
4. **Derive the used node set** from the describe logs and the placements.
5. **Filter** every `environment.yml` copy to that set.
6. **Redact** the text files with the rule table in `publish_rules.yml`
   (`category, pattern, replacement`). The node mapping is built once, from
   every node name seen in all files, in a stable order.
7. **Write** `BUNDLE.yml`, `MANIFEST.yml`, `REDACTIONS.md`, the README
   skeleton and the outside `redaction-map.yml`.
8. **Verify:** run the scan again on the result. It must be clean, or the
   tool deletes the output and fails.

The rule table is the single source for redaction, for `REDACTIONS.md` and
for the tests.

## Optional upstream change: relative paths at write time

The exporter does not need this, because it rewrites paths itself. It makes
records portable at the source, and is a small change to the harness:
- `tools.py::submit`'s result (`log`, `spec`), the `outcome.submitted_spec`
  of `run_design`/`run_interpret`, and the artifact event of `_write_reports`
  record paths relative to the study directory or the result root.
- The readers (`_carry_forward`, `_resolve_spec_reference`,
  `lifecycle.py::_read_phase_state`) accept both forms.
- The interpretation prompt still names the report by its absolute path.
  Changing what the model sees is a separate decision.

## Tests

- No `C:\`, `/home/`, namespace, public IP or kube context in the exported
  fixture.
- A planted JWT, PEM block or non-empty password refuses the export, and the
  message names file and line, not the value.
- A leftover unknown absolute path refuses the export, and `--allow` lets it
  through.
- `environment.yml` keeps only the used nodes, including a node that is only
  in the describe logs and one that is only in a placement.
- Pseudonyms are consistent across environment, spec, describe logs and
  reasoning.
- File and directory names are cleaned too.
- Author and copyright headers survive unchanged.
- A namespace that is a substring of another word does not touch that word.
- A node name in an unusual form is caught by the leftover check.
- The computer or login name in a planted traceback refuses the export.
- A redaction target inside a binary file refuses the export.
- UIDs, container IDs, image digests and timestamps are unchanged.
- `redaction-map.yml` lies outside the bundle.
- The sources are byte-identical afterwards.
- The final scan is clean.
- `--from-study` and an explicit list give the same bundle for the same
  inputs.
- A plain Bexhoma result folder without an agent can be exported.

## Open

- Which redactions should be configurable per export? At least the
  namespace, if it is not personal elsewhere.
- Whether a run's bundle should also carry the handbook and contract
  versions it used. They already are in the result folders as archived
  contracts; the handbook is identified only by its hash.
