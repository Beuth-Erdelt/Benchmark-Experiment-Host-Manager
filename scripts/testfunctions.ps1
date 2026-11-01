#Requires -Version 5.1
# Shared helper functions, default variables, and startup checks dot-sourced by
# all bexhoma test scripts.
#
# Declares default node/path variables, defines helper functions, then runs
# prerequisite checks and waits for any pre-existing bexhoma jobs, so every
# script that dot-sources this file starts in a known-good state.
#
# Default variable values can be overridden after dot-sourcing:
#   . .\scripts\testfunctions.ps1
#   $BEXHOMA_NODE_SUT = "other-node"   # override example
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

# ---------------------------------------------------------------------------
# Default variable values (override after dot-sourcing if needed)
# ---------------------------------------------------------------------------

$BEXHOMA_NODE_SUT         = "cl-worker36"
$BEXHOMA_NODE_LOAD        = "cl-worker38"
$BEXHOMA_NODE_BENCHMARK   = "cl-worker38"
# worker pods of distributed DBMS (CockroachDB, Citus, TiDB, YugabyteDB), joined by '+'
# as bexhoma -rnw expects; without -rst their data sits on the nodes' local disks, so
# the nodes decide the results. _4 for 4 workers (one per node).
$BEXHOMA_NODES_WORKER     = "cl-worker36+cl-worker37+cl-worker29"
$BEXHOMA_NODES_WORKER_4   = "cl-worker36+cl-worker37+cl-worker29+cl-worker39"
$LOG_DIR                  = ".\logs_tests"
$BEXHOMA_MS               = 10
$BEXHOMA_STORAGE_CLASS    = "nvme"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

function Wait-BexhomaProcess {
    param([string]$ProcessName)
    while ($true) {
        $running = Get-CimInstance Win32_Process |
                   Where-Object { $_.CommandLine -like "*bexhoma*$ProcessName*" }
        if (-not $running) { break }
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Waiting for bexhoma $ProcessName to terminate..."
        Start-Sleep -Seconds 60
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): bexhoma $ProcessName has terminated."
}

function Write-LogFile {
    # UTF-8 without BOM and with LF, as in the repository. In Windows PowerShell,
    # Set-Content and Out-File -Encoding utf8 write a BOM, Out-File also CRLF.
    # A file with these bytes already is not written, so git sees no change.
    param([string]$Path, [string]$Content)
    $bytes = (New-Object System.Text.UTF8Encoding($false)).GetBytes(($Content -replace "`r`n", "`n"))
    if ((Test-Path $Path) -and
        [Convert]::ToBase64String([IO.File]::ReadAllBytes($Path)) -ceq [Convert]::ToBase64String($bytes)) {
        return
    }
    [IO.File]::WriteAllBytes($Path, $bytes)
}

function Invoke-CleanLogs {
    Write-Host "Removing connection warning lines from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" -Recurse | ForEach-Object {
        # .NET reads UTF-8 without a BOM correctly, Get-Content takes it for ANSI
        $content = [IO.File]::ReadAllText($_.FullName) -replace "`r`n", "`n"
        $content = $content -replace '(?m)^Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens\.\n', ''
        $content = $content -replace '(?m)^Exception when calling CoreV1Api->.*\nReason: Unauthorized\nHTTP response headers: HTTPHeaderDict\(.*\nHTTP response body: .*\n(\n)*Create new access token\n', ''
        Write-LogFile -Path $_.FullName -Content $content
    }

    Write-Host "Extracting summaries from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" | ForEach-Object {
        Write-Host "Cleaning $($_.FullName)"
        $content = [IO.File]::ReadAllText($_.FullName)
        $start = [regex]::Match($content, '(?m)^.*## Show Summary')
        $summary = ''
        if ($start.Success) {
            $summary = $content.Substring($start.Index)
            if (-not $summary.EndsWith("`n")) { $summary += "`n" }
        }
        Write-LogFile -Path (Join-Path $_.DirectoryName "$($_.BaseName)_summary.md") -Content $summary
    }

    Write-Host "Extraction complete! Files are saved in $LOG_DIR."
}

# ---------------------------------------------------------------------------
# Startup checks (run at dot-source time)
# ---------------------------------------------------------------------------

if (-not (Test-Path "cluster.config")) {
    Write-Error "Error: cluster.config not found."
    exit 1
}
Write-Host "Passed: ./cluster.config found."

foreach ($dir in @("experiments", "k8s")) {
    if (-not (Test-Path $dir -PathType Container)) {
        Write-Error "Error: Directory '$dir' missing."
        exit 1
    }
}
Write-Host "Passed: ./experiments/ found."
Write-Host "Passed: ./k8s/ found."

New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null
Write-Host "Passed: $LOG_DIR/ found."

Write-Host "Checks passed. Proceeding..."

# ---------------------------------------------------------------------------
# Wait for any pre-existing jobs
# ---------------------------------------------------------------------------

#Wait-BexhomaProcess "tpch"
#Wait-BexhomaProcess "tpcds"
#Wait-BexhomaProcess "hammerdb"
#Wait-BexhomaProcess "benchbase"
#Wait-BexhomaProcess "ycsb"
