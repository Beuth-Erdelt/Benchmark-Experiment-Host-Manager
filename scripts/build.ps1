# Library of functions for building and pushing bexhoma Docker images.
#
# Mirrors the workflow of build.sh for PowerShell.
# All builds run as parallel background jobs; failures are logged and reported at the end.
# Intended to be called directly from the project root, or via scripts/build.ps1.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

$script:RootDir = if ($PSScriptRoot) { Split-Path $PSScriptRoot } else { $PWD.Path }
$script:Jobs    = [System.Collections.Generic.List[hashtable]]::new()
$script:AnyFailed = $false

# At most this many docker builds and this many docker pushes run at the
# same time. The two limits are independent.
# The jobs are separate processes, so they share named system semaphores.
$script:MaxParallelBuilds = 10
$script:MaxParallelPushes = 10
$script:BuildSemaphore    = "bexhoma_build_build_$PID"
$script:PushSemaphore     = "bexhoma_build_push_$PID"

# Runs inside each job: a command, holding one semaphore slot while it runs.
# Usage: & SlotCode <semName> <max> <exe> <args...>
$script:SlotCode = {
    param($semName, $max, $exe, [string[]]$cmdArgs)
    $sem = New-Object System.Threading.Semaphore($max, $max, $semName)
    $null = $sem.WaitOne()
    try {
        & $exe @cmdArgs
        if ($LASTEXITCODE -ne 0) { throw "$exe $($cmdArgs[0]) failed (exit $LASTEXITCODE)" }
    } finally {
        $null = $sem.Release()
        $sem.Dispose()
    }
}.ToString()

# Semaphore names and limits, handed to each job.
function _SlotArgs {
    @{
        Code      = $script:SlotCode
        BuildSem  = $script:BuildSemaphore
        MaxBuilds = $script:MaxParallelBuilds
        PushSem   = $script:PushSemaphore
        MaxPushes = $script:MaxParallelPushes
    }
}


#### Job tracking helpers ####

function _BgDockerJob {
    # Launch a background job that runs: docker build + docker push.
    # Usage: _BgDockerJob <label> <workdir> <image> <version> [dockerfile]
    param(
        [string]$Label,
        [string]$WorkDir,
        [string]$Image,
        [string]$Version,
        [string]$Dockerfile = 'Dockerfile'
    )
    $rootDir = $script:RootDir
    $job = Start-Job -ScriptBlock {
        param($rootDir, $workDir, $image, $version, $dockerfile, $slot)
        Set-Location (Join-Path $rootDir $workDir)
        $run = [scriptblock]::Create($slot.Code)
        & $run $slot.BuildSem $slot.MaxBuilds docker @('build', '-f', $dockerfile, '-t', "bexhoma/${image}:${version}", '.')
        & $run $slot.PushSem  $slot.MaxPushes docker @('push', "bexhoma/${image}:${version}")
    } -ArgumentList $rootDir, $WorkDir, $Image, $Version, $Dockerfile, (_SlotArgs)
    $script:Jobs.Add(@{ Job = $job; Label = $Label })
}

function _BgPyJob {
    # Launch a background job that runs: python create_Dockerfiles.py + docker push.
    # Used for the dbmsbenchmarker images which generate their Dockerfile via a script.
    # Usage: _BgPyJob <label> <workdir> <image> <version> <dbmsbenchmarker>
    param(
        [string]$Label,
        [string]$WorkDir,
        [string]$Image,
        [string]$Version,
        [string]$DbmsBenchmarker
    )
    $rootDir = $script:RootDir
    $job = Start-Job -ScriptBlock {
        param($rootDir, $workDir, $image, $version, $dbmsbenchmarker, $slot)
        Set-Location (Join-Path $rootDir $workDir)
        $run = [scriptblock]::Create($slot.Code)
        # create_Dockerfiles.py runs docker build itself, so it takes a build slot.
        & $run $slot.BuildSem $slot.MaxBuilds python @('create_Dockerfiles.py', '--version', $dbmsbenchmarker, '--image-tag', $version)
        & $run $slot.PushSem  $slot.MaxPushes docker @('push', "bexhoma/${image}:${version}")
    } -ArgumentList $rootDir, $WorkDir, $Image, $Version, $DbmsBenchmarker, (_SlotArgs)
    $script:Jobs.Add(@{ Job = $job; Label = $Label })
}

function _WaitAll {
    # Wait for all registered background jobs.
    # Prints each failed job's output, then a summary of all failures.
    # Sets $script:AnyFailed = $true if any job failed.
    $errors = [System.Collections.Generic.List[string]]::new()
    foreach ($entry in $script:Jobs) {
        $job   = $entry.Job
        $label = $entry.Label
        $null  = Wait-Job -Job $job
        $output = Receive-Job -Job $job 2>&1
        if ($job.State -eq 'Failed') {
            $errors.Add($label)
            Write-Host ""
            Write-Host "=== ERROR: $label ===" -ForegroundColor Red
            $output | ForEach-Object { Write-Host "  $_" }
            $reason = $job.ChildJobs[0].JobStateInfo.Reason.Message
            if ($reason) { Write-Host "  $reason" -ForegroundColor Yellow }
        }
        Remove-Job -Job $job
    }
    $script:Jobs.Clear()
    if ($errors.Count -gt 0) {
        Write-Host ""
        Write-Host "=== FAILED BUILDS ===" -ForegroundColor Red
        foreach ($e in $errors) {
            Write-Host "  FAILED: $e" -ForegroundColor Red
        }
        $script:AnyFailed = $true
    }
}


