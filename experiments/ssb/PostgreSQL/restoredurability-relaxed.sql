-- Benchmark-Experiment-Host-Manager | experiments/ssb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'relaxed' after the load (post-load phase, right
--          before the check script): back to the configured value.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM RESET synchronous_commit;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW synchronous_commit;
