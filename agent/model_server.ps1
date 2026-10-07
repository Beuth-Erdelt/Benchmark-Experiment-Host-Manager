<#
Operator helper, not part of the model-facing agent. PowerShell port of
agent/model_server.sh for Windows workstations; both scripts do the same thing
and either may be used.

The agent is stateless between phases: design submits the experiment and exits,
and interpretation is a fresh process that only starts once results exist.
Nothing needs the model server during the benchmark itself, so the GPU can be
handed back to the cluster for the hours a run takes.

    .\agent\model_server.ps1 down     release the GPU (the weights PVC is kept)
    .\agent\model_server.ps1 up       start the server and wait until it answers

`down` is still the prompt path: the pod also releases the GPU on its own after
a long idle period, but that safety net is minutes-to-hours slower than saying
so directly.

This is the low-level server switch, in agent/ beside agent/lifecycle.py. Nothing
under agent/harness/ (the model-facing code) uses it: the submitted experiment
and the agent remain usable without this operator convenience.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string] $Action
)

$ErrorActionPreference = 'Stop'

$defaultManifest = (Resolve-Path (Join-Path $PSScriptRoot 'k8s\vllm-qwen38-27b.yml')).Path
$MANIFEST        = if ($env:MODEL_SERVER_MANIFEST) { $env:MODEL_SERVER_MANIFEST } else { $defaultManifest }
$JOB            = if ($env:MODEL_SERVER_JOB)      { $env:MODEL_SERVER_JOB }      else { 'bexhoma-agent-model' }
$SVC            = if ($env:MODEL_SERVER_SERVICE)  { $env:MODEL_SERVER_SERVICE }  else { 'bexhoma-agent-model' }
$PORT          = if ($env:MODEL_SERVER_PORT)     { $env:MODEL_SERVER_PORT }     else { '8001' }
$BASE_URL      = if ($env:MODEL_SERVER_BASE_URL) { $env:MODEL_SERVER_BASE_URL } else { "http://localhost:$PORT/v1" }
$LOGIN         = if ($env:KUBE_LOGIN_SCRIPT)     { $env:KUBE_LOGIN_SCRIPT }     else { '' }
$CONTEXT       = if ($env:MODEL_SERVER_CONTEXT)  { $env:MODEL_SERVER_CONTEXT }  else { '' }
$NAMESPACE     = if ($env:MODEL_SERVER_NAMESPACE){ $env:MODEL_SERVER_NAMESPACE }else { '' }
# Counted from when the pod is scheduled; the wait for a GPU before that is
# unbounded by default, as startup waits for capacity by design.
$START_TIMEOUT = if ($env:MODEL_SERVER_START_TIMEOUT_SECONDS) { [int] $env:MODEL_SERVER_START_TIMEOUT_SECONDS } else { 2400 }
$SCHEDULE_TIMEOUT = if ($env:MODEL_SERVER_SCHEDULE_TIMEOUT_SECONDS) { [int] $env:MODEL_SERVER_SCHEDULE_TIMEOUT_SECONDS } else { 0 }
$STOP_TIMEOUT  = if ($env:MODEL_SERVER_STOP_TIMEOUT_SECONDS)  { [int] $env:MODEL_SERVER_STOP_TIMEOUT_SECONDS }  else { 300 }
# Each manifest carries its own generation annotation, so the expected value is
# read from the manifest being applied. A fixed default would call every other
# model's live Job outdated and replace it on each `up`.
$manifestGeneration = Select-String -Path $MANIFEST -Pattern '^\s*bexhoma\.local/model-server-generation:\s*(\S+)' |
    Select-Object -First 1 | ForEach-Object { $_.Matches[0].Groups[1].Value }
