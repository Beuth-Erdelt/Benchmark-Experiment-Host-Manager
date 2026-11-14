-- Benchmark-Experiment-Host-Manager | experiments/hammerdb/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Reset contract (docs/DBMS.md) for TPC-C (HammerDB) on SQL Server, run
--          before each benchmarking round with -ar, in the current database.
--          Step 1 (statistics): sp_updatestats refreshes the statistics of every
--          table whose rows changed.
--          Step 2 (persist): CHECKPOINT writes the dirty pages; it comes after
--          step 1, as updating statistics writes pages again.
--          Step 3 (counters): clears the wait and latch statistics of the server.
--          The server-wide DMV counters of I/O and queries (sys.dm_io_*,
--          sys.dm_exec_query_stats) cannot be reset without a restart.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- step 1 (statistics)
EXEC sp_updatestats;
GO

-- step 2 (persist)
CHECKPOINT;
GO

-- step 3 (counters)
DBCC SQLPERF('sys.dm_os_wait_stats', CLEAR) WITH NO_INFOMSGS;
DBCC SQLPERF('sys.dm_os_latch_stats', CLEAR) WITH NO_INFOMSGS;
GO
