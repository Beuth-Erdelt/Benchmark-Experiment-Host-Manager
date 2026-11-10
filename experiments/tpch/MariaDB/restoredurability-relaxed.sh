# Benchmark-Experiment-Host-Manager | experiments/tpch/MariaDB
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
-- #848: an ERROR if a setting is not back at its saved value (e.g. adjusted with only a
-- warning); reads settings only. Plain SQL cannot raise an error, so a procedure in the
-- bexhoma helper schema does it and is dropped again; on an error the saved values stay.
DROP PROCEDURE IF EXISTS bexhoma.check_restored;
DELIMITER //
CREATE PROCEDURE bexhoma.check_restored()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE setting_name VARCHAR(64);
    DECLARE setting_value VARCHAR(255);
    DECLARE settings CURSOR FOR SELECT name, value FROM bexhoma.saved_settings;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN settings;
    check_loop: LOOP
        FETCH settings INTO setting_name, setting_value;
        IF done THEN
            LEAVE check_loop;
        END IF;
        SET @check_sql = CONCAT('SELECT @@GLOBAL.', setting_name, ' INTO @check_current');
        PREPARE check_stmt FROM @check_sql;
        EXECUTE check_stmt;
        DEALLOCATE PREPARE check_stmt;
        IF CAST(@check_current AS CHAR) <> setting_value THEN
            SET @check_msg = CONCAT('load durability: ', setting_name, ' is ', @check_current,
                                    ', not the saved ', setting_value);
            CLOSE settings;
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @check_msg;
        END IF;
    END LOOP;
    CLOSE settings;
END//
DELIMITER ;
CALL bexhoma.check_restored();
DROP PROCEDURE bexhoma.check_restored;
SELECT name, value AS saved_value FROM bexhoma.saved_settings ORDER BY name;
DELETE FROM bexhoma.saved_settings;
SELECT @@GLOBAL.innodb_flush_log_at_trx_commit;
EOF