$GENERATION    = if ($env:MODEL_SERVER_GENERATION) { $env:MODEL_SERVER_GENERATION } elseif ($manifestGeneration) { $manifestGeneration } else { 'idle-watchdog-v3' }
# Set by agent/lifecycle.py when several lifecycles share this server.
$SHARED        = $env:MODEL_SERVER_SHARED -eq '1'

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
            ($_.CommandLine -match [regex]::Escape("pod/$JOB") -or
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
    # Required, with no default. The namespace decides whose objects this script
    # creates and deletes, and the set-context calls below write it into the
    # caller's kubeconfig, where every later namespace-less kubectl call --
    # bexhoma's SUT creation included -- inherits it. A default would therefore
    # not merely misplace the model server, it would redirect the whole run into
    # the account the default happens to name.
    if (-not $NAMESPACE) {
        [Console]::Error.WriteLine(@'
error: MODEL_SERVER_NAMESPACE is unset and has no default; it names the
       namespace the model server is created in and deleted from.

  agent/model_server.ps1 directly : $env:MODEL_SERVER_NAMESPACE = "<namespace>"
  agent/lifecycle.py              : MODEL_SERVER_NAMESPACE=<namespace> in .env
  in-cluster lifecycle Job        : set automatically from the Job's namespace

It must equal credentials.k8s.context.<context>.namespace in cluster.config,
or bexhoma will place the benchmark somewhere else than the model server.
'@)
        exit 2
    }
    # Required too, with no default for the same reason: a stranger's cluster
    # name would silently point every kubectl call below at it.
    if (-not $CONTEXT) {
        [Console]::Error.WriteLine('error: MODEL_SERVER_CONTEXT is unset and has no default; set it, ' +
            'or export it in .env, to the kubeconfig context this cluster is reached under.')
        exit 2
    }

    if ($env:MODEL_SERVER_IN_CLUSTER -eq '1') {
        kubectl config set-context $CONTEXT --namespace=$NAMESPACE | Out-Null
        return
    }

    # KUBE_LOGIN_SCRIPT has no default either: unlike NAMESPACE and CONTEXT this
    # one is optional -- an ordinary kubeconfig that never expires needs no
    # refresh -- so an expired token is reported below rather than handed to a
    # script that was never configured.
    if ((-not (Test-ClusterAuth)) -and $LOGIN) {
        # can-i failing could mean an expired token, but also a wrong context
        # name, an unreachable API server, or no VPN -- causes this check
        # cannot tell apart, so the message does not claim which one it is.
        Write-Host 'cluster auth check failed; attempting re-login'
        $ErrorActionPreference = 'Continue'
        $null | & bash $LOGIN *> $null
        $ErrorActionPreference = 'Stop'
    }
    # Always restore the configured namespace: a valid token does not imply that
    # the context still points at the namespace where this user can write.
    kubectl config set-context $CONTEXT --namespace=$NAMESPACE | Out-Null
    if (-not (Test-ClusterAuth)) {
        if ($LOGIN) {
            throw "cannot access namespace '$NAMESPACE' in context '$CONTEXT' after re-authenticating with $LOGIN"
        }
        throw ("cannot access namespace '$NAMESPACE' in context '$CONTEXT'; set KUBE_LOGIN_SCRIPT " +
            'to a script that refreshes credentials, or re-authenticate manually')
    }
}

function Test-ClusterAuth {
    <#
    True when the context's token is accepted and may read pods in the namespace.
    `auth whoami` is not usable here: it needs the SelfSubjectReview API, which
    not every cluster serves, whereas SelfSubjectAccessReview always is.
    #>
    # Under 'Stop', PowerShell 5.1 turns kubectl's stderr into a terminating error.
    $ErrorActionPreference = 'Continue'
    $null | & kubectl --context $CONTEXT --namespace $NAMESPACE auth can-i get pods *> $null
    return $LASTEXITCODE -eq 0
}

function Remove-LegacyPod {
    <#
    Before the server ran as a Job it was a bare pod under the Job's name, which
    the Service would still select alongside the Job's pod. Job pods always carry
    a generated suffix, so this name only ever matches such a leftover.
    #>
    kubectl --context $CONTEXT --namespace $NAMESPACE delete pod $JOB `
        --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
}

function Invoke-Down {
    Invoke-EnsureLogin
    kubectl --context $CONTEXT --namespace $NAMESPACE delete job $JOB `
        --ignore-not-found --cascade=foreground --wait=true --timeout="${STOP_TIMEOUT}s"
    Remove-LegacyPod
    kubectl --context $CONTEXT --namespace $NAMESPACE delete svc $SVC `
        --ignore-not-found
    Stop-PortForward
    Write-Host 'model server down; the weights volume is kept so restart needs no re-download'
}

function Get-PodState {
    <# "<pod>|<PodScheduled status>" of the Job's live pod, or '' while it has none. #>
    # Under 'Stop', PowerShell 5.1 turns kubectl's stderr into a terminating error.
    $ErrorActionPreference = 'Continue'
    $template = 'go-template={{range .items}}{{if not .metadata.deletionTimestamp}}{{.metadata.name}}|{{range .status.conditions}}{{if eq .type `PodScheduled`}}{{.status}}{{end}}{{end}}{{println}}{{end}}{{end}}'
    $lines = & kubectl --context $CONTEXT --namespace $NAMESPACE get pods -l "job-name=$JOB" -o $template 2>$null
    return "$(@($lines | Where-Object { $_ }) | Select-Object -First 1)"
}

function Write-WaitingReport {
    <#
    One line on why the server is not answering yet, so that a long `up` says
    what it waits for instead of looking hung: the scheduler's latest refusal
    while the pod pends, the server's latest log line once it is loading.
    #>
    param([string] $Pod, [string] $Scheduled)
    $ErrorActionPreference = 'Continue'
    if (-not $Pod) {
        Write-Host 'waiting: the model Job has no pod yet'
    } elseif ($Scheduled -ne 'True') {
        $detail = (& kubectl --context $CONTEXT --namespace $NAMESPACE get events `
            --field-selector "involvedObject.name=$Pod,reason=FailedScheduling" `
            --sort-by=.lastTimestamp -o 'jsonpath={.items[-1:].message}' 2>$null) -join ' '
        if (-not $detail) { $detail = "pod $Pod is pending" }
        Write-Host "waiting for a GPU node: $detail"
    } else {
        # The idle watchdog logs an unreadable /metrics every poll while the
        # engine loads; progress bars redraw with carriage returns.
        $detail = @(& kubectl --context $CONTEXT --namespace $NAMESPACE logs $Pod --tail=20 2>$null) |
            ForEach-Object { $_ -split "`r" } |
            Where-Object { $_.Trim() -and $_ -notmatch '^metrics unreadable' } |
            Select-Object -Last 1
        if ($detail) {
            $detail = $detail.Substring(0, [Math]::Min(200, $detail.Length))
        } else {
            $detail = "pod $Pod is starting"
        }
        Write-Host "loading: $detail"
    }
}