#### Build functions ####

function Build-AndPush-Dbmsbenchmarker {
    param([string]$DbmsBenchmarker, [string]$Version)
    if (-not $DbmsBenchmarker -or -not $Version) {
        Write-Host "Usage: Build-AndPush-Dbmsbenchmarker <dbmsbenchmarker_version> <image_tag>"
        return
    }
    _BgPyJob "bexhoma/evaluator_dbmsbenchmarker:$Version"  "images/evaluator_dbmsbenchmarker"  "evaluator_dbmsbenchmarker"  $Version $DbmsBenchmarker
    _BgPyJob "bexhoma/benchmarker_dbmsbenchmarker:$Version" "images/benchmarker_dbmsbenchmarker" "benchmarker_dbmsbenchmarker" $Version $DbmsBenchmarker
}

function Build-AndPush-Tpcds {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Tpcds <image_tag>"; return }
    _BgDockerJob "bexhoma/generator_tpcds:$Version"          "images/tpcds/generator"        "generator_tpcds"          $Version
    _BgDockerJob "bexhoma/loader_tpcds_postgresql:$Version"  "images/tpcds/loader_postgresql" "loader_tpcds_postgresql"  $Version
    _BgDockerJob "bexhoma/loader_tpcds_db2:$Version"         "images/tpcds/loader_db2"        "loader_tpcds_db2"         $Version
    _BgDockerJob "bexhoma/loader_tpcds_mysql:$Version"       "images/tpcds/loader_mysql"      "loader_tpcds_mysql"       $Version
    _BgDockerJob "bexhoma/loader_tpcds_mariadb:$Version"     "images/tpcds/loader_mariadb"    "loader_tpcds_mariadb"     $Version
    _BgDockerJob "bexhoma/loader_tpcds_monetdb:$Version"     "images/tpcds/loader_monetdb"    "loader_tpcds_monetdb"     $Version
    _BgDockerJob "bexhoma/loader_tpcds_clickhouse:$Version"  "images/tpcds/loader_clickhouse" "loader_tpcds_clickhouse"  $Version
}

function Build-AndPush-Ssb {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Ssb <image_tag>"; return }
    _BgDockerJob "bexhoma/generator_ssb:$Version"            "images/ssb/generator"           "generator_ssb"            $Version
    _BgDockerJob "bexhoma/loader_ssb_postgresql:$Version"    "images/ssb/loader_postgresql"   "loader_ssb_postgresql"    $Version
    _BgDockerJob "bexhoma/loader_ssb_monetdb:$Version"       "images/ssb/loader_monetdb"      "loader_ssb_monetdb"       $Version
    _BgDockerJob "bexhoma/loader_ssb_clickhouse:$Version"    "images/ssb/loader_clickhouse"   "loader_ssb_clickhouse"    $Version
    _BgDockerJob "bexhoma/loader_ssb_mysql:$Version"         "images/ssb/loader_mysql"        "loader_ssb_mysql"         $Version
    _BgDockerJob "bexhoma/loader_ssb_mariadb:$Version"       "images/ssb/loader_mariadb"      "loader_ssb_mariadb"       $Version
}

function Build-AndPush-Tpch {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Tpch <image_tag>"; return }
    _BgDockerJob "bexhoma/generator_tpch:$Version"          "images/tpch/generator"        "generator_tpch"          $Version
    _BgDockerJob "bexhoma/loader_tpch_postgresql:$Version"  "images/tpch/loader_postgresql" "loader_tpch_postgresql"  $Version
    _BgDockerJob "bexhoma/loader_tpch_mysql:$Version"       "images/tpch/loader_mysql"      "loader_tpch_mysql"       $Version
    _BgDockerJob "bexhoma/loader_tpch_mariadb:$Version"     "images/tpch/loader_mariadb"    "loader_tpch_mariadb"     $Version
    _BgDockerJob "bexhoma/loader_tpch_monetdb:$Version"     "images/tpch/loader_monetdb"    "loader_tpch_monetdb"     $Version
    _BgDockerJob "bexhoma/loader_tpch_clickhouse:$Version"  "images/tpch/loader_clickhouse" "loader_tpch_clickhouse"  $Version
    _BgDockerJob "bexhoma/loader_tpch_sqlserver:$Version"   "images/tpch/loader_sqlserver"  "loader_tpch_sqlserver"   $Version
    _BgDockerJob "bexhoma/loader_tpch_oracle:$Version"      "images/tpch/loader_oracle"     "loader_tpch_oracle"      $Version
    _BgDockerJob "bexhoma/loader_tpch_db2:$Version"         "images/tpch/loader_db2"        "loader_tpch_db2"         $Version
}

