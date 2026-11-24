# Plan: identify the harness of an agent run without git

Status: **planned** (2026-11-24), not implemented.

## Problem

Every phase event of a trajectory records `harness=_harness_revision()`
(`agent/harness/agent.py:843`, `:927`, `:1951`):

```python
{"commit": _checked_out_commit(repo_root), "sources_sha256": <sha256 over agent/harness/*.py>}
```

1. **The commit is read from `.git` files.** `_checked_out_commit()` reads
   `.git/HEAD` and then `.git/refs/heads/<branch>`. It returns `None`
   * in a git worktree (`.git` is a file `gitdir: ...`),
   * when the branch ref is only in `.git/packed-refs` (after `git gc`, fresh clone),
   * in a pip install or a container image (no `.git` at all).

   `tests/test_agent_harness.py::HarnessRevisionTest::test_a_trajectory_identifies_the_harness_that_drove_it`
   asserts a 40-character commit, so it fails in every worktree.
2. **The source hash covers too little.** Only `agent/harness/*.py`. The bexhoma
   code the harness calls to validate and submit (`bexhoma/spec.py`,
   `spec_argv.py`, `environment.py`) is not covered, so a change there is
   invisible in the trajectory.
3. **No version.** Neither the bexhoma version nor the DBMS-Benchmarker
   version is in the record.
4. **Line endings.** The hash is over raw bytes, so a CRLF checkout and an
   LF image of the same code give different hashes.

## Scope: code only

The harness identity covers **code**, nothing else. The inputs of a run are
recorded separately already and stay so:

| Input | Recorded as | Why separate |
|---|---|---|
| catalog contract | `catalog_sha256`, contract version | its own version line |
| `environment.yml` | `environment_sha256`, `environment_present` | describes the cluster, not the harness |
| handbook | `method_sha256`, `method_present` | an experimental variable (`--method` ablation); folding it in would mark runs with the same harness and a different handbook as "different harness" |

Comparing two runs then answers four separate questions: same harness code,
same catalog, same environment, same handbook.

## Design

### 1. Version from package metadata (always available)

* `bexhoma_version`: `bexhoma.__version__`
* `dbmsbenchmarker_version`: `importlib.metadata.version("dbmsbenchmarker")`, `None` if not installed

Works in a checkout, a pip install and an image.

### 2. Fingerprint over a declared manifest

One list of path patterns in one place, e.g. `agent/harness/fingerprint.py`:

```python
HARNESS_SOURCES = (
    "agent/harness/*.py",
    "bexhoma/spec.py",
    "bexhoma/spec_argv.py",
    "bexhoma/environment.py",
)
```

* Read through the package directories (`Path(agent.__file__)`,
  `Path(bexhoma.__file__)`), so it works in an installed copy.
* Normalise line endings (`\r\n` -> `\n`) before hashing.
* Hash per file over the normalised bytes, keyed by the repository-relative
  path; the overall `fingerprint` is the sha256 over the sorted
  `path:hash` lines.
* `fingerprint` is the comparison key: two runs have the same harness if and
  only if it is equal.

Not in the manifest: `agent/lifecycle.py` and `agent/lifecycle_controller.py`.
They are operator-side wrappers (model server start/stop, waiting for the
report) and call the agent's CLI; nothing under `agent.harness` imports them.
Follow-up and attempt decisions are in `agent/harness/agent.py` and
`prompts.py`, which the manifest covers.

### 3. Build stamp at release

At release, a generated `bexhoma/_build_info.py` holds

```python
VERSION = "X.Y.Z"
COMMIT = "<40 hex>"
FINGERPRINT = "sha256:..."
FILES = {"agent/harness/agent.py": "sha256:...", ...}
```

* Written by the publish workflow (`.github/workflows/publish-to-test-pypi.yml`)
  before building the package, not by `bump_version.py`: the commit of the
  release is known only there.
* Never edited by hand, not committed; `.gitignore` entry. Without it (dev
  checkout) the record has no `release_fingerprint`.
* At runtime: equal fingerprint -> the run used the release as published;
  different -> `modified` lists the files whose hash differs from `FILES`.

### 4. Git only as a label

If a checkout is present, add `commit` from `git rev-parse HEAD` (handles
worktrees and packed refs), with a short timeout and every error caught.
Missing git means `commit: null`. The commit never decides comparability.
`_checked_out_commit()` is removed.

### Resulting record

```yaml
harness:
  bexhoma_version: X.Y.Z
  dbmsbenchmarker_version: A.B.C
  fingerprint: sha256:...          # comparison key
  files: {agent/harness/agent.py: sha256:..., ...}
  release_fingerprint: sha256:...  # from _build_info, absent in a dev checkout
  modified: [agent/harness/prompts.py]  # only with a build stamp
  commit: 2af6a708...              # optional, null without git
```

`files` makes a differing fingerprint traceable without the source tree.

## Steps

1. `agent/harness/fingerprint.py`: manifest, `harness_identity()` returning the
   record above; `_harness_revision()` in `agent.py` delegates to it (call
   sites unchanged).
2. Publish workflow: write `bexhoma/_build_info.py` before the build; check
   that the built wheel contains it.
3. `.gitignore`: `bexhoma/_build_info.py`.
4. Docs: `docs/AgentHarness.md`, the trajectory fields (one table row each).
5. `agent/ARCHITECTURE.md`: the identity paragraph.

## Tests (`tests/test_agent_harness.py`)

* Same fingerprint in the checkout and in a copy of the manifest files without
  `.git` (temporary directory).
* Same fingerprint for CRLF and LF copies of the same files.
* Editing any manifest file changes `fingerprint` and exactly that entry of
  `files` (replaces `test_editing_the_harness_changes_the_recorded_fingerprint`).
* Changing the handbook, catalog or environment does **not** change the
  fingerprint.
* With a fake `_build_info`: `modified` empty when equal, lists the edited file
  otherwise; no `release_fingerprint` without it.
* `commit` is `None` when `git` is not on `PATH` (monkeypatched), and the
  record is otherwise complete.
* `test_a_trajectory_identifies_the_harness_that_drove_it` asserts version and
  fingerprint instead of a 40-character commit, so it passes in a worktree.

## Not in scope

* Fingerprinting the whole bexhoma package: the version covers releases,
  and the manifest covers what the model faces.
* Docker images of the benchmark runs: bexhoma records their tags per
  experiment, not their digests (`docs/AgentResultContract.md`); a separate topic.
