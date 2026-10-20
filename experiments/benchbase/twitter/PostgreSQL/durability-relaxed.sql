-- Benchmark-Experiment-Host-Manager | experiments/benchbase/twitter/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load durability 'relaxed' (-xld relaxed, the default), first pre-load
--          script. Commits return before the WAL is flushed; a crash loses the
--          last commits but never corrupts data. restoredurability-relaxed.sql
--          resets it after the load (ALTER SYSTEM survives restarts).
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM SET synchronous_commit = off;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW synchronous_commit;
