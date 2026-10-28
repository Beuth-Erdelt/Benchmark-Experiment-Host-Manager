# Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Undo load durability 'unsafe' after the load, before
#          restoredurability-relaxed.sh (which clears the saved values).
#          Restores doublewrite to its saved startup value (a missing row keeps
#          the current value). Runs as root (SET GLOBAL).
#          No curly braces in this file: bexhoma may fill it with str.format().

MYSQL="mariadb --user=root --password=$MARIADB_ROOT_PASSWORD"

$MYSQL <<'EOF'
SET @v = @@GLOBAL.innodb_doublewrite;
SELECT value INTO @v FROM bexhoma.saved_settings WHERE name = 'innodb_doublewrite';
SET GLOBAL innodb_doublewrite = @v;
SELECT @@GLOBAL.innodb_doublewrite;
EOF
