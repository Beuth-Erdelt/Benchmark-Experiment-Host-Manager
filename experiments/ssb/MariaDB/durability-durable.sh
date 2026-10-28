# Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Load durability 'durable' (-xld durable), first pre-load script.
#          The load runs crash-safe, whatever the server was started with (e.g.
#          --set flush 2 or doublewrite off): the redo log is flushed at
#          every commit and pages go through the doublewrite buffer (both can be
#          switched at runtime in MariaDB 12.3, checked 2026-10-20). Startup values
#          are saved in bexhoma.saved_settings; restoredurability-durable.sh
#          restores them. A shell script, because SET GLOBAL needs root.
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_flush_log_at_trx_commit', @@GLOBAL.innodb_flush_log_at_trx_commit),
  ('innodb_doublewrite', @@GLOBAL.innodb_doublewrite);
SELECT * FROM bexhoma.saved_settings;
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
SET GLOBAL innodb_doublewrite = ON;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit, @@GLOBAL.innodb_doublewrite;
EOF
