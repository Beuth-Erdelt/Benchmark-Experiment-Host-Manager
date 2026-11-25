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

BEXHOMA_NODE_SUT="cl-worker36"
BEXHOMA_NODE_LOAD="cl-worker38"
BEXHOMA_NODE_BENCHMARK="cl-worker38"
# worker pods of distributed DBMS (CockroachDB, Citus, TiDB, YugabyteDB), joined by '+'
# as bexhoma -rnw expects; without -rst their data sits on the nodes' local disks, so
# the nodes decide the results. _4 for 4 workers (one per node).
BEXHOMA_NODES_WORKER="cl-worker36+cl-worker37+cl-worker29"
BEXHOMA_NODES_WORKER_4="cl-worker36+cl-worker37+cl-worker29+cl-worker39"
LOG_DIR="./logs_tests"
BEXHOMA_MS=10
BEXHOMA_STORAGE_CLASS="nvme"


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


# wait_yugabytedb [timeout_seconds]
#   Waits after `helm install` of the YugabyteDB chart (release naming yb-master / yb-tserver)
#   until the master and tserver StatefulSets are rolled out and every tserver accepts
#   YSQL connections on port 5433. A fixed sleep is not enough: tservers may still be
#   pending or starting, and the first loader then fails with "connection refused".
#   Returns 1 on timeout (default 900s).
wait_yugabytedb() {
    local timeout=${1:-900}
    local deadline=$(( $(date +%s) + timeout ))

    echo "$(date '+%Y-%m-%d %H:%M:%S') Waiting for YugabyteDB StatefulSets..."
    kubectl rollout status statefulset/yb-master --timeout=${timeout}s || return 1
    kubectl rollout status statefulset/yb-tserver --timeout=$(( deadline - $(date +%s) ))s || return 1

    local replicas
    replicas=$(kubectl get statefulset yb-tserver -o jsonpath='{.spec.replicas}')
    local i=0
    while [[ $i -lt $replicas ]]; do
        if kubectl exec yb-tserver-0 -c yb-tserver -- /home/yugabyte/bin/ysqlsh \
            -h yb-tserver-$i.yb-tservers -p 5433 -U yugabyte -d yugabyte -At -c "SELECT 1" > /dev/null 2>&1; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') yb-tserver-$i accepts YSQL connections"
            i=$(( i + 1 ))
        elif [[ $(date +%s) -ge $deadline ]]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: yb-tserver-$i does not accept YSQL connections after ${timeout}s" >&2
            return 1
        else
            sleep 10
        fi
    done
    echo "$(date '+%Y-%m-%d %H:%M:%S') YugabyteDB is ready ($replicas tservers)"
}


# logs_open_for_writing
#   Reads log paths on stdin and prints those that another process has open for writing,
#   i.e. logs of runs that are still going (readers such as tail -F do not count).
#   Rewriting such a log in place (sed -i, perl -i, dos2unix) mixes it up with other logs
#   on Windows and cuts it off on Linux. Windows (Git Bash): an open for reading that does
#   not share write access fails while a writer holds the file. Linux: lsof access mode w/u.
#   Returns 2 if neither powershell.exe nor lsof is available.
logs_open_for_writing() {
    local files=()
    mapfile -t files
    [[ ${#files[@]} -eq 0 ]] && return 0
    if command -v powershell.exe >/dev/null 2>&1 && command -v cygpath >/dev/null 2>&1; then
        paste <(printf '%s\n' "${files[@]}") <(printf '%s\n' "${files[@]}" | cygpath -w -f -) \
        | powershell.exe -NoProfile -NonInteractive -Command '$input | ForEach-Object {
            $path, $win = $_ -split "`t", 2
            try { [IO.File]::Open($win, "Open", "Read", "Read").Close() } catch [IO.IOException] { $path }
          }' \
        | tr -d '\r'
    elif command -v lsof >/dev/null 2>&1; then
        local open file
        open=$(lsof -w -F an -- "${files[@]}" 2>/dev/null \
               | awk '/^a/ {mode = substr($0, 2)} /^n/ {if (mode ~ /[wu]/) print substr($0, 2)}')
        for file in "${files[@]}"; do
            grep -qxF -- "$(realpath "$file")" <<<"$open" && echo "$file"
        done
        return 0
    else
        return 2
    fi
}


# report_result <exit_code> <label>
#   Prints "[DONE] <label>" after a bexhoma call that returned 0 and "[FAIL] <label> (exit N)"
#   otherwise. bexhoma returns 1 if a test of the summary failed or the run crashed; skipped
#   tests and warnings do not fail. Pass $? right after the call: the redirect &>log does not
#   change it, a pipe (| tee) would. Counts the calls for report_total.
BEXHOMA_RUNS=0
BEXHOMA_RUNS_FAILED=0
report_result() {
    local code=$1 label=$2
    BEXHOMA_RUNS=$((BEXHOMA_RUNS + 1))
    if [[ "$code" -eq 0 ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] $label"
    else
        BEXHOMA_RUNS_FAILED=$((BEXHOMA_RUNS_FAILED + 1))
        echo "$(date '+%Y-%m-%d %H:%M:%S') [FAIL] $label  (exit $code)"
    fi
}


# report_total
#   Prints how many of the bexhoma calls reported by report_result failed.
report_total() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [SUMMARY] $BEXHOMA_RUNS_FAILED of $BEXHOMA_RUNS experiments failed"
}


# clean_logs [--force]
#   Strips kubectl token warnings from the logs and extracts their "## Show Summary" part
#   into <name>_summary.md. Off by default: runs only with BEXHOMA_CLEAN_LOGS=1 or --force.
#   Logs that are still being written (see logs_open_for_writing) are left alone.
clean_logs() {
    if [[ "${BEXHOMA_CLEAN_LOGS:-0}" != "1" && "$1" != "--force" ]]; then
        echo "Skipping log cleaning (set BEXHOMA_CLEAN_LOGS=1 or call clean_logs --force)."
        return 0
    fi

    if [[ -z "$LOG_DIR" ]]; then
        echo "LOG_DIR is not set. Please set it before calling clean_logs."
        return 1
    fi

    local logs=() open file
    mapfile -t logs < <(find "$LOG_DIR" -name '*.log' -type f | sort)
    if ! open=$(printf '%s\n' "${logs[@]}" | logs_open_for_writing); then
        echo "Error: cannot tell which logs are still being written (needs powershell.exe or lsof); logs not cleaned." >&2
        return 1
    fi
    local idle=()
    for file in "${logs[@]}"; do
        if [[ -n "$open" ]] && grep -qxF -- "$file" <<<"$open"; then
            echo "Skipping $file (still being written)"
        else
            idle+=("$file")
        fi
    done
    [[ ${#idle[@]} -eq 0 ]] && { echo "No logs to clean."; return 0; }

    echo "Removing connection warning lines from log files..."

    grep -l "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens." -- "${idle[@]}" \
    | xargs -r -d '\n' sed -i '/Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens./d'

    grep -l "Exception when calling CoreV1Api->" -- "${idle[@]}" \
    | xargs -r -d '\n' perl -0777 -i -pe 's/^Exception when calling CoreV1Api->.*\nReason: Unauthorized\nHTTP response headers: HTTPHeaderDict\(.*\nHTTP response body: .*\n(\n)*Create new access token\n//mg'

    echo "Extracting summaries from log files..."

    for file in "${idle[@]}"; do
        # summaries only for the logs directly in LOG_DIR, as before
        [[ "${file%/*}" == "${LOG_DIR%/}" ]] || continue
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
