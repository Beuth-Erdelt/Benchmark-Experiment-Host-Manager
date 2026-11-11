-- Benchmark-Experiment-Host-Manager | experiments/tpcds/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'durable' after the load (post-load phase, right
--          before the check script): back to the configured values (template
--          and --set arguments), which may be less durable than the load was.
--          Resets the server and the database setting of synchronous_commit.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM RESET synchronous_commit;
ALTER SYSTEM RESET fsync;
ALTER SYSTEM RESET full_page_writes;
SELECT pg_reload_conf();
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I RESET synchronous_commit', current_database());
END
$$;
SELECT pg_sleep(1);
SHOW fsync;
SHOW full_page_writes;
-- SHOW synchronous_commit would show the load value: this session started with the
-- database setting; new sessions get the configured value (no database setting left)
SELECT d.datname, s.setconfig FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
    WHERE d.datname = current_database() AND s.setrole = 0;

-- #848: an ERROR if the database setting is still there (reads catalogs only)
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
               WHERE d.datname = current_database() AND s.setrole = 0
                   AND EXISTS (SELECT 1 FROM unnest(s.setconfig) c WHERE c LIKE 'synchronous_commit=%')) THEN
        RAISE EXCEPTION 'load durability: synchronous_commit is still set for database %', current_database();
    END IF;
END
$$;
