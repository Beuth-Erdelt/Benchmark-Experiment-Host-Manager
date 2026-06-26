# scripts/

Helper and maintenance scripts for the bexhoma project.
Scripts connect to a Kubernetes cluster and invoke the Python bexhoma CLI (`bexhoma <subcommand>`).

---

## Directory structure

```
scripts/
├── test-docs-*.sh / *.ps1   # paired experiment-runner scripts (one per topic)
├── testfunctions.sh / .ps1  # shared helper functions (sourced at script start)
├── build.sh / build.ps1     # Docker image build and push helpers
├── run_collector_validations.sh / .ps1
│                            # run all validate_collector_*.py scripts
├── validate_collector_*.py  # unit-level validators for collector output
├── compare-commands.py      # cross-check flags between .sh, .ps1, and docs
├── scan-docs.py             # report experiment metadata for every doc log reference
├── replace-docs.py          # patch docs with fresh summary content from logs_tests/
├── convert-to-lf.ps1        # normalize line endings to LF + UTF-8 no-BOM (Windows)
├── _reorder_flags.py        # reorder bexhoma flags to canonical order in test scripts
├── _sync_docs.py            # sync example commands in docs/ from test-docs-*.sh
├── _sync_ps.py              # sync test-docs-*.ps1 to match their .sh counterparts
└── _sync_cases_sh.py        # regenerate test-docs-cases.sh from test-docs-cases.ps1
```

---

## Bash and PowerShell variants

Every test script exists in two platform variants that run the same experiments:

| Variant | Platform | Invocation |
|---|---|---|
| `.sh` | Ubuntu / Linux | `bash scripts/test-docs-collector.sh` |
| `.ps1` | Windows | `.\scripts\test-docs-collector.ps1` |

Both variants connect to the same Kubernetes cluster.
The PowerShell scripts set `$PYTHON` at the top of the file — adjust this path to match your local Python environment.

Shared helper functions live in `testfunctions.sh` and `testfunctions.ps1` and are sourced at the start of every test script.
They provide:

- `wait_process` / `Wait-BexhomaProcess` — polls until no `python <name>.py` process remains; called after every `bexhoma` invocation.
- `clean_logs` / `Invoke-CleanLogs` — strips kubectl token warnings and extracts `## Show Summary` sections from each `.log` file into `<basename>_summary.md` files.

---

## test-docs-* scripts — producing documentation examples

The `test-docs-*` scripts are the primary source of example output shown in the documentation pages.

Each script runs a fixed sequence of bexhoma benchmark experiments for one topic (a DBMS, a benchmark type, or a feature set) and writes log files to `logs_tests/`.
After the experiments finish, `clean_logs`/`Invoke-CleanLogs` extracts the `## Show Summary` section of each log into a matching `_summary.md` file in the same directory.

The summary files are the content embedded inside ` ```markdown ``` ` blocks in the `docs/` pages.

**Node variables** (set at the top of each script, or inherited from `testfunctions.sh/.ps1`):

| Variable | Role |
|---|---|
| `BEXHOMA_NODE_SUT` | Kubernetes node for the DBMS pod |
| `BEXHOMA_NODE_LOAD` | Kubernetes node for loader pods |
| `BEXHOMA_NODE_BENCHMARK` | Kubernetes node for benchmarker pods |
| `BEXHOMA_MS` | Max simultaneous DBMS configurations (`-ms`) |

**Log file naming:** `logs_tests/doc_<benchmark>_<topic>[_N].log`

**Flag ordering** inside every `bexhoma` call follows the canonical group order defined in `CLAUDE.md` (target → identity → timing → sweep → parallelism → topology → resources → node pinning).

---

## Python utility scripts

### `scan-docs.py`

Scans `docs/*.md` for log-file references and reports experiment metadata for each one.

```
python scripts/scan-docs.py
```

Output columns: doc file, log file, experiment code, duration, bexhoma version, passed/failed test counts, and whether the `.log` / `_summary.md` files exist locally.
Also reports missing log files and log files in `logs_tests/` that no doc references.