function Build-AndPush-TpchRefresh {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-TpchRefresh <image_tag>"; return }
    # Generator needs dbgen/dists.dss/tpc_eula.txt copied from images/tpch/generator first.
    _BgDockerJob "bexhoma/generator_tpch_refresh:$Version"        "images/tpch_refresh/generator"        "generator_tpch_refresh"         $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_postgresql:$Version" "images/tpch_refresh/loader_postgresql" "loader_tpch_refresh_postgresql" $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_mysql:$Version"      "images/tpch_refresh/loader_mysql"      "loader_tpch_refresh_mysql"      $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_mariadb:$Version"    "images/tpch_refresh/loader_mariadb"    "loader_tpch_refresh_mariadb"    $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_monetdb:$Version"    "images/tpch_refresh/loader_monetdb"    "loader_tpch_refresh_monetdb"    $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_clickhouse:$Version" "images/tpch_refresh/loader_clickhouse" "loader_tpch_refresh_clickhouse" $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_sqlserver:$Version"  "images/tpch_refresh/loader_sqlserver"  "loader_tpch_refresh_sqlserver"  $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_oracle:$Version"     "images/tpch_refresh/loader_oracle"     "loader_tpch_refresh_oracle"     $Version
    _BgDockerJob "bexhoma/loader_tpch_refresh_db2:$Version"        "images/tpch_refresh/loader_db2"        "loader_tpch_refresh_db2"        $Version
}

function Build-AndPush-Monitoring {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Monitoring <image_tag>"; return }
    _BgDockerJob "bexhoma/monitoring:$Version" "images/monitoring" "monitoring" $Version
}

function Build-AndPush-Hammerdb {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Hammerdb <image_tag>"; return }
    _BgDockerJob "bexhoma/benchmarker_hammerdb:$Version" "images/hammerdb/benchmarker" "benchmarker_hammerdb" $Version
    _BgDockerJob "bexhoma/generator_hammerdb:$Version"   "images/hammerdb/generator"   "generator_hammerdb"   $Version
}

function Build-AndPush-Ycsb {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Ycsb <image_tag>"; return }
    _BgDockerJob "bexhoma/benchmarker_ycsb:$Version" "images/ycsb/benchmarker" "benchmarker_ycsb" $Version
    _BgDockerJob "bexhoma/generator_ycsb:$Version"   "images/ycsb/generator"   "generator_ycsb"   $Version
}

function Build-AndPush-Benchbase {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Benchbase <image_tag>"; return }
    _BgDockerJob "bexhoma/generator_benchbase:$Version"   "images/benchbase" "generator_benchbase"   $Version "Dockerfile_generator"
    _BgDockerJob "bexhoma/benchmarker_benchbase:$Version" "images/benchbase" "benchmarker_benchbase" $Version "Dockerfile_benchmarker"
}

function Build-AndPush-Hardware {
    param([string]$Version)
    if (-not $Version) { Write-Host "Usage: Build-AndPush-Hardware <image_tag>"; return }
    _BgDockerJob "bexhoma/benchmarker_hardware:$Version" "images/hardware/benchmarker" "benchmarker_hardware" $Version
    _BgDockerJob "bexhoma/sut_hardware:$Version"         "images/hardware/sut"         "sut_hardware"         $Version
}


#### Main ####

# The DBMS-Benchmarker images use the installed version (set by requirements.txt);
# its git tags have the form vX.Y.Z.
$dbmsbenchmarkerVersion = (pip show dbmsbenchmarker | Select-String "^Version:" | ForEach-Object { ($_ -split '\s+')[1] })
if (-not $dbmsbenchmarkerVersion) { throw "dbmsbenchmarker is not installed" }
$dbmsbenchmarker = "v$dbmsbenchmarkerVersion"
Write-Output "DBMS-Benchmarker $dbmsbenchmarker"
$version = (pip show bexhoma | Select-String "^Version:" | ForEach-Object { ($_ -split '\s+')[1] })
Write-Output $version

Build-AndPush-Dbmsbenchmarker $dbmsbenchmarker $version
Build-AndPush-Tpch          $version
Build-AndPush-TpchRefresh   $version
Build-AndPush-Tpcds         $version
Build-AndPush-Ssb           $version
Build-AndPush-Monitoring    $version
Build-AndPush-Hammerdb      $version
Build-AndPush-Ycsb          $version
Build-AndPush-Benchbase     $version
Build-AndPush-Hardware      $version

_WaitAll
Write-Output "All version builds and pushes completed."

$version = "latest"
Write-Output $version

Build-AndPush-Dbmsbenchmarker $dbmsbenchmarker $version
Build-AndPush-Tpch          $version
Build-AndPush-TpchRefresh   $version
Build-AndPush-Tpcds         $version
Build-AndPush-Ssb           $version
Build-AndPush-Monitoring    $version
Build-AndPush-Hammerdb      $version
Build-AndPush-Ycsb          $version
Build-AndPush-Benchbase     $version
Build-AndPush-Hardware      $version

_WaitAll
Write-Output "All latest builds and pushes completed."

if ($script:AnyFailed) { exit 1 }
