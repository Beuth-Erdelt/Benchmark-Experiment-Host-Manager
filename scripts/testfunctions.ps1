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

$BEXHOMA_NODE_SUT       = "cl-worker38"
$BEXHOMA_NODE_LOAD      = "cl-worker19"
$BEXHOMA_NODE_BENCHMARK = "cl-worker19"
$LOG_DIR                = ".\logs_tests"
$BEXHOMA_MS             = 10

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

function Wait-BexhomaLog {
    param([string]$LogFile)
    while (-not (Test-Path $LogFile)) {
        Start-Sleep -Seconds 2
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Waiting for log to close: $LogFile"
    while ($true) {
        try {
            $stream = [System.IO.File]::Open(
                $LogFile,
                [System.IO.FileMode]::Open,
                [System.IO.FileAccess]::ReadWrite,
                [System.IO.FileShare]::Read
            )
            $stream.Close()
            break
        } catch [System.IO.IOException] {
            Start-Sleep -Seconds 10
        }
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): Log closed: $LogFile"
}

function Invoke-CleanLogs {
    $warningText = "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens."

    Write-Host "Removing connection warning lines from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" -Recurse | ForEach-Object {
        $lines = Get-Content $_.FullName
        $filtered = $lines | Where-Object { $_ -ne $warningText }
        if ($filtered.Count -ne $lines.Count) {
            $filtered | Set-Content $_.FullName -Encoding utf8
        }
    }

    Write-Host "Extracting summaries from log files..."
    Get-ChildItem -Path $LOG_DIR -Filter "*.log" | ForEach-Object {
        $filename = $_.BaseName
        Write-Host "Cleaning $($_.FullName)"
        $show = $false
        $summary = @(foreach ($line in Get-Content $_.FullName) {
            if ($line -match '## Show Summary') { $show = $true }
            if ($show) { $line }
        })
        $summary | Out-File "$LOG_DIR\${filename}_summary.md" -Encoding utf8
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
