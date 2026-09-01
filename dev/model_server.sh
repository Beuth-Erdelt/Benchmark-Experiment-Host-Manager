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
#
# `down` is still the prompt path: the pod also releases the GPU on its own
# after a long idle period, but that safety net is minutes-to-hours slower than
# saying so directly.
# This is the low-level server switch used by dev/agent_lifecycle.py.  It is
# intentionally outside agent/: the submitted experiment and the agent remain
# usable without this operator convenience.
set -euo pipefail

MANIFEST="${MODEL_SERVER_MANIFEST:-$(cd "$(dirname "$0")/.." && pwd)/agent/k8s/vllm-qwen38-27b.yml}"
POD="${MODEL_SERVER_POD:-bexhoma-agent-model}"
SVC="${MODEL_SERVER_SERVICE:-bexhoma-agent-model}"
PORT="${MODEL_SERVER_PORT:-8001}"
BASE_URL="${MODEL_SERVER_BASE_URL:-http://localhost:$PORT/v1}"
LOGIN="${KUBE_LOGIN_SCRIPT:-$HOME/git/BIRD-Interact/scripts/kube-login.sh}"
CONTEXT="${MODEL_SERVER_CONTEXT:-oidc_ds_cluster}"
NAMESPACE="${MODEL_SERVER_NAMESPACE:-}"
START_TIMEOUT="${MODEL_SERVER_START_TIMEOUT_SECONDS:-2400}"
STOP_TIMEOUT="${MODEL_SERVER_STOP_TIMEOUT_SECONDS:-300}"
GENERATION="${MODEL_SERVER_GENERATION:-idle-watchdog-v2}"

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

  dev/model_server.sh directly : export MODEL_SERVER_NAMESPACE=<namespace>
  dev/agent_lifecycle.py       : MODEL_SERVER_NAMESPACE=<namespace> in .env
  in-cluster lifecycle Job     : set automatically from the Job's namespace

It must equal credentials.k8s.context.<context>.namespace in cluster.config,
or bexhoma will place the benchmark somewhere else than the model server.
USAGE
        exit 2
    fi
    if [ "${MODEL_SERVER_IN_CLUSTER:-0}" = "1" ]; then
        kubectl config set-context "$CONTEXT" --namespace="$NAMESPACE" >/dev/null
        return
    fi
    if ! kubectl --context "$CONTEXT" auth whoami >/dev/null 2>&1 </dev/null; then
        echo "cluster token expired; re-authenticating"
        bash "$LOGIN" >/dev/null 2>&1 </dev/null
    fi
    # Always restore the configured namespace: a valid token does not imply
    # that the context still points at the namespace where this user can write.
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
    # A finished watchdog pod keeps its name, and Kubernetes cannot update a
    # live Pod's command or restart policy in place. Replace finished pods and
    # older immutable generations, while preserving a current loaded server.
    pod_state=$(kubectl --context "$CONTEXT" --namespace "$NAMESPACE" get pod "$POD" \
        -o go-template='{{.status.phase}}|{{index .metadata.annotations "bexhoma.local/model-server-generation"}}' \
        2>/dev/null || true)
    phase="${pod_state%%|*}"
    current_generation="${pod_state#*|}"
    if [ -n "$phase" ] && { \
        { [ "$phase" != "Running" ] && [ "$phase" != "Pending" ]; } \
        || [ "$current_generation" != "$GENERATION" ]; \
    }; then
        echo "replacing model pod in phase $phase, generation ${current_generation:-unversioned}"
        kubectl --context "$CONTEXT" --namespace "$NAMESPACE" delete pod "$POD" \
            --ignore-not-found --wait=true --timeout="${STOP_TIMEOUT}s"
    fi
    # The manifest names no namespace, so this flag is what places the objects.
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" apply -f "$MANIFEST"
    kubectl --context "$CONTEXT" --namespace "$NAMESPACE" \
        wait --for=condition=ready "pod/$POD" \
        --timeout="${START_TIMEOUT}s"
    if [[ "$BASE_URL" == http://localhost:* ]] \
        && ! curl -sf --max-time 3 "$BASE_URL/models" >/dev/null; then
        pkill -f "port-forward (pod/$POD|svc/$SVC)" 2>/dev/null || true
        setsid nohup kubectl --context "$CONTEXT" --namespace "$NAMESPACE" port-forward \
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
