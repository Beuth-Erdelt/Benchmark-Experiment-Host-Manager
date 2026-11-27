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

function Wait-YugabyteDB {
    # Waits after `helm install` of the YugabyteDB chart (release naming yb-master / yb-tserver)
    # until the master and tserver StatefulSets are rolled out and every tserver accepts
    # YSQL connections on port 5433. A fixed sleep is not enough: tservers may still be
    # pending or starting, and the first loader then fails with "connection refused".
    # Returns $false on timeout.
    param([int]$TimeoutSeconds = 900)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') Waiting for YugabyteDB StatefulSets..."
    # Out-Host: kubectl output must not become part of the return value
    kubectl rollout status statefulset/yb-master --timeout="$($TimeoutSeconds)s" | Out-Host
    if ($LASTEXITCODE -ne 0) { return $false }
    $left = [int][Math]::Max(1, ($deadline - (Get-Date)).TotalSeconds)
    kubectl rollout status statefulset/yb-tserver --timeout="$($left)s" | Out-Host
    if ($LASTEXITCODE -ne 0) { return $false }

    $replicas = [int](kubectl get statefulset yb-tserver -o jsonpath='{.spec.replicas}')
    $i = 0
    while ($i -lt $replicas) {
        kubectl exec yb-tserver-0 -c yb-tserver -- /home/yugabyte/bin/ysqlsh `
            -h "yb-tserver-$i.yb-tservers" -p 5433 -U yugabyte -d yugabyte -At -c "SELECT 1" 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') yb-tserver-$i accepts YSQL connections"
            $i++
        } elseif ((Get-Date) -ge $deadline) {
            Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ERROR: yb-tserver-$i does not accept YSQL connections after $($TimeoutSeconds)s"
            return $false
        } else {
            Start-Sleep -Seconds 10
        }
    }
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') YugabyteDB is ready ($replicas tservers)"
    return $true
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

function Test-LogOpenForWriting {
    # True if another process has the file open for writing, i.e. the log of a run that is
    # still going (readers such as tail -F do not count). An open for reading that does not
    # share write access fails while a writer holds the file. Rewriting such a log in place
    # mixes it up with other logs.
    param([string]$Path)
    try { [IO.File]::Open($Path, 'Open', 'Read', 'Read').Close(); return $false }
    catch [IO.IOException] { return $true }
}

$script:BEXHOMA_RUNS        = 0
$script:BEXHOMA_RUNS_FAILED = 0

function Write-ExperimentResult {
    # Prints "[DONE] <label>" after a bexhoma call that returned 0 and "[FAIL] <label> (exit N)"
    # otherwise. bexhoma returns 1 if a test of the summary failed or the run crashed; skipped
    # tests and warnings do not fail. Pass $LASTEXITCODE right after the call: it holds the exit
    # code of bexhoma also behind | Out-File. $? does not, in Windows PowerShell 2>&1 sets it to
    # $false. Counts the calls for Write-ExperimentTotal.
    param([int]$ExitCode, [string]$Label)
    $script:BEXHOMA_RUNS++
    if ($ExitCode -eq 0) {
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] $Label"
    } else {
        $script:BEXHOMA_RUNS_FAILED++
        Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [FAIL] $Label  (exit $ExitCode)"
    }
}

function Write-ExperimentTotal {
    # Prints how many of the bexhoma calls reported by Write-ExperimentResult failed.
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [SUMMARY] $script:BEXHOMA_RUNS_FAILED of $script:BEXHOMA_RUNS experiments failed"
}

function Invoke-CleanLogs {
    # Strips kubectl token warnings from the logs and extracts their "## Show Summary" part
    # into <name>_summary.md. Off by default: runs only with $env:BEXHOMA_CLEAN_LOGS = '1'
    # or -Force. Logs that are still being written are left alone.
    param([switch]$Force)
    if (-not $Force -and $env:BEXHOMA_CLEAN_LOGS -ne '1') {
        Write-Host "Skipping log cleaning (set `$env:BEXHOMA_CLEAN_LOGS = '1' or call Invoke-CleanLogs -Force)."
        return
    }

    $logs = @(Get-ChildItem -Path $LOG_DIR -Filter "*.log" -Recurse | Sort-Object FullName | Where-Object {
        if (Test-LogOpenForWriting $_.FullName) {
            Write-Host "Skipping $($_.FullName) (still being written)"
            $false
        } else { $true }
    })
    $logDirFull = (Get-Item $LOG_DIR).FullName.TrimEnd('\')

    Write-Host "Removing connection warning lines from log files..."
    $logs | ForEach-Object {
        # .NET reads UTF-8 without a BOM correctly, Get-Content takes it for ANSI
        $content = [IO.File]::ReadAllText($_.FullName) -replace "`r`n", "`n"
        $content = $content -replace '(?m)^Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens\.\n', ''
        $content = $content -replace '(?m)^Exception when calling CoreV1Api->.*\nReason: Unauthorized\nHTTP response headers: HTTPHeaderDict\(.*\nHTTP response body: .*\n(\n)*Create new access token\n', ''
        Write-LogFile -Path $_.FullName -Content $content
    }

    Write-Host "Extracting summaries from log files..."
    # summaries only for the logs directly in LOG_DIR, as before
    $logs | Where-Object { $_.DirectoryName.TrimEnd('\') -eq $logDirFull } | ForEach-Object {
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
