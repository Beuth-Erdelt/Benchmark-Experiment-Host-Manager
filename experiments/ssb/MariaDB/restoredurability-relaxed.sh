# Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Undo load durability 'relaxed' after the load (post-load phase, right
#          before the check script). Restores the value saved by
#          durability-relaxed.sh (a missing row keeps the current value), then
#          clears the saved values, so a later load on the same volume saves the
#          server's values again. Runs as root (SET GLOBAL).
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
SET @v = @@GLOBAL.innodb_flush_log_at_trx_commit;
SELECT CAST(value AS UNSIGNED) INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_flush_log_at_trx_commit';
SET GLOBAL innodb_flush_log_at_trx_commit = @v;
SELECT name, value AS saved_value FROM bexhoma.saved_settings ORDER BY name;
DELETE FROM bexhoma.saved_settings;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit;
EOF
