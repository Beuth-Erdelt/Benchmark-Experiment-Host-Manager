# Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Steps 2 (persist) and 3 (counters) of the reset contract
#          (docs/DBMS.md) for MariaDB, run in the SUT pod after the ANALYZE
#          TABLE script. InnoDB has no CHECKPOINT statement: setting
#          innodb_max_dirty_pages_pct to 0 makes the page cleaner write all
#          dirty pages; the script waits until Innodb_buffer_pool_pages_dirty
#          is 0 (at most TIMEOUT seconds) and restores the old value. The
#          pages stay in the buffer pool, so caches stay warm. On timeout it
#          writes a message to stderr and exits 1; the round starts anyway.
#          SET GLOBAL needs root (MARIADB_ROOT_PASSWORD of the container).
#          The same file is in every benchmark folder that has a MariaDB reset.
#          No curly braces in this file: bexhoma may fill it with str.format().

TIMEOUT=600
MYSQL="mariadb --batch --skip-column-names --user=root --password=$MARIADB_ROOT_PASSWORD"

# step 2 (persist)
old=$($MYSQL -e "SELECT @@GLOBAL.innodb_max_dirty_pages_pct")
if [ -z "$old" ]; then
    echo "cannot read innodb_max_dirty_pages_pct, no flush" >&2
    exit 1
fi
echo "innodb_max_dirty_pages_pct was $old"
$MYSQL -e "SET GLOBAL innodb_max_dirty_pages_pct = 0"
start=$(date +%s)
status=0
while true; do
    dirty=$($MYSQL -e "SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_dirty'" | cut -f2)
    elapsed=$(( $(date +%s) - start ))
    echo "dirty pages: $dirty after $elapsed s"
    if [ "$dirty" = "0" ]; then
        break
    fi
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "flush timeout: $dirty dirty pages left after $elapsed s" >&2
        status=1
        break
    fi
    sleep 1
done
$MYSQL -e "SET GLOBAL innodb_max_dirty_pages_pct = $old"
echo "innodb_max_dirty_pages_pct restored to $old"

# step 3 (counters)
$MYSQL -e "FLUSH STATUS"
echo "FLUSH STATUS done"

exit $status
