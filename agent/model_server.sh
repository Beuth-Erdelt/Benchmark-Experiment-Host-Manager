#!/usr/bin/env bash
# Operator helper, not part of the model-facing agent.
#
# The agent is stateless between phases: design submits the experiment and
# exits, and interpretation is a fresh process that only starts once results
# exist. Nothing needs the model server during the benchmark itself, so the
# GPU can be handed back to the cluster for the hours a run takes.
#
#   down                        release the GPU (the weights PVC is kept)
#   up                          start the server and wait until it answers
#
# `down` is still the prompt path: the pod also releases the GPU on its own
# after a long idle period, but that safety net is minutes-to-hours slower than
# saying so directly.
# This is the low-level server switch used by `agent/lifecycle.py`. It sits in
# agent/ beside that wrapper, but nothing under agent/harness/ (the model-facing
# code) uses it: the submitted experiment and the agent remain usable without
# this operator convenience.
set -euo pipefail

MANIFEST="${MODEL_SERVER_MANIFEST:-$(cd "$(dirname "$0")" && pwd)/k8s/vllm-qwen38-27b.yml}"
JOB="${MODEL_SERVER_JOB:-bexhoma-agent-model}"
SVC="${MODEL_SERVER_SERVICE:-bexhoma-agent-model}"
PORT="${MODEL_SERVER_PORT:-8001}"
BASE_URL="${MODEL_SERVER_BASE_URL:-http://localhost:$PORT/v1}"
LOGIN="${KUBE_LOGIN_SCRIPT:-}"
CONTEXT="${MODEL_SERVER_CONTEXT:-}"
NAMESPACE="${MODEL_SERVER_NAMESPACE:-}"
# Counted from when the pod is scheduled; the wait for a GPU before that is
# unbounded by default, as startup waits for capacity by design.
START_TIMEOUT="${MODEL_SERVER_START_TIMEOUT_SECONDS:-2400}"
SCHEDULE_TIMEOUT="${MODEL_SERVER_SCHEDULE_TIMEOUT_SECONDS:-0}"
STOP_TIMEOUT="${MODEL_SERVER_STOP_TIMEOUT_SECONDS:-300}"
# Each manifest carries its own generation annotation, so the expected value is
# read from the manifest being applied. A fixed default would call every other
# model's live Job outdated and replace it on each `up`.
MANIFEST_GENERATION=$(sed -n 's/^ *bexhoma\.local\/model-server-generation: *//p' "$MANIFEST" | head -n 1)
GENERATION="${MODEL_SERVER_GENERATION:-${MANIFEST_GENERATION:-idle-watchdog-v3}}"
# Set by agent/lifecycle.py when several lifecycles share this server.
SHARED="${MODEL_SERVER_SHARED:-0}"

# A benchmark outlives the cluster token by hours, so a later `up` would fail at
# exactly the moment interpretation needs the server unless we refresh here.
ensure_login() {
    # Required, with no default. The namespace decides whose objects this script
    # creates and deletes, and the set-context calls below write it into the
    # caller's kubeconfig, where every later namespace-less kubectl call --
    # bexhoma's SUT creation included -- inherits it. A default would therefore
    # not merely misplace the model server, it would redirect the whole run into
    # the account the default happens to name.
    if [ -z "$NAMESPACE" ]; then
        cat >&2 <<'USAGE'
error: MODEL_SERVER_NAMESPACE is unset and has no default; it names the
       namespace the model server is created in and deleted from.

  agent/model_server.sh directly : export MODEL_SERVER_NAMESPACE=<namespace>
  agent/lifecycle.py             : MODEL_SERVER_NAMESPACE=<namespace> in .env
  in-cluster lifecycle Job       : set automatically from the Job's namespace

It must equal credentials.k8s.context.<context>.namespace in cluster.config,
or bexhoma will place the benchmark somewhere else than the model server.
USAGE
        exit 2
    fi
    # Required too, with no default for the same reason: a stranger's cluster
    # name would silently point every kubectl call below at it.
    if [ -z "$CONTEXT" ]; then
        echo "error: MODEL_SERVER_CONTEXT is unset and has no default; export it," \
             "or set it in .env, to the kubeconfig context this cluster is" \
             "reached under." >&2
        exit 2
    fi
    if [ "${MODEL_SERVER_IN_CLUSTER:-0}" = "1" ]; then
        kubectl config set-context "$CONTEXT" --namespace="$NAMESPACE" >/dev/null
        return
    fi
    # KUBE_LOGIN_SCRIPT has no default either: unlike NAMESPACE and CONTEXT
    # this one is optional -- an ordinary kubeconfig that never expires needs
    # no refresh -- so an expired token is reported below rather than handed
    # to a script that was never configured.
    if ! cluster_auth_ok && [ -n "$LOGIN" ]; then
        # can-i failing could mean an expired token, but also a wrong context
        # name, an unreachable API server, or no VPN -- causes this check
        # cannot tell apart, so the message does not claim which one it is.
        echo "cluster auth check failed; attempting re-login"
        bash "$LOGIN" >/dev/null 2>&1 </dev/null || true
    fi
    # Always restore the configured namespace: a valid token does not imply
    # that the context still points at the namespace where this user can write.
    kubectl config set-context "$CONTEXT" --namespace="$NAMESPACE" >/dev/null
    if ! cluster_auth_ok; then
        if [ -n "$LOGIN" ]; then
            echo "cannot access namespace '$NAMESPACE' in context '$CONTEXT' after re-authenticating with $LOGIN" >&2
        else
            echo "cannot access namespace '$NAMESPACE' in context '$CONTEXT'; set" \
                 "KUBE_LOGIN_SCRIPT to a script that refreshes credentials, or" \
                 "re-authenticate manually" >&2
        fi
        exit 1
    fi
}

