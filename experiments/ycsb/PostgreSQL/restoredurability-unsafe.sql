-- Benchmark-Experiment-Host-Manager | experiments/ycsb/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Undo load durability 'unsafe' after the load, before
--          restoredurability-relaxed.sql. Back to the configured fsync and
--          full_page_writes, then a checkpoint writes all dirty buffers.
--          restoredurability-unsafe.sh runs next and flushes the OS cache:
--          files written while fsync was off are not flushed by the checkpoint.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER SYSTEM RESET fsync;
ALTER SYSTEM RESET full_page_writes;
SELECT pg_reload_conf();
SELECT pg_sleep(1);
SHOW fsync;
SHOW full_page_writes;
CHECKPOINT;
