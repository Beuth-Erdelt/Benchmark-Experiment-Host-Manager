<#
Dev-only operator helper, NOT part of the agent prototype. PowerShell port of
dev/model_server.sh for Windows workstations; both scripts do the same thing and
either may be used.

The agent is stateless between phases: design submits the experiment and exits,
and interpretation is a fresh process that only starts once results exist.
Nothing needs the model server during the benchmark itself, so the GPU can be
handed back to the cluster for the hours a run takes.

    .\dev\model_server.ps1 down     release the GPU (the weights PVC is kept)
    .\dev\model_server.ps1 up       start the server and wait until it answers

`down` is still the prompt path: the pod also releases the GPU on its own after
a long idle period, but that safety net is minutes-to-hours slower than saying
so directly.

This is the low-level server switch. It is intentionally outside agent/: the
submitted experiment and the agent remain usable without this operator
convenience.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string] $Action
)

$ErrorActionPreference = 'Stop'

$defaultManifest = (Resolve-Path (Join-Path $PSScriptRoot '..\agent\k8s\vllm-qwen38-27b.yml')).Path
$MANIFEST        = if ($env:MODEL_SERVER_MANIFEST) { $env:MODEL_SERVER_MANIFEST } else { $defaultManifest }
$POD            = if ($env:MODEL_SERVER_POD)      { $env:MODEL_SERVER_POD }      else { 'bexhoma-agent-model' }
$SVC            = if ($env:MODEL_SERVER_SERVICE)  { $env:MODEL_SERVER_SERVICE }  else { 'bexhoma-agent-model' }
$PORT          = if ($env:MODEL_SERVER_PORT)     { $env:MODEL_SERVER_PORT }     else { '8001' }
$BASE_URL      = if ($env:MODEL_SERVER_BASE_URL) { $env:MODEL_SERVER_BASE_URL } else { "http://localhost:$PORT/v1" }
$LOGIN         = if ($env:KUBE_LOGIN_SCRIPT)     { $env:KUBE_LOGIN_SCRIPT }     else { Join-Path $HOME 'git/BIRD-Interact/scripts/kube-login.sh' }
$CONTEXT       = if ($env:MODEL_SERVER_CONTEXT)  { $env:MODEL_SERVER_CONTEXT }  else { 'oidc_ds_cluster' }
$NAMESPACE     = if ($env:MODEL_SERVER_NAMESPACE){ $env:MODEL_SERVER_NAMESPACE }else { 'perdelt' }
$START_TIMEOUT = if ($env:MODEL_SERVER_START_TIMEOUT_SECONDS) { [int] $env:MODEL_SERVER_START_TIMEOUT_SECONDS } else { 2400 }
$STOP_TIMEOUT  = if ($env:MODEL_SERVER_STOP_TIMEOUT_SECONDS)  { [int] $env:MODEL_SERVER_STOP_TIMEOUT_SECONDS }  else { 300 }
$GENERATION    = if ($env:MODEL_SERVER_GENERATION) { $env:MODEL_SERVER_GENERATION } else { 'idle-watchdog-v2' }

$portForwardLog = Join-Path $env:TEMP 'vllm-portforward.log'

function Test-ModelEndpoint {
    <# True when the endpoint answers a /models request within three seconds. #>
    param([string] $Url)
    try {
        $null = Invoke-WebRequest -Uri "$Url/models" -TimeoutSec 3 -UseBasicParsing
        return $true
    } catch {
        return $false
    }
}

