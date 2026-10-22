# Benchmark-Experiment-Host-Manager | experiments/ycsb/YugabyteDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Step 3 (counters) of the reset contract (docs/DBMS.md) for
#          YugabyteDB, run in the helper pod after the ANALYZE script.
#          pg_stat_reset() only resets the tserver a connection reaches, and
#          yb-tserver-service picks one per connection, so this connects to
#          every tserver pod of the Helm StatefulSet directly
#          (yb-tserver-N.yb-tservers, short names resolve in the namespace)
#          until a name does not resolve. Exits 1 if no tserver was reached
#          or a reset failed; the round starts anyway.
#          The same file is in every benchmark folder that has a YugabyteDB reset.
#          No curly braces in this file: bexhoma may fill it with str.format().

status=0
i=0
while getent hosts yb-tserver-$i.yb-tservers > /dev/null; do
    if psql -h yb-tserver-$i.yb-tservers -p 5433 -U yugabyte -d yugabyte -At -c "SELECT pg_stat_reset()" > /dev/null; then
        echo "pg_stat_reset() on yb-tserver-$i"
    else
        echo "pg_stat_reset() failed on yb-tserver-$i" >&2
        status=1
    fi
    i=$((i + 1))
done
if [ "$i" -eq 0 ]; then
    echo "no tserver yb-tserver-0.yb-tservers found, counters not reset" >&2
    exit 1
fi
echo "counters reset on $i tservers"

exit $status
