#!/usr/bin/env bash
# Dev-only operator helper, NOT part of the agent prototype.
#
# The agent is stateless between phases: design submits the experiment and
# exits, and interpretation is a fresh process that only starts once results
# exist. Nothing needs the model server during the benchmark itself, so the
# GPU can be handed back to the cluster for the hours a run takes.
#
#   down                        release the GPU (the weights PVC is kept)
#   up                          start the server and wait until it answers
# This is the low-level server switch used by dev/agent_lifecycle.py.  It is
# intentionally outside agent/: the submitted experiment and the agent remain
# usable without this operator convenience.
set -euo pipefail

MANIFEST="${MODEL_SERVER_MANIFEST:-$(cd "$(dirname "$0")/.." && pwd)/agent/k8s/vllm-qwen38-27b.yml}"
POD="${MODEL_SERVER_POD:-vllm-qwen38-server}"
SVC="${MODEL_SERVER_SERVICE:-vllm-qwen38-service}"
PORT="${MODEL_SERVER_PORT:-8001}"
LOGIN="${KUBE_LOGIN_SCRIPT:-$HOME/git/BIRD-Interact/scripts/kube-login.sh}"
CONTEXT="${MODEL_SERVER_CONTEXT:-oidc_ds_cluster}"
NAMESPACE="${MODEL_SERVER_NAMESPACE:-lliu}"
START_TIMEOUT="${MODEL_SERVER_START_TIMEOUT_SECONDS:-2400}"
STOP_TIMEOUT="${MODEL_SERVER_STOP_TIMEOUT_SECONDS:-300}"

# A benchmark outlives the cluster token by hours, so a later `up` would fail at
# exactly the moment interpretation needs the server unless we refresh here.
ensure_login() {
    if kubectl --context "$CONTEXT" auth whoami >/dev/null 2>&1 </dev/null; then
        return
    fi
    echo "cluster token expired; re-authenticating"
    bash "$LOGIN" >/dev/null 2>&1 </dev/null
    # kube-login.sh recreates the context and drops the namespace with it;
    # without this every object would go to a namespace we cannot write to.
    kubectl config set-context "$CONTEXT" --namespace="$NAMESPACE" >/dev/null
    kubectl --context "$CONTEXT" auth whoami >/dev/null 2>&1 </dev/null
}

down() {
    ensure_login
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete pod "$POD" \
        --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete svc "$SVC" \
        --ignore-not-found
    pkill -f "port-forward (pod/$POD|svc/$SVC)" 2>/dev/null || true
    echo "model server down; the 150Gi weights volume is kept so restart needs no re-download"
}

up() {
    ensure_login
    kubectl --context "$CONTEXT" apply -f "$MANIFEST"
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" \
        wait --for=condition=ready "pod/$POD" \
        --timeout="${START_TIMEOUT}s"
    if ! curl -sf --max-time 3 "http://localhost:$PORT/v1/models" >/dev/null; then
        pkill -f "port-forward (pod/$POD|svc/$SVC)" 2>/dev/null || true
        setsid nohup kubectl --context "$CONTEXT" --namespace "$NAMESPACE" port-forward \
            "svc/$SVC" "$PORT:80" >/tmp/vllm-portforward.log 2>&1 &
    fi
    deadline=$((SECONDS + START_TIMEOUT))
    until curl -sf --max-time 3 "http://localhost:$PORT/v1/models" >/dev/null; do
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
