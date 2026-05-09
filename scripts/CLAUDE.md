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

**Log output directory:** `./logs_tests/`

**Log file naming pattern:** `doc_<benchmark>_testcase_collector[_tenants_<isolation>][_N].log`

**Comment style in `.ps1`:** inline `<# ... #>` block comments (the only syntax compatible
with PowerShell backtick line continuation — `#` line comments cannot follow a `` ` ``).

**Comment alignment:** all `<# ... #>` are aligned to column 32. The one exception is
`-ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS"` (49 chars) which lands at column 50.

**Shared helper functions** (bash: `testfunctions.sh`, PowerShell: inline):
- `Wait-BexhomaProcess / wait_process` — polls `Win32_Process` / `ps aux` until no `python <name>.py` process remains.
- `Invoke-CleanLogs / clean_logs` — strips a specific kubectl token warning from all `.log` files, then extracts everything from `## Show Summary` onward into `<basename>_summary.md`.

## Conventions for new PowerShell test scripts

- One CLI parameter per line, each followed by a `<# description #>` comment.
- All `<#` comments aligned to column 32 (pad with spaces; use `1` space minimum for overlong prefixes).
- Use backtick `` ` `` for line continuation; it must be the absolute last character on the line.
- Redirect both stdout and stderr with `2>&1 | Out-File <log> -Encoding utf8`.
- Call `Wait-BexhomaProcess "<name>"` after each run (polls until `python <name>.py` exits).
