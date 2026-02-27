#!/usr/bin/env bash

set -euo pipefail

source ./testfunctions.sh

BEXHOMA_NODE_SUT="cl-worker21"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p "$LOG_DIR"

if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"



WAIT_SECONDS=300   # 5 minutes
LOG_DIR=${LOG_DIR:-/tmp}

# Get all nodes containing "cl-worker"
NODES=$(kubectl get nodes -o name | sed 's|node/||' | grep cl-worker)

for NODE in $NODES; do
  echo "========================================"
  echo "Starting experiment on node: $NODE"
  echo "========================================"

  export BEXHOMA_NODE_SUT="$NODE"

  # Start workload
  nohup python ycsb.py -tr \
    -sf 1 \
    -sfo 10 \
    --workload a \
    -dbms Redis \
    -rnn "$BEXHOMA_NODE_SUT" \
    -rnl "$BEXHOMA_NODE_LOAD" \
    -rnb "$BEXHOMA_NODE_BENCHMARK" \
    -tb 16384 \
    -nlp 8 \
    -nlt 64 \
    -nlf 12 \
    -nbp 1 \
    -nbt 128 \
    -nbf 4 \
    -ne 1 \
    -nc 2 \
    -m -mc \
    -rst shared -rss 50Gi -rsr \
    -rr 1Gi -rc 0.1 \
    run </dev/null &>"$LOG_DIR/doc_ycsb_redis_$BEXHOMA_NODE_SUT.log" &

  YCSB_PID=$!

  echo "YCSB started (PID=$YCSB_PID), waiting 5 minutes..."
  sleep "$WAIT_SECONDS"

  # Check for Pending pods containing "sut"
DESCRIBE_DIR=${DESCRIBE_DIR:-./pod_describes}
mkdir -p "$DESCRIBE_DIR"

TS=$(date +"%Y%m%d_%H%M%S")

PENDING_SUT_PODS=$(kubectl get pods \
  --field-selector=status.phase=Pending \
  -o custom-columns=NAME:.metadata.name \
  --no-headers \
  | grep -i sut || true)

if [[ -n "$PENDING_SUT_PODS" ]]; then
  RESULT="FAILED"

  for POD in $PENDING_SUT_PODS; do
    OUT_FILE="$DESCRIBE_DIR/describe_${BEXHOMA_NODE_SUT}_${POD}_${TS}.txt"

    echo "Saving kubectl describe for pod $POD (node $BEXHOMA_NODE_SUT)"
    kubectl describe pod "$POD" > "$OUT_FILE"
  done

else
  RESULT="SUCCESS"
fi



  echo "Stopping YCSB and experiments on node: $NODE"

  # Kill all ycsb.py processes (defensive)
  pkill -f ycsb.py || true

  # Stop bexperiments
  bexperiments stop || true

  kubectl delete all -l app=bexhoma || true
  kubectl delete pvc -l component=storage || true

  echo "$RESULT - $NODE"
  echo

done
