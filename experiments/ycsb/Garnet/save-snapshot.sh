# Benchmark-Experiment-Host-Manager | experiments/ycsb/Garnet
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Pre-benchmark reset for YCSB on Garnet, run before each
#          benchmarking round with -ar: in the SUT pod (standalone) or on
#          every worker (cluster, script target 'workers'). Steps of the reset
#          contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
#          redis-cli is copied into the pod by the init container.
#          SAVE (a checkpoint) answers "ERR checkpoint already in progress"
#          while another one runs (e.g. a replica syncing from its primary),
#          so the script retries until that one is done.
#          No curly braces in this file: bexhoma may fill it with str.format().

# step 1 (statistics): n/a - key-value store without optimizer statistics

# step 2 (persist): SAVE takes a checkpoint into --checkpointdir
TIMEOUT=600
waited=0
while true; do
  echo "invoking SAVE"
  reply=$(redis-cli SAVE)
  if ! echo "$reply" | grep -q "checkpoint already in progress"; then
    echo "$reply"
    break
  fi
  echo "checkpoint in progress, retrying"
  if [ $waited -ge $TIMEOUT ]; then
    echo "$reply"
    break
  fi
  sleep 1
  waited=$((waited+1))
done
echo "waited $waited s for a running checkpoint"

# step 3 (counters): n/a - Garnet does not support CONFIG RESETSTAT
