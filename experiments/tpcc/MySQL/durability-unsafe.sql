-- Benchmark-Experiment-Host-Manager | experiments/tpcc/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'unsafe' (-xld unsafe), runs after durability-relaxed.sql.
--          Disables the InnoDB redo log for the load: a server crash during the
--          load leaves the instance unusable. Doublewrite goes to DETECT_ONLY
--          (only metadata in the doublewrite buffer, torn pages are detected but
--          not repaired); MySQL 9.7 cannot switch it OFF at runtime, and not at
--          all when started with OFF (then this last statement fails and
--          doublewrite stays OFF). The startup value is saved in
--          bexhoma.saved_settings; restoredurability-unsafe.sql enables both again.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Save the startup value of doublewrite (first save wins)
CREATE DATABASE IF NOT EXISTS bexhoma;
CREATE TABLE IF NOT EXISTS bexhoma.saved_settings (name VARCHAR(64) PRIMARY KEY, value VARCHAR(255));
INSERT IGNORE INTO bexhoma.saved_settings VALUES
  ('innodb_doublewrite', @@GLOBAL.innodb_doublewrite);
COMMIT;

ALTER INSTANCE DISABLE INNODB REDO_LOG;
SHOW GLOBAL STATUS LIKE 'Innodb_redo_log_enabled';

-- last: fails (harmlessly) if the server was started with doublewrite OFF
SET GLOBAL innodb_doublewrite = DETECT_ONLY;
SELECT @@GLOBAL.innodb_doublewrite;
