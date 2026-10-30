# Benchmark-Experiment-Host-Manager | experiments/ycsb/CockroachDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Post-load, before checkschema-ycsb.sql: wait until every range
#          has all its replicas and no learner replicas, so the benchmark does
#          not start while data still moves between the nodes. A loop in SQL
#          needs DO or PL/pgSQL, which v24.2.4 does not have (DO) or allows only
#          with an enterprise license (PL/pgSQL), so the loop is here.
#          Runs in the SUT container (client pod with the cockroach binary).
#          Fails after 30 minutes.

HOST="$BEXHOMA_WORKER_FIRST"
if [ -z "$HOST" ]; then
    echo "ERROR: BEXHOMA_WORKER_FIRST not set, cannot reach the cluster" >&2
    exit 1
fi
REPLICAS={num_worker_replicas}
QUERY="SELECT count(*) FROM crdb_internal.ranges WHERE array_length(learner_replicas, 1) > 0 OR array_length(replicas, 1) < $REPLICAS"

echo "wait for rebalancing: $REPLICAS replicas per range"
i=0
while [ $i -lt 360 ]; do
    pending=$(cockroach sql --insecure --host "$HOST" --format=csv -e "$QUERY" | tail -n 1)
    echo "$(date +%T) ranges pending: $pending"
    if [ "$pending" = "0" ]; then
        echo "wait for rebalancing: done"
        exit 0
    fi
    i=$((i + 1))
    sleep 5
done
echo "ERROR: ranges still pending after 30 minutes: $pending" >&2
exit 1
