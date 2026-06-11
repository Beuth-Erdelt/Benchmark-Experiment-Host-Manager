# Scripts folder

## Running scripts

Each test script exists in two platform variants:
- **`.sh`** — run locally on an Ubuntu machine
- **`.ps1`** — run locally on a Windows machine

Both variants connect to the same Kubernetes cluster and invoke the same Python bexhoma scripts.

Python interpreter for PowerShell scripts is set via `$PYTHON` at the top of each `.ps1` file and must be adjusted per machine.

Run on Ubuntu:
```bash
bash scripts/test-docs-collector.sh
```

Run on Windows:
```powershell
.\scripts\test-docs-collector.ps1
```

Run unit tests for the collector evaluation logic:
```powershell
.\scripts\run_collector_tests.ps1      # PowerShell
bash scripts/run_collector_tests.sh   # Bash
```

## test-docs-collector.ps1 / test-docs-collector.sh

Runs a fixed sequence of bexhoma benchmark experiments (Benchbase, TPC-H, YCSB, HammerDB)
and their multi-tenant variants, then extracts `## Show Summary` sections from every log into
`_summary.md` files.

**Node variables** (top of both files — edit to retarget the cluster):
| Variable | Default | Role |
|---|---|---|
| `BEXHOMA_NODE_SUT` | `cl-worker38` | DBMS pod node |
| `BEXHOMA_NODE_LOAD` | `cl-worker19` | loader pod node |
| `BEXHOMA_NODE_BENCHMARK` | `cl-worker19` | benchmarker pod node |
| `BEXHOMA_MS` | `1` | max simultaneous DBMS configurations (`-ms`) |

**Log output directory:** `./logs_tests/`

**Log file naming pattern:** `doc_<benchmark>_testcase_collector[_tenants_<isolation>][_N].log`

**Comment style in `.sh`:** a heading comment block immediately before each `bexhoma` call
lists every parameter of that call, one `# -flag value   description` line per flag. The
description starts at column 32 (0-indexed); use 1 space minimum when the flag+value is longer.

**Comment style in `.ps1`:** inline `<# ... #>` block comments on the same line as each
parameter (the only syntax compatible with PowerShell backtick line continuation — `#` line
comments cannot follow a `` ` ``).

**Comment alignment (both variants):** descriptions aligned to column 32. The one exception is
`-ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS"` (49 chars) which lands at column 50.

**Shared helper functions** (bash: `testfunctions.sh`, PowerShell: `testfunctions.ps1`):
- `Wait-BexhomaProcess / wait_process` — polls `Win32_Process` / `ps aux` until no `python <name>.py` process remains. Called after every `bexhoma` invocation and at source-time to clear any pre-existing jobs.
- `Invoke-CleanLogs / clean_logs` — strips a specific kubectl token warning from all `.log` files, then extracts everything from `## Show Summary` onward into `<basename>_summary.md`.

## Conventions for new test scripts

### Shared setup (both `.sh` and `.ps1`)
- Source `testfunctions.sh` / dot-source `testfunctions.ps1` at the very top; this sets default node/path variables and waits for any pre-existing jobs.
- Override `BEXHOMA_MS` after sourcing when the script intentionally uses a value other than 1 (e.g., `BEXHOMA_MS=2` for DatabaseService which compares two DBMS simultaneously).
- Pass `-ms $BEXHOMA_MS` to every `bexhoma` call.
- Call `wait_process "<name>"` / `Wait-BexhomaProcess "<name>"` after every `bexhoma` invocation.

### Bash-specific
- One CLI parameter per continuation line (each ending with `\`).
- Precede every `bexhoma` call with a heading comment block: one `# -flag [value]   description` line per parameter, in the same order they appear in the call. Each flag is listed separately even when multiple flags share a continuation line in the call (e.g., `-ii -ic -is`).
- Redirect both stdout and stderr with `&>$LOG_DIR/<logfile>`.

### PowerShell-specific
- One CLI parameter per line, each followed by a `<# description #>` comment.
- All `<#` comments aligned to column 32 (pad with spaces; use `1` space minimum for overlong prefixes).
- Use backtick `` ` `` for line continuation; it must be the absolute last character on the line.
- Redirect both stdout and stderr with `2>&1 | Out-File <log> -Encoding utf8`.
