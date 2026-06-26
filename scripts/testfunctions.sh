#!/bin/bash
# Shared helper functions, default variables, and startup checks sourced by all
# bexhoma test scripts.
#
# Declares default node/path variables, defines helper functions, then runs
# prerequisite checks (files, directories, log folder) so every script that
# sources this file starts in a known-good state.
#
# Default node values can be overridden in the sourcing script after this line:
#   source ./scripts/testfunctions.sh
#   BEXHOMA_NODE_SUT="other-node"   # override example
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# ---------------------------------------------------------------------------
# Default variable values (override after sourcing if needed)
# ---------------------------------------------------------------------------

BEXHOMA_NODE_SUT="cl-worker38"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_MS=10
BEXHOMA_STORAGE_CLASS="shared"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


prepare_logs() {
    if [[ -z "$LOG_DIR" ]]; then
        echo "LOG_DIR is not set." >&2
        return 1
    fi

    if ! mkdir -p "$LOG_DIR"; then
        echo "Failed to create log directory: $LOG_DIR" >&2
        return 2
    fi
}


wait_process() {
    local process_name=$1

    while ps aux | grep "[p]ython $process_name.py" > /dev/null; do
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for process python $process_name.py to terminate..."
        sleep 60
    done

    echo "$(date +"%Y-%m-%d %H:%M:%S"): Process python $process_name.py has terminated."
}


clean_logs() {
    export MYDIR=$(pwd)

    if [[ -z "$LOG_DIR" ]]; then
        echo "LOG_DIR is not set. Please set it before calling clean_logs."
        return 1
    fi

    cd "$LOG_DIR" || { echo "Failed to change directory to $LOG_DIR"; return 1; }

    echo "Removing connection warning lines from log files..."

    grep -rl "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens." . \
    | xargs sed -i '/Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens./d'

    grep -rl "Exception when calling CoreV1Api->" . \
    | xargs perl -0777 -i -pe 's/^Exception when calling CoreV1Api->.*\nReason: Unauthorized\nHTTP response headers: HTTPHeaderDict\(.*\nHTTP response body: .*\n(\n)*Create new access token\n//mg'

    cd "$MYDIR" || return

    echo "Extracting summaries from log files..."

    for file in "$LOG_DIR"/*.log; do
        echo "Cleaning $file"
        filename=$(basename "$file" .log)
        dos2unix "$file"
        awk '/## Show Summary/ {show=1} show {print}' "$file" > "$LOG_DIR/${filename}_summary.md"
    done

    echo "Extraction complete! Files are saved in $LOG_DIR."
}


# ---------------------------------------------------------------------------
# Startup checks (run at source time)
# ---------------------------------------------------------------------------

if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."

if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."

# ---------------------------------------------------------------------------
# Wait for any pre-existing jobs
# ---------------------------------------------------------------------------

#wait_process "tpch"
#wait_process "tpcds"
#wait_process "hammerdb"
#wait_process "benchbase"
#wait_process "ycsb"