function Get-JobField {
    <# One field of the model Job, or '' when there is no such Job. #>
    param([string] $Output)
    try {
        return (& kubectl --context $CONTEXT --namespace $NAMESPACE get job $JOB -o $Output 2>$null) -join ''
    } catch {
        return ''
    }
}

function Remove-FinishedJob {
    <#
    Deletes the finished model Job with this uid, and its pod, and waits until
    both are gone. The uid precondition is what makes this safe when lifecycles
    share the server: they arrive together, and another may already have replaced
    the finished Job with a starting one under the same name, which must survive.
    The server answers that case with a Conflict, and it is left alone.
    #>
    param([string] $Uid)
    # Under Stop, Windows PowerShell turns the first line kubectl writes to
    # stderr into a terminating error, before the Conflict could be recognised.
    $ErrorActionPreference = 'Continue'
    $body ='{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground","preconditions":{"uid":"' + $Uid + '"}}'
    # A file rather than a pipe: Windows PowerShell prefixes piped text with a
    # byte-order mark, which kubectl's JSON parser rejects.
    $bodyFile = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllText($bodyFile, $body)
        $output = (& kubectl --context $CONTEXT delete `
            --raw "/apis/batch/v1/namespaces/$NAMESPACE/jobs/$JOB" -f $bodyFile 2>&1) -join "`n"
    } finally {
        Remove-Item -LiteralPath $bodyFile -Force -ErrorAction SilentlyContinue
    }
    if (($LASTEXITCODE -ne 0) -and ($output -notmatch 'Conflict|NotFound')) {
        throw "deleting the finished model Job failed: $output"
    }
    $deadline = (Get-Date).AddSeconds($STOP_TIMEOUT)
    while ((Get-JobField 'jsonpath={.metadata.uid}') -eq $Uid) {
        if ((Get-Date) -ge $deadline) {
            throw "finished model Job was not deleted within ${STOP_TIMEOUT}s"
        }
        Start-Sleep -Seconds 2
    }
}