# True when the context's token is accepted and may read pods in the namespace.
# `auth whoami` is not usable here: it needs the SelfSubjectReview API, which
# not every cluster serves, whereas SelfSubjectAccessReview always is.
cluster_auth_ok() {
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" auth can-i get pods \
        >/dev/null 2>&1 </dev/null
}

# Before the server ran as a Job it was a bare pod under the Job's name, which
# the Service would still select alongside the Job's pod. Job pods always carry
# a generated suffix, so this name only ever matches such a leftover.
delete_legacy_pod() {
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete pod "$JOB" \
        --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
}

down() {
    ensure_login
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete job "$JOB" \
        --ignore-not-found --cascade=foreground --wait=true --timeout="${STOP_TIMEOUT}s"
    delete_legacy_pod
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete svc "$SVC" \
        --ignore-not-found
    pkill -f "port-forward (pod/$JOB|svc/$SVC)" 2>/dev/null || true
    echo "model server down; the weights volume is kept so restart needs no re-download"
}

# "<pod>|<PodScheduled status>" of the Job's live pod, or "|" while it has none.
pod_state() {
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get pods -l "job-name=$JOB" \
        -o go-template='{{range .items}}{{if not .metadata.deletionTimestamp}}{{.metadata.name}}|{{range .status.conditions}}{{if eq .type "PodScheduled"}}{{.status}}{{end}}{{end}}{{"\n"}}{{end}}{{end}}' \
        2>/dev/null | head -n 1 || true
}

# One line on why the server is not answering yet, so that a long `up` says
# what it waits for instead of looking hung: the scheduler's latest refusal
# while the pod pends, the server's latest log line once it is loading.
report_waiting() {
    local pod="$1" scheduled="$2" detail
    if [ -z "$pod" ]; then
        echo "waiting: the model Job has no pod yet"
    elif [ "$scheduled" != "True" ]; then
        detail=$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get events \
            --field-selector "involvedObject.name=$pod,reason=FailedScheduling" \
            --sort-by=.lastTimestamp -o jsonpath='{.items[-1:].message}' 2>/dev/null || true)
        echo "waiting for a GPU node: ${detail:-pod $pod is pending}"
    else
        # The idle watchdog logs an unreadable /metrics every poll while the
        # engine loads; progress bars redraw with carriage returns.
        detail=$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" logs "$pod" --tail=20 2>/dev/null \
            | tr '\r' '\n' | grep -v '^metrics unreadable\|^ *$' | tail -n 1 | cut -c1-200 || true)
        echo "loading: ${detail:-pod $pod is starting}"
    fi
}

# Deletes the finished model Job with this uid, and its pod, and waits until
# both are gone. The uid precondition is what makes this safe when lifecycles
# share the server: they arrive together, and another may already have replaced
# the finished Job with a starting one under the same name, which must survive.
# The server answers that case with a Conflict, and it is left alone.
delete_finished_job() {
    local uid="$1" output deadline
    # MSYS_NO_PATHCONV keeps Git Bash on Windows from rewriting the API path.
    if ! output=$(printf '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground","preconditions":{"uid":"%s"}}' "$uid" \
        | MSYS_NO_PATHCONV=1 kubectl --context "$CONTEXT" delete \
            --raw "/apis/batch/v1/namespaces/$NAMESPACE/jobs/$JOB" -f - 2>&1); then
        case "$output" in
            *Conflict*|*NotFound*) ;;
            *) echo "$output" >&2; exit 1 ;;
        esac
    fi
    deadline=$((SECONDS + STOP_TIMEOUT))
    while [ "$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get job "$JOB" \
        -o jsonpath='{.metadata.uid}' 2>/dev/null || true)" = "$uid" ]; do
        if (( SECONDS >= deadline )); then
            echo "finished model Job was not deleted within ${STOP_TIMEOUT}s" >&2
            exit 1
        fi
        sleep 2
    done
}

