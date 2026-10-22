# Benchmark-Experiment-Host-Manager | experiments/ycsb/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Load durability 'relaxed' (-xld relaxed, the default), first pre-load
#          script. The redo log is written at commit but flushed once per second,
#          as the template had before -xld existed. The startup value is
#          saved in bexhoma.saved_settings; restoredurability-relaxed.sh restores it.
#          A shell script, because SET GLOBAL needs root (MARIADB_ROOT_PASSWORD of
#          the container) and loadData connects as bexhoma.
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_flush_log_at_trx_commit', @@GLOBAL.innodb_flush_log_at_trx_commit);
SELECT * FROM bexhoma.saved_settings;
SET GLOBAL innodb_flush_log_at_trx_commit = 2;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit;
EOF
