# Benchmark-Experiment-Host-Manager | experiments/ycsb/Cassandra
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: After the load, and before each benchmarking round with -ar: in the
#          SUT pod (single node) or on every worker (cluster, script target
#          'workers'). Steps of the reset contract (docs/DBMS.md): 1 statistics,
#          2 persist, 3 counters. Writes the memtables to SSTables and waits for
#          the compactions they cause, which would otherwise run during the
#          benchmark. Fails after 30 minutes.
#          No curly braces in this file: bexhoma may fill it with str.format().

# step 1 (statistics): n/a - no optimizer statistics to compute

# step 2 (persist)
echo "invoking nodetool flush"
nodetool flush ycsb usertable || exit 1
TIMEOUT=1800
waited=0
while : ; do
    pending=$(nodetool compactionstats | grep '^pending tasks' | tr -s ' ' | cut -d' ' -f3)
    if [ "$pending" = "0" ]; then
        break
    fi
    if [ $waited -ge $TIMEOUT ]; then
        echo "ERROR: compactions still pending after $waited s: $pending" >&2
        exit 1
    fi
    sleep 5
    waited=$((waited+5))
done
echo "waited $waited s for compactions"
nodetool tablestats ycsb.usertable

# step 3 (counters): n/a - the JMX metrics of Cassandra cannot be reset