up() {
    ensure_login
    delete_legacy_pod
    # A finished Job keeps its name until its TTL runs out, and Kubernetes
    # cannot update a Job's pod template in place. Replace finished Jobs and
    # older immutable generations, while preserving a current loaded server.
    job_state=$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get job "$JOB" \
        -o go-template='{{.metadata.uid}}|{{range .status.conditions}}{{if eq .status "True"}}{{.type}} {{end}}{{end}}|{{index .metadata.annotations "bexhoma.local/model-server-generation"}}' \
        2>/dev/null || true)
    IFS='|' read -r uid conditions current_generation <<<"$job_state"
    # Complete and Failed are set once the pod has ended; the other two already
    # while it terminates, and a terminating server is no more usable.
    finished=""
    for condition in $conditions; do
        case "$condition" in
            Complete|Failed|SuccessCriteriaMet|FailureTarget) finished="$condition" ;;
        esac
    done
    if [ -n "$uid" ] && [ -n "$finished" ]; then
        echo "replacing finished model Job ($finished)"
        delete_finished_job "$uid"
    elif [ -n "$uid" ] && [ "$current_generation" != "$GENERATION" ]; then
        if [ "$SHARED" = "1" ]; then
            echo "model Job runs generation ${current_generation:-unversioned}, not $GENERATION;" \
                "another lifecycle is using that model, so it is left alone" >&2
            exit 3
        fi
        echo "replacing model Job of generation ${current_generation:-unversioned}"
        kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete job "$JOB" \
            --ignore-not-found --cascade=foreground --wait=true --timeout="${STOP_TIMEOUT}s"
    fi
    # The manifest names no namespace, so this flag is what places the objects.
    # Lifecycles sharing the server may both have deleted the finished Job, and
    # the one that loses the race to create its replacement fails AlreadyExists;
    # applied again, it finds that replacement and keeps it.
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" apply -f "$MANIFEST"         || kubectl --context "$CONTEXT" --namespace "$NAMESPACE" apply -f "$MANIFEST"
    # The Job's pod has a generated name, so readiness is read off the Job. The
    # start timeout only runs once the pod is scheduled: waiting for a free GPU
    # took 2.5 hours on 2026-09-30 and is bounded by SCHEDULE_TIMEOUT instead.
    waiting_since=$SECONDS
    scheduled_at=""
    last_report=""
    until [ "$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get job "$JOB" \
        -o jsonpath='{.status.ready}' 2>/dev/null || true)" = "1" ]; do
        IFS='|' read -r pod scheduled <<<"$(pod_state)"
        if [ -z "$scheduled_at" ] && [ "$scheduled" = "True" ]; then
            scheduled_at=$SECONDS
            echo "model pod $pod scheduled after $((SECONDS - waiting_since))s; loading the model"
        fi
        if [ -z "$scheduled_at" ]; then
            if (( SCHEDULE_TIMEOUT > 0 && SECONDS - waiting_since >= SCHEDULE_TIMEOUT )); then
                echo "model pod was not scheduled within ${SCHEDULE_TIMEOUT}s; see kubectl describe job/$JOB" >&2
                exit 1
            fi
        elif (( SECONDS - scheduled_at >= START_TIMEOUT )); then
            echo "model pod was not ready within ${START_TIMEOUT}s of being scheduled; see kubectl logs job/$JOB" >&2
            exit 1
        fi
        if [ -z "$last_report" ] || (( SECONDS - last_report >= 60 )); then
            last_report=$SECONDS
            report_waiting "$pod" "$scheduled"
        fi
        sleep 5
    done
    if [[ "$BASE_URL" == http://localhost:* ]] \
        && ! curl -sf --max-time 3 "$BASE_URL/models" >/dev/null; then
        pkill -f "port-forward (pod/$JOB|svc/$SVC)" 2>/dev/null || true
        # macOS ships no setsid. Without this fallback the forward never
        # starts there, and the wait below times out on a server that is up.
        detach=""
        if command -v setsid >/dev/null 2>&1; then
            detach="setsid"
        fi
        $detach nohup kubectl --context "$CONTEXT" --namespace "$NAMESPACE" port-forward \
            "svc/$SVC" "$PORT:80" >/tmp/vllm-portforward.log 2>&1 &
    fi
    deadline=$((SECONDS + START_TIMEOUT))
    until curl -sf --max-time 3 "$BASE_URL/models" >/dev/null; do
        if (( SECONDS >= deadline )); then
            echo "model server did not answer within ${START_TIMEOUT}s; see /tmp/vllm-portforward.log" >&2
            exit 1
        fi
        sleep 5
    done
    echo "model server up and answering on localhost:$PORT"
}

case "${1:-}" in
    down) down ;;
    up)   up ;;
    *) echo "usage: $0 {down|up}" >&2; exit 2 ;;
esac
