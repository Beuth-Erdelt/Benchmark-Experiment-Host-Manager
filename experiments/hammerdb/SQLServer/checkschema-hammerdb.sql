-- Benchmark-Experiment-Host-Manager | experiments/hammerdb/SQLServer
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Post-load checks for TPC-C (HammerDB) on SQL Server (initscripts key 'Checks').
--          Runs last after loading: reports the settings in effect, writes a
--          checkpoint (dirty pages of the load to disk), and reports row counts,
--          sizes, the log written so far and the server configuration.
--          Load settings (-xld) are restored before, by restoredurability-*.sql.
--          The database is the current one (loadData switches to it).
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Edition and version
SELECT SERVERPROPERTY('Edition') AS edition, SERVERPROPERTY('ProductVersion') AS product_version,
       SERVERPROPERTY('ProductUpdateLevel') AS update_level;

-- Settings of the database
SELECT name, recovery_model_desc, delayed_durability_desc, is_auto_create_stats_on,
       is_auto_update_stats_on, is_read_committed_snapshot_on, snapshot_isolation_state_desc
FROM sys.databases
WHERE name = DB_NAME();
GO

-- Persist: write the dirty pages of the load
CHECKPOINT;
GO

-- Row counts (heap or clustered index) and sizes per table
SELECT t.name AS table_name,
       SUM(CASE WHEN ps.index_id IN (0, 1) THEN ps.row_count ELSE 0 END) AS row_count,
       SUM(ps.reserved_page_count) * 8 / 1024 AS reserved_mib,
       SUM(CASE WHEN ps.index_id > 1 THEN ps.reserved_page_count ELSE 0 END) * 8 / 1024 AS index_mib
FROM sys.dm_db_partition_stats ps
JOIN sys.tables t ON t.object_id = ps.object_id
GROUP BY t.name
ORDER BY reserved_mib DESC;

-- Data and log written since server start, i.e. mostly by the load
SELECT f.type_desc, f.name, f.size * 8 / 1024 AS size_mib,
       vfs.num_of_bytes_written / 1024 / 1024 AS written_mib
FROM sys.dm_io_virtual_file_stats(DB_ID(), NULL) vfs
JOIN sys.database_files f ON f.file_id = vfs.file_id;

SELECT total_log_size_in_bytes / 1024 / 1024 AS total_log_mib,
       used_log_space_in_bytes / 1024 / 1024 AS used_log_mib
FROM sys.dm_db_log_space_usage;

-- Server configuration that differs from the defaults of SQL Server 2022
SELECT name, value, value_in_use
FROM sys.configurations
WHERE name IN ('max server memory (MB)', 'min server memory (MB)', 'max degree of parallelism',
               'cost threshold for parallelism', 'max worker threads', 'optimize for ad hoc workloads')
ORDER BY name;
GO
