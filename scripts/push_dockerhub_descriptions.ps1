# Pushes README.md files to Docker Hub repository descriptions.
#
# Usage:
#   .\scripts\push_dockerhub_descriptions.ps1 -Username bexhoma -Password YOUR_PASSWORD
#
# The script authenticates once, then PATCHes the full_description of every
# bexhoma/* repository that has a corresponding README.md in the images/ tree.

param(
    [Parameter(Mandatory)][string]$Username,
    [Parameter(Mandatory)][string]$Password
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Map: Docker Hub repository slug -> relative path to README.md
$images = [ordered]@{
    'evaluator_dbmsbenchmarker'  = 'images\evaluator_dbmsbenchmarker\README.md'
    'benchmarker_dbmsbenchmarker'= 'images\benchmarker_dbmsbenchmarker\README.md'
    'monitoring'                 = 'images\monitoring\README.md'
    'benchmarker_hammerdb'       = 'images\hammerdb\benchmarker\README.md'
    'generator_hammerdb'         = 'images\hammerdb\generator\README.md'
    'benchmarker_ycsb'           = 'images\ycsb\benchmarker\README.md'
    'generator_ycsb'             = 'images\ycsb\generator\README.md'
    'generator_benchbase'        = 'images\benchbase\README.md'
    'benchmarker_benchbase'      = 'images\benchbase\README.md'
    'generator_tpch'             = 'images\tpch\generator\README.md'
    'loader_tpch_postgresql'     = 'images\tpch\loader_postgresql\README.md'
    'loader_tpch_mysql'          = 'images\tpch\loader_mysql\README.md'
    'loader_tpch_mariadb'        = 'images\tpch\loader_mariadb\README.md'
    'loader_tpch_monetdb'        = 'images\tpch\loader_monetdb\README.md'
    'generator_tpcds'            = 'images\tpcds\generator\README.md'
    'loader_tpcds_postgresql'    = 'images\tpcds\loader_postgresql\README.md'
    'loader_tpcds_mysql'         = 'images\tpcds\loader_mysql\README.md'
    'loader_tpcds_mariadb'       = 'images\tpcds\loader_mariadb\README.md'
    'loader_tpcds_monetdb'       = 'images\tpcds\loader_monetdb\README.md'
}

# Authenticate
Write-Host "Authenticating as $Username ..."
$loginBody = "{`"username`":`"$Username`",`"password`":`"$Password`"}"
$loginResponse = Invoke-RestMethod -Method Post `
    -Uri 'https://hub.docker.com/v2/users/login/' `
    -ContentType 'application/json' `
    -Body $loginBody
$token = $loginResponse.token
if ($token) {
    Write-Host "Authentication successful (token: $($token.Substring(0,8))...)"
} else {
    Write-Host "Authentication failed - no token returned."
    exit 1
}

Add-Type -AssemblyName System.Web.Extensions
$serializer = New-Object System.Web.Script.Serialization.JavaScriptSerializer
$serializer.MaxJsonLength = [int]::MaxValue

$projectRoot = Split-Path $PSScriptRoot -Parent

Write-Host "PSScriptRoot : $PSScriptRoot"
Write-Host "Project root : $projectRoot"
Write-Host "Image count  : $($images.Count)"

$ok = 0
$failed = @()

foreach ($entry in $images.GetEnumerator()) {
    $repo = $entry.Key
    $readmePath = Join-Path $projectRoot $entry.Value
    Write-Host "  -> $repo  ($readmePath)"
    if (-not (Test-Path $readmePath)) {
        Write-Host "  SKIP $repo - README not found at $readmePath"
        continue
    }
    $readme = Get-Content $readmePath -Raw -Encoding UTF8
    $body = $serializer.Serialize(@{ full_description = [string]$readme })
    $uri = "https://hub.docker.com/v2/repositories/bexhoma/$repo/"
    try {
        Invoke-RestMethod -Method Patch `
            -Uri $uri `
            -Headers @{ Authorization = "Bearer $token" } `
            -ContentType 'application/json' `
            -Body $body | Out-Null
        Write-Host "  OK  $repo"
        $ok++
    } catch {
        Write-Host "  FAIL $repo - $($_.Exception.Message)"
        $failed += $repo
    }
}

Write-Host ""
Write-Host "$ok updated, $($failed.Count) failed."
if ($failed.Count -gt 0) {
    Write-Host "Failed repositories:"
    $failed | ForEach-Object { Write-Host "  $_" }
    exit 1
}