function Stop-PortForward {
    <# Kill any kubectl port-forward this script started for the model pod or service. #>
    Get-CimInstance Win32_Process -Filter "Name = 'kubectl.exe'" -ErrorAction SilentlyContinue |
        Where-Object {
            $_.CommandLine -and $_.CommandLine -match 'port-forward' -and
            ($_.CommandLine -match [regex]::Escape("pod/$POD") -or
             $_.CommandLine -match [regex]::Escape("svc/$SVC"))
        } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

function Assert-LastExitCode {
    param([string] $What)
    if ($LASTEXITCODE -ne 0) { throw "$What failed with exit code $LASTEXITCODE" }
}

function Invoke-EnsureLogin {
    <#
    A benchmark outlives the cluster token by hours, so a later `up` would fail
    at exactly the moment interpretation needs the server unless the session is
    refreshed here.
    #>
    if ($env:MODEL_SERVER_IN_CLUSTER -eq '1') {
        kubectl config set-context $CONTEXT --namespace=$NAMESPACE | Out-Null
        return
    }

    $null | & kubectl --context $CONTEXT auth whoami *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'cluster token expired; re-authenticating'
        $null | & bash $LOGIN *> $null
    }
    # Always restore the configured namespace: a valid token does not imply that
    # the context still points at the namespace where this user can write.
    kubectl config set-context $CONTEXT --namespace=$NAMESPACE | Out-Null
    $null | & kubectl --context $CONTEXT auth whoami *> $null
}

function Invoke-Down {
    Invoke-EnsureLogin
    kubectl --context $CONTEXT --namespace $NAMESPACE delete pod $POD `
        --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
    kubectl --context $CONTEXT --namespace $NAMESPACE delete svc $SVC `
        --ignore-not-found
    Stop-PortForward
    Write-Host 'model server down; the 150Gi weights volume is kept so restart needs no re-download'
}

function Invoke-Up {
    Invoke-EnsureLogin

    # A finished watchdog pod keeps its name, and Kubernetes cannot update a live
    # Pod's command or restart policy in place. Replace finished pods and older
    # immutable generations, while preserving a current loaded server.
    $goTemplate = 'go-template={{.status.phase}}|{{index .metadata.annotations "bexhoma.local/model-server-generation"}}'
    $podState = ''
    try {
        $podState = (& kubectl --context $CONTEXT --namespace $NAMESPACE get pod $POD -o $goTemplate 2>$null) -join ''
    } catch {
        $podState = ''
    }
    $parts = "$podState" -split '\|', 2
    $phase = $parts[0]
    $currentGeneration = if ($parts.Count -gt 1) { $parts[1] } else { '' }
    if ($phase -and ((($phase -ne 'Running') -and ($phase -ne 'Pending')) -or ($currentGeneration -ne $GENERATION))) {
        $shownGeneration = if ($currentGeneration) { $currentGeneration } else { 'unversioned' }
        Write-Host "replacing model pod in phase $phase, generation $shownGeneration"
        kubectl --context $CONTEXT --namespace $NAMESPACE delete pod $POD `
            --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
    }

    # The manifest names no namespace, so this flag is what places the objects.
    kubectl --context $CONTEXT --namespace $NAMESPACE apply -f $MANIFEST
    Assert-LastExitCode 'kubectl apply'
    kubectl --context $CONTEXT --namespace $NAMESPACE `
        wait --for=condition=ready "pod/$POD" --timeout="${START_TIMEOUT}s"
    Assert-LastExitCode 'kubectl wait'

    if (($BASE_URL -like 'http://localhost:*') -and -not (Test-ModelEndpoint $BASE_URL)) {
        Stop-PortForward
        Start-Process -FilePath 'kubectl' -WindowStyle Hidden `
            -ArgumentList @('--context', $CONTEXT, '--namespace', $NAMESPACE,
                            'port-forward', "svc/$SVC", "${PORT}:80") `
            -RedirectStandardOutput $portForwardLog `
            -RedirectStandardError "$portForwardLog.err"
    }

    $deadline = (Get-Date).AddSeconds($START_TIMEOUT)
    while (-not (Test-ModelEndpoint $BASE_URL)) {
        if ((Get-Date) -ge $deadline) {
            Write-Error "model server did not answer within ${START_TIMEOUT}s; see $portForwardLog"
            exit 1
        }
        Start-Sleep -Seconds 5
    }
    Write-Host "model server up and answering on localhost:$PORT"
}

switch ($Action) {
    'down' { Invoke-Down }
    'up'   { Invoke-Up }
    default {
        [Console]::Error.WriteLine("usage: $($MyInvocation.MyCommand.Name) {down|up}")
        exit 2
    }
}
