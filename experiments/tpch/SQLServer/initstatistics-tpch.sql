-- Benchmark-Experiment-Host-Manager | experiments/tpch/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Collect optimizer statistics after loading (and optionally after
--          initindexes): all statistics of every TPC-H table, full scan.
--          No curly braces in this file: bexhoma may fill it with str.format().

UPDATE STATISTICS dbo.customer WITH FULLSCAN;
UPDATE STATISTICS dbo.lineitem WITH FULLSCAN;
UPDATE STATISTICS dbo.nation   WITH FULLSCAN;
UPDATE STATISTICS dbo.orders   WITH FULLSCAN;
UPDATE STATISTICS dbo.part     WITH FULLSCAN;
UPDATE STATISTICS dbo.partsupp WITH FULLSCAN;
UPDATE STATISTICS dbo.region   WITH FULLSCAN;
UPDATE STATISTICS dbo.supplier WITH FULLSCAN;
GO
