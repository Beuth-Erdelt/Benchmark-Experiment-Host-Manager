# Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Undo load durability 'durable' after the load (post-load phase, right
#          before the check script). Restores the values saved by
#          durability-durable.sh (a missing row keeps the current value), then
#          clears the saved values. Runs as root (SET GLOBAL).
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
SET @v = @@GLOBAL.innodb_flush_log_at_trx_commit;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_flush_log_at_trx_commit';
SET GLOBAL innodb_flush_log_at_trx_commit = @v;
SET @v = @@GLOBAL.innodb_doublewrite;
SELECT value INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_doublewrite';
SET GLOBAL innodb_doublewrite = @v;
SELECT name, value AS saved_value FROM bexhoma.saved_settings ORDER BY name;
DELETE FROM bexhoma.saved_settings;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_doublewrite;
EOF