### `replace-docs.py`

Patches `docs/*.md` in-place by replacing the content of every ` ```markdown ``` ` block (identified by the preceding log-file name) with the matching `_summary.md` from `logs_tests/`.

```
python scripts/replace-docs.py
```

Run this after executing test-docs scripts to refresh the embedded example output in the docs.

### `compare-commands.py`

Cross-checks `bexhoma` flag sets across all three sources — `.sh` scripts, `.ps1` scripts, and `docs/*.md` bash blocks — and reports any disagreements per log file.

```
python scripts/compare-commands.py
```

Useful for catching drift when a command is updated in one place but not the others.

### `convert-to-lf.ps1`

Rewrites `.md`, `.txt`, `.sh`, and `.py` files under `docs/`, `logs_tests/`, `images/`, and `scripts/` as UTF-8 without BOM with LF line endings.
`.ps1` files are intentionally left untouched (CRLF is fine for PowerShell).

```powershell
.\scripts\convert-to-lf.ps1
```

The Python sync scripts (`_reorder_flags.py`, `_sync_docs.py`, `_sync_ps.py`, `_sync_cases_sh.py`, `replace-docs.py`) all write with explicit LF and do not need this script as a follow-up.
`convert-to-lf.ps1` is useful for one-off corrections or after editing files directly in a Windows text editor.

### `validate_collector_*.py`

Unit-level validators for the collector evaluation notebooks.
Each script loads an experiment result from `logs_tests/` and the matching result folder, runs the corresponding `collectors.*` class, and checks that all expected DataFrames are non-empty and contain the required columns.

Run individually or via `run_collector_validations.sh` / `run_collector_validations.ps1`.

---

## Sync/convert scripts

These scripts (`_` prefix) keep the three representations of each `bexhoma` command — bash test scripts, PowerShell test scripts, and doc examples — consistent with each other.
Run them from the repository root whenever commands are added or changed.

### `_reorder_flags.py`

Reorders the flags in every `bexhoma` call in `test-docs-*.sh` and `test-docs-*.ps1` to match the canonical group order defined in `CLAUDE.md`.
Also reconstructs the preceding comment block in `.sh` files and the inline `<# … #>` comments in `.ps1` files to match the new order.

```
python scripts/_reorder_flags.py
```

Run this first whenever flags are added, removed, or reordered.

### `_sync_docs.py`

Propagates the canonical `bexhoma` commands from `test-docs-*.sh` into the matching bash blocks inside `docs/*.md`.
Only the command lines are written to docs; the heading comment block from the `.sh` file is omitted.

```
python scripts/_sync_docs.py
```

### `_sync_ps.py`

Regenerates the `bexhoma` command blocks in `test-docs-*.ps1` from the corresponding `.sh` commands, converting bash syntax to PowerShell syntax (backtick continuation, inline `<# … #>` comments, double-quoting of comma-separated values).
Descriptions are taken from the `.sh` header comment block.

```
python scripts/_sync_ps.py
```

### `_sync_cases_sh.py`

`test-docs-cases` is the exception to the rule: its PowerShell file is the canonical source.
This script regenerates `test-docs-cases.sh` from `test-docs-cases.ps1`, converting PS syntax back to bash and translating `Write-Host`, `Start-Sleep`, and `Invoke-CleanLogs` calls to their bash equivalents.

```
python scripts/_sync_cases_sh.py
```

---

## Typical workflow after changing a test command

1. Edit the `.sh` file (or `.ps1` for the cases script).
2. `python scripts/_reorder_flags.py` — enforce canonical flag order.
3. `python scripts/_sync_ps.py` — mirror changes to `.ps1` files.
4. `python scripts/_sync_docs.py` — mirror changes to `docs/` examples.
5. Run the relevant `test-docs-*.sh` script to produce fresh logs.
6. `python scripts/replace-docs.py` — embed the new summary output in docs.
7. `python scripts/compare-commands.py` — verify no drift remains.
