# Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Load durability 'unsafe' (-xld unsafe), runs after durability-relaxed.sh.
#          Doublewrite off for the load (switchable at runtime in MariaDB 12.3,
#          checked 2026-10-20): pages are written once, a crash during the load
#          can leave torn pages. The startup value is saved in
#          bexhoma.saved_settings; restoredurability-unsafe.sh restores it.
#          Runs as root (SET GLOBAL).
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_doublewrite', @@GLOBAL.innodb_doublewrite);
SET GLOBAL innodb_doublewrite = OFF;
SELECT @@GLOBAL.innodb_doublewrite;
EOF
