#!/bin/bash
# Shared helper functions and default variable values sourced by all bexhoma test scripts.
#
# Provides wait helpers, log-extraction utilities, and default node assignments
# (BEXHOMA_NODE_SUT, BEXHOMA_NODE_LOAD, BEXHOMA_NODE_BENCHMARK). Source this
# file at the top of every test script with: source ./scripts/testfunctions.sh
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# some default values
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

###########################################
########## Prepare log folder #############
###########################################


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



###########################################
### Wait for benchmarking to complete #####
###########################################


wait_process() {
    local process_name=$1

    # Wait until the process with the name passed as an argument has terminated
    while ps aux | grep "[p]ython $process_name.py" > /dev/null; do
        # Process is still running, wait for 5 seconds
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for process python $process_name.py to terminate..."
        sleep 60
    done

    echo "$(date +"%Y-%m-%d %H:%M:%S"): Process python $process_name.py has terminated."
}

# Example usage
#wait_process "tpch"




###########################################
############## Clean Folder ###############
###########################################


clean_logs() {
    export MYDIR=$(pwd)

    if [[ -z "$LOG_DIR" ]]; then
        echo "LOG_DIR is not set. Please set it before calling clean_logs."
        return 1
    fi

    cd "$LOG_DIR" || { echo "Failed to change directory to $LOG_DIR"; return 1; }

    echo "Removing connection warning lines from log files..."

    # Remove the specific warning from all files recursively
    grep -rl "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens." . \
    | xargs sed -i '/Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens./d'

    cd "$MYDIR" || return

    echo "Extracting summaries from log files..."

    # Loop over each .log file in LOG_DIR
    for file in "$LOG_DIR"/*.log; do
        echo "Cleaning $file"
        filename=$(basename "$file" .log)
        dos2unix "$file"
        awk '/## Show Summary/ {show=1} show {print}' "$file" > "$LOG_DIR/${filename}_summary.md"
    done

    echo "Extraction complete! Files are saved in $LOG_DIR."
}