function Invoke-Up {
    Invoke-EnsureLogin
    Remove-LegacyPod

    # A finished Job keeps its name until its TTL runs out, and Kubernetes
    # cannot update a Job's pod template in place. Replace finished Jobs and
    # older immutable generations, while preserving a current loaded server.
    # Go raw strings in backquotes, because Windows PowerShell strips the double
    # quotes from a native command's argument and the template would not parse.
    $goTemplate = 'go-template={{.metadata.uid}}|{{range .status.conditions}}{{if eq .status `True`}}{{.type}} {{end}}{{end}}|{{index .metadata.annotations `bexhoma.local/model-server-generation`}}'
    $parts = "$(Get-JobField $goTemplate)" -split '\|', 3
    $uid = $parts[0]
    $conditions = if ($parts.Count -gt 1) { $parts[1] -split ' ' } else { @() }
    $currentGeneration = if ($parts.Count -gt 2) { $parts[2] } else { '' }
    $shownGeneration = if ($currentGeneration) { $currentGeneration } else { 'unversioned' }
    # Complete and Failed are set once the pod has ended; the other two already
    # while it terminates, and a terminating server is no more usable.
    $finished = $conditions | Where-Object { $_ -in @('Complete', 'Failed', 'SuccessCriteriaMet', 'FailureTarget') } |
        Select-Object -Last 1
    if ($uid -and $finished) {
        Write-Host "replacing finished model Job ($finished)"
        Remove-FinishedJob $uid
    } elseif ($uid -and ($currentGeneration -ne $GENERATION)) {
        if ($SHARED) {
            [Console]::Error.WriteLine("model Job runs generation $shownGeneration, not $GENERATION; another lifecycle is using that model, so it is left alone")
            exit 3
        }
        Write-Host "replacing model Job of generation $shownGeneration"
        kubectl --context $CONTEXT --namespace $NAMESPACE delete job $JOB `
            --ignore-not-found --cascade=foreground --wait=true --timeout="${STOP_TIMEOUT}s"
    }

    # The manifest names no namespace, so this flag is what places the objects.
    # Lifecycles sharing the server may both have deleted the finished Job, and
    # the one that loses the race to create its replacement fails AlreadyExists;
    # applied again, it finds that replacement and keeps it.
    kubectl --context $CONTEXT --namespace $NAMESPACE apply -f $MANIFEST
    if ($LASTEXITCODE -ne 0) {
        kubectl --context $CONTEXT --namespace $NAMESPACE apply -f $MANIFEST
    }
    Assert-LastExitCode 'kubectl apply'
    # The Job's pod has a generated name, so readiness is read off the Job. The
    # start timeout only runs once the pod is scheduled: waiting for a free GPU
    # took 2.5 hours on 2026-09-30 and is bounded by SCHEDULE_TIMEOUT instead.
    $waitingSince = Get-Date
    $scheduledAt = $null
    $lastReport = $null
    while ((Get-JobField 'jsonpath={.status.ready}') -ne '1') {
        $pod, $scheduled = (Get-PodState) -split '\|', 2
        if ((-not $scheduledAt) -and ($scheduled -eq 'True')) {
            $scheduledAt = Get-Date
            Write-Host "model pod $pod scheduled after $([int]($scheduledAt - $waitingSince).TotalSeconds)s; loading the model"
        }
        if (-not $scheduledAt) {
            if (($SCHEDULE_TIMEOUT -gt 0) -and ((Get-Date) -ge $waitingSince.AddSeconds($SCHEDULE_TIMEOUT))) {
                Write-Error "model pod was not scheduled within ${SCHEDULE_TIMEOUT}s; see kubectl describe job/$JOB"
                exit 1
            }
        } elseif ((Get-Date) -ge $scheduledAt.AddSeconds($START_TIMEOUT)) {
            Write-Error "model pod was not ready within ${START_TIMEOUT}s of being scheduled; see kubectl logs job/$JOB"
            exit 1
        }
        if ((-not $lastReport) -or ((Get-Date) -ge $lastReport.AddSeconds(60))) {
            $lastReport = Get-Date
            Write-WaitingReport $pod $scheduled
        }
        Start-Sleep -Seconds 5
    }

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
